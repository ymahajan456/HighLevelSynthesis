# Title        : VHDL Generating Code
# Description  : This file contains functions than generate the VHDL Codes
#                based on the binding output from schedule and bind
# Developed by : Yogesh Mahajan (y.mahajan456@gmail.com)    (14D070022 @ IITB EE)
#                OV Shashank    (shashank[at]ee.iitb.ac.in) (14D070021 @ IITB EE)
#                Avineil Jain   (avineil96[at]ee.iitb.ac.in)(14D170002 @ IITB EE)   

# Note: In the following code all strings are maintained as lists
#       with each element representing a new line. Finally the join method
#       along with \n is used to create the printable version

'''
The following code contains functions to create the synthesisable 
VHDL code by using the scheduling and binding algorithm.

Requirements: 
The following design expects the userto provide/use their own 
implementations of ALU, and Register based on the entity as 
restricted by the following code. 
Using the given inputs it creates modular data_paths which contain
various combinations of the basic modules.
'''

import vhdl
import math
import os
from datetime import date
from copy import copy

'''
Provides a list of lists contaning signals which have 
everything except their names in common.

It is basically used to provide a compact representation
while defining the signals in an architecture or an entity
to decrease the line count of the output VHDL Code
'''
def consolidate_signals(signals):
    # Look at duplicates in signals
    consolidate = []
    for signal in signals:
        if signal not in consolidate:
            consolidate.append(signal)
    common = []
    for signal in consolidate:
        common.append([i for i in signals if signal == i])
    del consolidate

    # Because a line cannot contain a large number of signals
    # mainly for readability purposes, number of signal per line
    # is resitricted to 5 by the following code though it does not
    # preserve order
    change = True
    while(change):
        change = False
        for signals in common:
            if len(signals) > 5:
                common.append(signals[0:5])
                common.append(signals[5:])
                common.remove(signals)
                change = True
    return common

def generate_vhdl(top_level_name, binding_out):
    
    #Deflate from the given binding output
    bound_list = binding_out[4]
    store = binding_out[5]
    time = binding_out[6]
    alu_count = binding_out[7]
    reg_count = binding_out[8]
    alu_in = binding_out[10]
    reg_in = binding_out[11]
    input_list = binding_out[12]
    output_list = binding_out[13]
    out_locations = binding_out[14]

    #ALU Select Signal Mapping to Operations
    alu_ops_map = {
        "+": "000",
        "-": "001",
        "*": "010",
        "%": "011",
        "!": "100",
        "&": "101",
        "^": "110",
        "|": "111"
        }    
    alu_op_size = 3     #ceil(log2(len(alu_ops)))

    # Defining some ports and signals
    data_width = vhdl.integers("data_width","",16)
    clk = vhdl.std_logic("clk", 0, "IN")
    start = vhdl.std_logic("start", 0, "IN")
    complete = vhdl.std_logic("complete", 0, "OUT")
    ena = vhdl.std_logic("ena", 0, "IN")
    reset = vhdl.std_logic("reset", 0, "IN")
    clr = vhdl.std_logic("clr", 0, "IN")
    in_0 = vhdl.std_logic("inp", data_width.name, "IN")
    in_1 = vhdl.std_logic("in_1", data_width.name, "IN")
    in_2 = vhdl.std_logic("in_2", data_width.name, "IN")    
    out = vhdl.std_logic("outp", data_width.name, "OUT")
    select = vhdl.std_logic("sel", alu_op_size, "IN")

    #ALU and REG Component Definitions
    ALU = vhdl.vhdl_component("ALU", [in_1, in_2, out, select], [data_width]) 
    ALU.store_architecture(["ARCHITECTURE dummy OF ALU IS","BEGIN","\toutp <= (OTHERS => '0');", "END ARCHITECTURE;"])  
    REG = vhdl.vhdl_component("REG", [in_0, out, clk, clr, ena], [data_width])
    REG.store_architecture(["ARCHITECTURE dummy OF REG IS","BEGIN","\toutp <= (OTHERS => '0');", "END ARCHITECTURE;"])  

    #########################################################
    #DATA PATH CREATION
    #########################################################

    # Extract the multiplexor lengths required
    muxes_length_alu = [math.ceil(math.log2(len(i))) for j in alu_in for i in j ]
    muxes_length_reg = [math.ceil(math.log2(len(i))) for i in reg_in]

    # T Signal Port Length 
    T_signal_count = alu_count*alu_op_size + reg_count + sum(muxes_length_alu) + sum(muxes_length_reg)
    # T signal/port Object
    T_data = vhdl.std_logic("T", T_signal_count, "IN")
    
    # Ports for Data Path
    ports = [clk, reset, T_data]
    for i in input_list:
        ports.append(vhdl.std_logic(str(i), data_width.name, "IN"))
    for i in range(len(output_list)):
        ports.append(vhdl.std_logic("output_" + str(i), data_width.name, "OUT"))
    data_path = vhdl.vhdl_component("data_path", ports, [data_width])
    data_path_signals = []

    # Start the creation of the Data Path Architecture
    data_path_architecture = ["ARCHITECTURE data OF data_path is"] + [("\t" + i) for i in ALU.create_component()] + \
        ["\t" + i for i in REG.create_component()] + ["", "begin", ""]

    # Create all ALU Instances
    for i in range(alu_count):
        [string, signals] = ALU.create_instance([],[data_width.name])
        data_path_architecture += ["\t" + i for i in string]
        data_path_signals += signals
    
    # Create all Register Instances
    for i in range(reg_count):
        [string, signals] = REG.create_instance([],[data_width.name])
        data_path_architecture += ["\t" + i for i in string]
        data_path_signals += signals

    # Consolidate the signals
    common = consolidate_signals(data_path_signals)
    # Combine them with the architecture
    for signals in common:
        if(len(signals)==1):
            line = ""
        else:
            line = ", ".join([i.name for i in signals[1:]]) + ", "
        line += str(signals[0]) + ";"
        data_path_architecture.insert(1,"\tSIGNAL " + line)

    data_path_architecture.append("")   # Basically a new line
   
    T_count = 0                         # Stores the T_signals used until a point
    T_enable_mapping = {}               # Map of the register enables to appropritate T Signals
    T_ALU_select_mapping = {}           # Map of the ALU Operation Bits to appropriate T slices

    # Now to create all the mappings of signals to input ports as follows
    # Clocks, Reset, Enable , Data Width and ALU Select
    for signal in data_path_signals:
        if "clk" in signal.name:
            data_path_architecture.append("\t" + signal.name + " <= " + clk.name + ";")
        if "clr" in signal.name or "reset" in signal.name:
            data_path_architecture.append("\t" + signal.name + " <= " + reset.name + ";")
        if "sel" in signal.name:
            data_path_architecture.append("\t" + signal.name + " <= " + 'T ( '+ str(T_count) + ' TO ' + str(T_count + select.length - 1) + ' )' + ";")
            T_ALU_select_mapping[int(signal.name[7:])] = 'T ( '+ str(T_count) + ' TO ' + str(T_count + select.length - 1) + ' )'
            T_count += select.length
        if "ena" in signal.name:
            data_path_architecture.append("\t" + signal.name + " <= " + "T(" + str(T_count) + ");")
            T_enable_mapping[int(signal.name[7:])] = "T(" + str(T_count) + ")"
            T_count += 1

    data_path_architecture.append("")   # Again a new line

    # ALU Input Mapping based on ALU Input List
    # Because all inputs are from registers we have
    T_ALU_MUX_mapping = {}              # Map of the ALU Input Multiplexor Bits to appropriate T slices

    for alu_num in range(alu_count):
        mapping = []
        for i in range(2):
            mux_length = muxes_length_alu[alu_num*2 + i]
            data_path_architecture.append("\tin_" + str(i+1) + "_ALU" + str(alu_num) + " <= outp_REG" + str(alu_in[alu_num][i][0]))
            for input in range(1, len(alu_in[alu_num][i])):
                data_path_architecture.append('\t\twhen (T ( '+ str(T_count) + ' TO ' + str(T_count + mux_length - 1) + ' ) = "' + \
                    ('{0:0'+ str(mux_length) +'b}').format(input-1) + '") else outp_REG' + str(alu_in[alu_num][i][input]))
            if not mux_length == 0:
                mapping.append('T ( '+ str(T_count) + ' TO ' + str(T_count + mux_length - 1) + ' )')
            else:
                mapping.append('')
            T_count += mux_length
            data_path_architecture[-1] += ";" 
        T_ALU_MUX_mapping[alu_num] = mapping
    data_path_architecture.append("")

    # REG Input Mapping based on REG Input List
    # Because inputs to the register can be from global 
    # inputs as well we have

    T_REG_MUX_mapping = {}               # Map of the REG Input Multiplexor Bits to appropriate T slices
    for reg_num in range(reg_count):
        mux_length = muxes_length_reg[reg_num]
        if (isinstance(reg_in[reg_num][0],int)):
            data_path_architecture.append("\tinp_REG" + str(reg_num) + " <= outp_ALU" + str(reg_in[reg_num][0]))
        else:
            data_path_architecture.append("\tinp_REG" + str(reg_num) + " <= " + reg_in[reg_num][0])
        for input in range(1, len(reg_in[reg_num])):
            if (isinstance(reg_in[reg_num][input],int)):
                data_path_architecture.append('\t\twhen (T ( '+ str(T_count) + ' TO ' + str(T_count + mux_length - 1) + ' ) = "' + \
                    ('{0:0'+ str(mux_length) +'b}').format(input-1) + '") else outp_ALU' + str(reg_in[reg_num][input]))
            else:
                data_path_architecture.append('\t\twhen (T ( '+ str(T_count) + ' TO ' + str(T_count + mux_length - 1) + ' ) = "' + \
                    ('{0:0'+ str(mux_length) +'b}').format(input-1) + '") else ' + reg_in[reg_num][input])
        if not mux_length == 0:
            T_REG_MUX_mapping[reg_num] = 'T ( '+ str(T_count) + ' TO ' + str(T_count + mux_length - 1) + ' )'
        T_count += mux_length
        data_path_architecture[-1] += ";" 
    data_path_architecture.append("")   

    # Mapping the global outputs to registers' outputs
    for output in range(len(output_list)):
        data_path_architecture.append("\toutput_" + str(output) + " <= outp_REG" + str(out_locations[output_list[output]]) + ";")

    data_path_architecture.append('END ARCHITECTURE;')
    data_path.store_architecture(data_path_architecture)
    data_path_string = data_path.create_complete()

    #########################################################
    #CONTROL PATH CREATION
    #########################################################

    # Create a copy to be edited 
    T_control = copy(T_data)
    T_control.type = "OUT"

    # The control path component
    control_path = vhdl.vhdl_component("control_path",[start, complete, clk, reset, T_control]) 
        
    states = ["init"] + ["S" + str(i) for i in range(time)] + ["done"]          # States of the FSM
    next_states = states[1:] + [states[0]]                                      # Next states of the FSM
     
    # Initial path of the control path architecture is sort of hardcoded
    control_path_architecture = ["ARCHITECTURE control OF control_path IS", 
                                 "\tTYPE fsm_state IS ( "+ ", ".join(states) + " );",
                                 "\tSIGNAL nQ, Q: fsm_state := " + states[0] + ";", "", "BEGIN", "\tclock: PROCESS(" + clk.name + ")",
                                 "\tBEGIN","\t\tif(" + clk.name + "'EVENT AND " + clk.name + " = '1') THEN",
                                 "\t\t\tQ <= nQ;","\t\tEND IF;","\tEND PROCESS;","","\tnext_state: PROCESS( reset, " + start.name + ", Q )","\tbegin",
                                 "\t\tnQ <= Q;"," \t\tIF (" + reset.name + " = '1') THEN", "\t\t\tnQ <= " + states[0] + ";",
                                 "\t\tELSE", "\t\t\tCASE Q IS","\t\t\t\tWHEN " + states[0] + " =>","\t\t\t\t\tif (" + start.name + \
                                     " = '1') then nQ <= " + next_states[0] + ";", "\t\t\t\t\tEND IF;"] + \
                                     ["\t\t\t\tWHEN " + states[i] + " => nQ <= " + next_states[i] + ";" for i in range(1,len(states))] + \
                                     ["\t\t\t\tWHEN OTHERS => nQ <= " + states[0] + ";", "\t\t\tEND CASE;", "\t\tEND IF;", "", "\tEND PROCESS;", "",
                                      "\tT_process: PROCESS ( Q )","\tBEGIN","\t\tT <= (OTHERS => '0');", "\t\t" + complete.name + " <= '0';","\t\tCASE Q IS"]

    # The Main Part - Controlling the T Signals based on the binding output and the T Maps created before
    # The following sections involve decoding the binding output for generation of the FSM
    # The register enables
    reg_enables = [[] for i in states]
    reg_enables[0] = [i for i in range(len(input_list))]
    for i in range(1,len(states)-1):
        reg_enables[i] = [num for reg in bound_list[i-1].values() for num in reg[3]]

    # ALU Operations
    alu_operation_select = [["000" for j in range(alu_count)] for i in states]
    for i in range(1,len(states)-1):
        for alu_num in bound_list[i-1].keys():
            alu_operation_select[i][alu_num] = alu_ops_map[bound_list[i-1][alu_num][0]]

    # ALU Input Multiplexor Control
    alu_mux_select = [[('{0:0' + str(j) + 'b}').format(0) if j is not 0 else '' for j in muxes_length_alu] for i in states]
    alu_mux_select = [[[alu_mux_select[j][i],alu_mux_select[j][i+1]] for i in range(0,alu_count*2,2)] for j in range(len(states))]
    for i in range(1,len(states)-1):
        for alu_num in bound_list[i-1].keys():
            for j in range(2):
                if alu_mux_select[i][alu_num][j] is not '':
                    alu_mux_select[i][alu_num][j] = ('{0:0' + str(muxes_length_alu[alu_num*2 + j]) + 'b}').format(alu_in[alu_num][j].index(bound_list[i-1][alu_num][2][j]))

    #Reg Input Multiplexor Control
    reg_mux_select = [[('{0:0' + str(j) + 'b}').format(0) if j is not 0 else '' for j in muxes_length_reg] for i in states]
    for i in range(len(input_list)):
        if muxes_length_reg[i] is not 0: 
            reg_mux_select[0][i] = ('{0:0' + str(muxes_length_reg[i]) + 'b}').format(reg_in[i].index(input_list[i]))
    for i in range(1,len(states)-1):
        for alu_num in bound_list[i-1].keys():
            reg = bound_list[i-1][alu_num][3]
            if reg and muxes_length_reg[reg[0]] is not 0:
                reg = reg[0]
                reg_mux_select[i][reg] = ('{0:0' + str(muxes_length_reg[reg]) + 'b}').format(reg_in[reg].index(alu_num))


    # Assigning the appropriate T signals to their appropriate values
    for state in range(len(states)):
        control_path_architecture.append("\t\t\tWHEN " + states[state] + " =>")
        # Register Enables
        for i in reg_enables[state]:
            control_path_architecture.append("\t\t\t\t" + T_enable_mapping[i] + " <= '1';")
        # ALU Operations
        for i in range(len(alu_operation_select[state])):
            if alu_operation_select[state][i] != "".join(['0' for j in alu_operation_select[state][i]]):
                control_path_architecture.append("\t\t\t\t" + T_ALU_select_mapping[i] + ' <= "' + alu_operation_select[state][i] + '";')
        # ALU Input Multiplexors
        for i in range(len(alu_mux_select[state])):
            for j in range(2):
                if alu_mux_select[state][i][j] != '' and alu_mux_select[state][i][j] != "".join(['0' for j in alu_mux_select[state][i][j]]):
                    control_path_architecture.append("\t\t\t\t" + T_ALU_MUX_mapping[i][j] + ' <= "' + alu_mux_select[state][i][j] + '";')
        # REG Input Multiplexors
        for i in range(len(reg_mux_select[state])):
             if reg_mux_select[state][i] != '' and reg_mux_select[state][i] != "".join(['0' for j in reg_mux_select[state][i]]):
                control_path_architecture.append("\t\t\t\t" + T_REG_MUX_mapping[i] + ' <= "' + reg_mux_select[state][i] + '";')
        # If not T signals were required
        if control_path_architecture[-1] == "\t\t\tWHEN " + states[state] + " =>":
            control_path_architecture.pop(-1)

    # Finish the architecture
    control_path_architecture.append("\t\t\tWHEN " + states[-1] + " => " + complete.name + " <= '1';")
    control_path_architecture += ["\t\tEND CASE;", "\tEND PROCESS;", "", "END ARCHITECTURE;"]

    # Store and create the printable version
    control_path.store_architecture(control_path_architecture)
    control_path_string = control_path.create_complete()

    # Global Entity Creation
    ports.remove(T_data)
    ports += [start, complete]
    T_data.type = ""
    top_level = vhdl.vhdl_component(top_level_name, ports, [data_width])

    # Create the architecture with the data and control path components
    top_level_architecture = ["ARCHITECTURE top_level OF " + top_level_name + " IS"] + \
        ["\t" + i for i in data_path.create_component()] + [""] + ["\t" + i for i in control_path.create_component()] + ["\tSIGNAL " + str(T_data) + ";"] + \
        ["", "BEGIN"]
    top_level_signals = []

    # The following follows the same procedure as the data_path creation
    [string, signals] = data_path.create_instance([],[data_width.name],[port.name for port in data_path.ports])
    top_level_signals += signals
    top_level_architecture += ["\t" + i for i in string] + [""]

    [string, signals] = control_path.create_instance([],[data_width.name],[port.name for port in control_path.ports])
    top_level_signals += signals
    top_level_architecture += ["\t" + i for i in string] + [""]

    # Consolidate the signals
    common = consolidate_signals(top_level_signals)
    #Combine them with the architecture
    for signals in common:
        if(len(signals)==1):
            line = ""
        else:
            line = ", ".join([i.name for i in signals[1:]]) + ", "
        line += str(signals[0]) + ";"
        top_level_architecture.insert(1,"\tSIGNAL " + line)

    # Finish off the architecture
    top_level_architecture += ["END ARCHITECTURE;"]
    top_level.store_architecture(top_level_architecture)
    top_level_string = top_level.create_complete()

    #Output into files
    output_directory = top_level_name + "_VHDL"
    if not os.path.exists("./"+ output_directory +"/"):
        os.makedirs(""+ output_directory +"")

    file = open("./"+ output_directory +"/data_path.vhd",'w')
    file.write("\n".join(["", "-- ============================================================",
                          "-- File Name: data_path.vhd",
                          "-- ============================================================",
                          "-- ************************************************************",
                          "-- THIS IS A AUTO-GENERATED FILE. DO NOT EDIT THIS FILE!",
                          "-- ", "-- 2.0 BUILD. GENERATED ON " + str(date.today()), 
                          "-- ************************************************************", ""] + data_path_string))
    file.close()

    file = open("./"+ output_directory +"/control_path.vhd",'w')
    file.write("\n".join(["", "-- ============================================================",
                          "-- File Name: control_path.vhd",
                          "-- ============================================================",
                          "-- ************************************************************",
                          "-- THIS IS A AUTO-GENERATED FILE. DO NOT EDIT THIS FILE!",
                          "-- ", "-- 2.0 BUILD. GENERATED ON " + str(date.today()), 
                          "-- ************************************************************", ""] + control_path_string))
    file.close()

    file = open("./"+ output_directory +"/" + top_level_name + ".vhd",'w')
    file.write("\n".join(["", "-- ============================================================",
                          "-- File Name: " + top_level_name + ".vhd",
                          "-- ============================================================",
                          "-- ************************************************************",
                          "-- THIS IS A AUTO-GENERATED FILE. DO NOT EDIT THIS FILE!",
                          "-- ", "-- 2.0 BUILD. GENERATED ON " + str(date.today()), 
                          "-- ************************************************************", ""] + top_level_string))
    file.close()

    alu_ops_map = {
        "ADD": "000",
        "SUBTRACT": "001",
        "MULTIPLY": "010",
        "DIVIDE": "011",
        "NOT": "100",
        "AND": "101",
        "XOR": "110",
        "OR": "111"
        }    

    alu_ops_map = {alu_ops_map[i]:i for i in alu_ops_map.keys()}
    keys = list(alu_ops_map.keys())
    keys.sort()
    map = ["--\t\t" + i + " => " + alu_ops_map[i] for i in keys]
    file = open("./"+ output_directory +"/ALU.vhd",'w')
    file.write("\n".join(["", "-- ============================================================",
                          "-- File Name: ALU.vhd",
                          "-- ============================================================",
                          "-- ************************************************************",
                          "-- THIS IS A DUMMY FILE. DO NOT EDIT THE ENTITY STRUCTURE",
                          "-- ONLY REPLACE THE ARCHITECTURE BY YOUR OWN ARCHITECTURE",
                          "-- ", "-- 2.0 BUILD. GENERATED ON " + str(date.today()), 
                          "-- ************************************************************", "",
                          "-- ALU SELECT SIGNAL MAPPING TO THE RESPECTIVE OPERATIONS:"] + \
                              ["\n".join(map), ""] + ALU.create_complete()))
    file.close()

    file = open("./"+ output_directory +"/REG.vhd",'w')
    file.write("\n".join(["", "-- ============================================================",
                          "-- File Name: REG.vhd",
                          "-- ============================================================",
                          "-- ************************************************************",
                          "-- THIS IS A DUMMY FILE. DO NOT EDIT THE ENTITY STRUCTURE",
                          "-- ONLY REPLACE THE ARCHITECTURE BY YOUR OWN ARCHITECTURE",
                          "-- ", "-- 2.0 BUILD. GENERATED ON " + str(date.today()), 
                          "-- ************************************************************", ""] + REG.create_complete()))
    file.close()

    file = open("./"+ output_directory +"/" + top_level_name + ".cmp", 'w')
    file.write("\n".join(["", "-- ============================================================",
                          "-- File Name: " + top_level_name + ".cmp",
                          "-- ============================================================",
                          "-- ************************************************************",
                          "-- THIS IS A COMPONENT FILE. CONTAINS THE COMPONENT",
                          "-- OF THE TOP LEVEL WHICH CAN BE DIRECTLY USED",
                          "-- ", "-- 2.0 BUILD. GENERATED ON " + str(date.today()), 
                          "-- ************************************************************", "",
                          "-- NO COPYRIGHT EXISTS FOR THIS CODE", "-- USE IT AS YOU WISH :P", ""] + top_level.create_component()))
    file.close()

    file = open("./"+ output_directory +"/" + top_level_name + "_inst.vhd", 'w')
    file.write("\n".join(["", "-- ============================================================",
                          "-- File Name: " + top_level_name + "_inst.vhd",
                          "-- ============================================================",
                          "-- ************************************************************",
                          "-- THIS IS A SAMPLE INSTANCE FILE. CONTAINS AN INSTANCE",
                          "-- OF THE TOP LEVEL WHICH CAN BE DIRECTLY USED",
                          "-- ", "-- 2.0 BUILD. GENERATED ON " + str(date.today()), 
                          "-- ************************************************************", "",
                          "-- NO COPYRIGHT EXISTS FOR THIS CODE", "-- USE IT AS YOU WISH :P", ""] + top_level.create_instance()[0]))
    file.close()

#infix_inputs = []
#infix_inputs.append("(a+b)+(c+d)+(a+b)*(c+d)")
#infix_inputs.append("(a+b)+(c+d)-(a-b)*(c-d)")
#infix_inputs.append("(a+b)*(c+d)+(a-b)*(c-d)")
#infix_inputs.append("(a+b)+(c+d)")
#infix_inputs.append("(a+b)+(c+d)+(a-b)")
#infix_inputs.append("(a+b)*(c+d)+(a-b)+(c-d)")

#Get data by using scheduling and binding
#output = schedule_and_bind(infix_inputs,5)
#generate_vhdl("top_level", output)

#for i in output:
#    print(i)
#pass