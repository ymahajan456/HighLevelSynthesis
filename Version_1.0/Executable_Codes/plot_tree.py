# Title			: Plotting Expression Tree and Data Path
# Developed by : Yogesh Mahajan (y.mahajan456@gmail.com)    (14D070022 @ IITB EE)
#                OV Shashank    (shashank[at]ee.iitb.ac.in) (14D070021 @ IITB EE)
#                Avineil Jain   (avineil96[at]ee.iitb.ac.in)(14D170002 @ IITB EE)   
# Description	: Generating DOT files for both expression tree and data path from binding result
#				  Use this DOT files to generate png files using PyDot and Graphviz

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
"""
Dependencies : 
--------------
    1. pydot (1.2.3 or above) 
    2. graphviz (Windows: must be added to PATH variable)

Functions :
--------------
    1. generate_tree_dot_file(--)
        * generates DOT file for plotting expression tree
        
    2. generate_data_path_dot_file(--)
        * generates DOT file for plotting data path
        * lot of work needed as lacement is done by Graphviz. Result may nat be very good :)
        
    3. gen_png_from_dot_file(--)
        * Generated images from DOT files.
"""
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

# import dependencies

import graphviz
import pydot

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------
"""
1. Generate DOT File for Expression Tree

    * Inputs: Combined leveled tree of expressions, Output file name
    * Output DOT FIle format: Inputs are given by Square boxes. All other nodes are given by Circles
     
"""
#--------------------------------------------------------------------------------------------------
def generate_tree_dot_file(leveled_tree,out_file_name):
    tree = {}
    for i in range(len(leveled_tree)):             # generate combined tree
        tree.update(leveled_tree[i])
    out_file = open(out_file_name + "_tree.dot", "w")
    out_file.write("digraph tree {\n")          # directed Grapg
    out_file.write("graph [ dpi = 300]\n")      # DPI = 300
    out_count = 0
    for node in tree.keys():
        node_label = tree[node][0]
        out_file.write(str(node) + " [ label = \""+ str(node_label) + "\"]\n")
        if (tree[node][2] == 0):
            out_file.write(str(node) + " [ shape = box ]\n") # Inputs
        else:
            out_file.write(str(node) + " [ shape = circle ]\n")     # other nodes

        for child in tree[node][1]:
            out_file.write(str(child) + " -> "+ str(node) + "\n")   # add edges
    out_file.write("}\n")
    out_file.close()
    return True



#--------------------------------------------------------------------------------------------------
"""
2. Generate DOT File for Expression Tree

    * Inputs: ALUs' input lists, Registers' input iists, Outputs lIst, Output Addresses, Output file name
    * Output DOT FIle format: 
        Register : Golden Box
        ALU      : Green Trapezium
        MUX      : Gray Circle
        Inputs   : Red Circle
        Output   : Red Doublecircle
        
"""
#--------------------------------------------------------------------------------------------------    
def generate_data_path_dot_file(alu_in,reg_in,input_list,output_list,out_locations,out_file_name):
    out_file = open(out_file_name + "_data_path.dot",'w')
    out_file.write("digraph data_path{\n")
    out_file.write("graph [ dpi = 300 ];\n")
    #out_file.write("rankdir=LR\n")
    
    #--------------
    # Define Nodes
    #--------------
    
    # Add Registers
    #---------------
    reg_count = len(reg_in)
    reg_names = ["\"Reg_"+str(i)+"\"" for i in range(reg_count)]
    for reg in range(reg_count):
        out_file.write(reg_names[reg] + " [ shape = box, style = filled, fillcolor = gold ] ;\n")
    
    # Add ALUs
    #----------
    alu_count = len(alu_in)
    alu_names = ["\"ALU_"+str(i)+"\"" for i in range(alu_count)]
    for alu in range(alu_count):
        out_file.write(alu_names[alu] + " [ shape = trapezium, style = filled, fillcolor = lawngreen ] ;\n")
        
    # Add ALU Input MUXes
    #---------------------
    alu_in_mux_names = [[],[]]
    alu_in_mux_names[0] = ["\"alu_mux_"+str(i)+"_0\"" for i in range(alu_count)]
    for mux_name in alu_in_mux_names[0]:
        out_file.write(mux_name + " [shape = circle, style = filled, fillcolor = gray, label = \"Mux\"] ; \n")
    alu_in_mux_names[1] = ["\"alu_mux_"+str(i)+"_1\"" for i in range(alu_count)]
    for mux_name in alu_in_mux_names[1]:
        out_file.write(mux_name + " [shape = circle, style = filled, fillcolor = gray, label = \"Mux\"] ; \n")
    
    # Add Register Input MUX
    #-------------------------
    reg_in_mux_names = ["\"reg_mux_"+str(i)+"\"" for i in range(reg_count)]
    for mux_name in reg_in_mux_names :
        out_file.write(mux_name + " [shape = circle, style = filled, fillcolor = gray, label = \"Mux\"] ; \n")
    
    # Inputs
    #--------
    for inp in input_list :
        out_file.write("\""+inp+"\"" + " [shape = circle style = filled, fillcolor = red];\n") 
    
    
    
    #--------------
    # Define Edges
    #-------------- 
    
    # ALU Input MUXes -> ALU Inputs
    #--------------------------------
    for alu in range(alu_count):
        out_file.write(alu_in_mux_names[0][alu] + " -> " + alu_names[alu] + " [ label = \"0\" ];\n")
        out_file.write(alu_in_mux_names[1][alu] + " -> " + alu_names[alu] + " [ label = \"1\" ];\n")
    
    # Register Inputs -> Reg Input MUX
    #------------------------------------
    for reg in range(reg_count):
        out_file.write(reg_in_mux_names[reg] + " -> " + reg_names[reg] + " ;\n")
        i = 0
        for inp in reg_in[reg] :
            if inp in input_list :
                out_file.write("\"" + inp+ "\"" + " -> " + reg_in_mux_names[reg] + " [ label = \""+ str(i)+"\" ];\n")
            else:
                out_file.write(alu_names[inp] + " -> " + reg_in_mux_names[reg] + " [ label = \""+ str(i)+"\" ];\n")
            i = i+1
    
    # ALU Inputs -> ALU Input MUX
    #------------------------------------    
    for mux in range(alu_count):
        i = 0
        for inp in alu_in[mux][0] :
            out_file.write(reg_names[inp] + " -> " + alu_in_mux_names[0][mux] + " [ label = \""+ str(i)+"\" ];\n")  
            i = i+1
        i = 0
        for inp in alu_in[mux][1] :
            out_file.write(reg_names[inp] + " -> " + alu_in_mux_names[1][mux] + " [ label = \""+ str(i)+"\" ];\n")  
            i = i+1  
    # Define output nodes and connect them
    #---------------------------------------
    for out in range(len(output_list)):
        out_reg_name = reg_names[out_locations[output_list[out]]]
        out_file.write(out_reg_name + " -> \"output" + str(out) + "\" ;\n")
        out_file.write("\"output" + str(out) + "\"" + " [shape = doublecircle style = filled, fillcolor = red];\n")
                
    #out_file.write("{ rank = same; ")
    #for inp in input_list:
    #    out_file.write("\"" + inp+ "\" ")
    #out_file.write("}\n")
    #out_file.write("} -> ")
    
    #out_file.write("{ rank = same; ")
    #for alu in range(alu_count):
    #    out_file.write(alu_names[alu] + " ")
    #out_file.write("}\n")
    #out_file.write("} -> ") 
    
    #out_file.write("{ rank = same; ")
    #for out in range(len(output_list)):
    #    out_file.write("\"output" + str(out) + "\" ")
    #out_file.write("}\n")
    #out_file.write("} -> ")
    #out_file.write("} [style=invis]; \n")
    
    
    out_file.write("}\n")
    out_file.close()       


#---------------------------------------------------------------------------------------------------

# Debug Structure
#------------------    
#from postfix2bdt import *
#postfix = ['a', 'c', '+', 'e', 'r', '-', 'y', 'a', '+', 'j', '*', '^', 'w', 'e', '*', 'q', '-', '/', '-', 'a', 'b', 'c', '-', '*', '+', 'w', '^']
#[bdt,parent] = postfix2bdt(postfix)
#k = generate_dot_from_tree(bdt,"first_tree")
#(graph,) = pydot.graph_from_dot_file('first_tree.dot')
#graph.write_png('first_tree.png') 


#--------------------------------------------------------------------------------------------------
"""
3. Genera PNG files from DOT Files
"""
#--------------------------------------------------------------------------------------------------
def gen_png_from_dot_file(file_name):
    (graph_tree,) = pydot.graph_from_dot_file(file_name + '_tree.dot')
    graph_tree.write_png(file_name + '_tree.png') 
    
    (graph_tree,) = pydot.graph_from_dot_file(file_name + '_data_path.dot')
    graph_tree.write_png(file_name + '_data_path.png') 


#--------------------------------------------------------------------------------------------------    

