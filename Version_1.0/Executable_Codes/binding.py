# Title        : Hardware Scheduling and Binding from infix expressions
# Developed by : Yogesh Mahajan (y.mahajan456@gmail.com)    (14D070022 @ IITB EE)
#                OV Shashank    (shashank[at]ee.iitb.ac.in) (14D070021 @ IITB EE)
#                Avineil Jain   (avineil96[at]ee.iitb.ac.in)(14D170002 @ IITB EE)   
# Description  : Generate hardware binding solution for set of infix expressions to be evaluated simulteniously


#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
"""
Assumptions :
--------------
    1. Operations are executed by set of identical Arithmatic and Logic Units
    2. Each ALU can execute every type of operation
    3. Number of operands of each operands must be less than or equal to 2 (can be changed with minor efforts)  
--------------            
Dependencies : 
--------------
    1. postfix2bdt.py 
    2. infix2postfix.py
"""

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
"""
    Functions :
    --------------
    1. combine_leveled_trees_with_signle_parent(--)
        * combine leveled trees with single output (parent node) to on leveled tree 
         
    2. get_leveled_tree(--)
        * Generate leveled tree from tree directory 
        
    3. get_out_list(--)
        * Generate fanout list for each node from unleveled tree directory

    4. get_priority_list(--)
        * generate scheduling priority list for all operations in tree 

    5. ls_from_tree(--)
        * Priority based list scheduling of all opeartions in tree

    6. identical_nodes(--)
        * returns true if two nodes are identical

    7. remove_identical_nodes(--)
        * removes identical nodes from tree and regenerate leveled tree and fanout list
          
    8. variable_life_time(--)
        * generate list of all the active variables at each time cycle 
          
    9. binding(--)
        * generate binding from scheduled list of processes
          
    10.get_combined_trees(--)
        * get combined trees from set of infix expressions
          
    11.schedule_and_bind(--)      
        * main scheduling and binding function   
"""    
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------


# import dependencies
from postfix2bdt import *
from infix2postfix import *
#from copy import deepcopy

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
"""
Data structures :
------------------
    1. Postfix : List holding names of variables and opeartors in postfix order for given infix exression

    2. Trees : tree is a dictionary of nodes
        * Keys are node names
        * Values are lists holding information about node
        * Values format : [_opeartion, _List of children, _level of node]
                        opeartion will hold name of variavle in case of input variable node
                        Input variable nodes are in level 0 and level increases as we move from inputs to outputs in tree

    3. Leveled trees : Leveled tree is list of dictionaries holding nodes of same level in ascesding order
        * Leveled tree reduces traversing complexity of large tree directory br breaking it in to small directories
        * Dictionary of level 0 nodes is at index 0 of list
        
    4. Schedule : Time scheduled output of list scheduling function
        * List of dictionaries, one dictionary for each time cycle
        * Keys of dictionaries are addresses (integer) of ALU 
        * Values are lists holding information or particular operation under execution
        * Values format : [_Operator, _Ordered ist of inputs, _Time cycles remaining]
                        _Operator : Defines the opeartion to be performed by ALU
                        _Time cycles remaining : Remaining time cycles including current cycle
        * If ALU is not in directory of some time instance then that ALU is ideal in that time cycle
                        
    5. Store : List of lists 
        * Each sublist defines containts of each register 
        
    6. Bound List :  List of directories holding binding information for each time cycle
        * Keys of directory are addresses(integer) of ALUs 
        * Values are lists holding binding information for ALU and registers
        * Values format : [_Operator, _Ordered list of input register addresses(integer), _list of address of output destination register(if Any)] 
        ** Output register addresses is also list considering multiple output from ALU (Future Work may be)
"""           
#--------------------------------------------------------------------------------------------------   






 
#--------------------------------------------------------------------------------------------------
"""
1. Combine Leveled Trees With Single Parent

    * combine leveled trees with single output (parent node) to on leveled tree 
    * Here single output tree -> tree generated from one infix expression 
    * This function won't remove duplicate or similar nodes from trees  
    * Nodes from all trees must have different nodes (Except for input variable nodes)

    * Inputs : List of leveled trees to be combined
    * Output : Combined Leveled tree  
"""
#--------------------------------------------------------------------------------------------------

def combine_leveled_trees_with_signle_parent(leveled_trees = []):
    num_of_trees = len(leveled_trees)
    if(num_of_trees == 0):                   # Nothing in input
        return None
    if(num_of_trees == 1):                   # only one tree return as it is
        return leveled_trees[0]
        
    level_counts = [len(tree) for tree in leveled_trees] 
    max_level = max(level_counts)              # max level in combined tree
    combined_level_tree = [{} for level in range(max_level)]
            
    for tree in range(num_of_trees):           # append nodes levelwise from each tree to combined tree
        for level in range(level_counts[tree]):
            for node in leveled_trees[tree][level].keys():
                combined_level_tree[level][node] = leveled_trees[tree][level][node]     
    
    return combined_level_tree
    
    
    
    
#--------------------------------------------------------------------------------------------------
"""
2. Get Leveled Tree

    * Generate leveled tree from tree directory 
    * Parent node is one of the nodes with maximum level nodes

    * Inputs : Tree and output node of tree i.e. parent node (one of nodes having maximum level count which is also one of the outputs)
    * Outputs : Leveled tree for input tree
"""
#-------------------------------------------------------------------------------------------------

def get_leveled_tree(unleveled_tree,parent_node):
    max_level = unleveled_tree[parent_node][2]
    #print(unleveled_tree)
    leveled_tree = [{} for i in range(max_level+1)]      # level 0 inclusive
    for node_name in unleveled_tree.keys():  
        #print(node_name)           
        leveled_tree[unleveled_tree[node_name][2]][node_name] = unleveled_tree[node_name]
    return leveled_tree
    
    
    
#--------------------------------------------------------------------------------------------------
# Define time taken by each operation in terms of clock cycles
# op_time => directory holding operation times
# commutative_op => list of commutative opertors
#--------------------------------------------------------------------------------------------------    
op_time = {}
op_time['@'] = 4    # exponent
op_time['*'] = 3    # mul
op_time['/'] = 3    # div
op_time['%'] = 3    # modulo
op_time['+'] = 2    # add
op_time['-'] = 2    # sub

op_time['!'] = 1     # NOT
op_time['&'] = 1     # AND
op_time['^'] = 1     # XOR
op_time['|'] = 1     # OR
 

commutative_op = ['*','+','&','|','^']  # commutative opertor


#--------------------------------------------------------------------------------------------------
"""
3. Get Out List

    * Inputs : Tree
    * Output : Dictionary of Fanout Lists with each node as key
"""
#--------------------------------------------------------------------------------------------------
def get_out_list(unleveled_tree):
    out_list = {node:[] for node in unleveled_tree.keys()}
    for node in unleveled_tree.keys():
        for child in unleveled_tree[node][1]:
            out_list[child].append(node)
    return out_list


    
#--------------------------------------------------------------------------------------------------
"""
4. get Priority List

    * Dictionary of execution priority of each non variable node
    * Priority value indicate maximum timed distance of that node (including self delay) from output nodes
    * This help to evenly distribute work between ALUs 
    
    * Inputs : Tree, Leveled Tree, Fanout List, Output Nodes List
    * Outputs : Dictionary {node_name : Priority Value}
    
    * Algo : priority[node] = max{Priority if Fanout nodes} + delay
"""
#--------------------------------------------------------------------------------------------------
def get_priority_list(tree,leveled_tree,out_list,output_list):
    level_count = len(leveled_tree)
    priority_list = {}
    for node in output_list:                      # Output Nodes' delay -> priority
        priority_list[node] = op_time[tree[node][0]]  # operation time
    for level in range(level_count-2,0,-1):          # no priority for level 0 so ditch it and all max level nodes are output nodes
        for node in leveled_tree[level].keys():
            if(out_list[node] != []):             # Output of one expression can be node in other expression
                delay = op_time[leveled_tree[level][node][0]]
                priority_list[node] = max([priority_list[fanout] for fanout in out_list[node]]) + delay
    return priority_list
        

        
        
#-------------------------------------------------------------------------------------------------  
"""  
5. List Scheduling from Tree

    * Generate scheduled output for operations defined from tree
    
    * Inputs : Tree, Leveled tree, Priority for each operation, ALU count from user
        -User_ALU_count is maximum number of ALUs that user can afford in design
        -Different types of algos can be used to generate priority lists. 
        
    * Outputs : Schedule, Total time of execution, Final number of ALUs used, Upper limit of required number of ALUs
        - Final number of ALUs used : 
            + As AALUs are one of the most bulky components in unnit we must try to minimize 
              ALU count while aming for maximum computation speed
            + Final number ALUs used may be less that or equal to ALU count specified by user
        - Upper limit of required number of ALUs : 
            + Execution time is least if each opeartion is performed as soon as
              all the inputs for that opeartion are available. This may require more ALUs than specified
            + Uppper limit of required number of ALUs is determined by considering all operations of same execution time and 
              counting maximum number of ALUs required in each time step
            + This can be also viewed as maximum number of processing nodes in each level of tree
            
    * Algo :
    
        Upper limit of ALU count  = max(len(level in leveled tree))  # Maximum number of simultenious operations
        repeat untill all opeartions are scheduled 
            for each ALU 
                if ALU was busy in previous cycle 
                    If opeartion is complete free ALU and mark opeartion as done
                    Else reduce required time by one
            if current level is done upgrade currrent level
            Find candidates (whose all inputs are processed) (using leveled tree saves traversing time as schedule advances)
            For each Free ALU
                assign candidate with highest priority
                upadte current cycle record
                if all candidates are assigned then exit from loop
            Append current cycle to schedule
            increment current cycle count
        Count number of ALUs actually used 
           
"""
#-------------------------------------------------------------------------------------------------

def ls_from_tree(tree,leveled_tree,priority_list,user_alu_count):
    ls = []                                 # schedule list
    task_count = len(tree)                     # number of operations 
    done_count = 0
    #print(task_count)
    
    #-------------------------
    # get and define some vars
    # -------------------------    
    level_count = len(leveled_tree)    
    # done flags 
    done_flag = {node : False for node in tree.keys()} # indicate if opeartion is done
    for node in leveled_tree[0].keys():           # level 0 nodes already are processed
        done_flag[node] = True
        done_count = done_count+1
        
    #-----------------    
    #decide alu_count
    #-----------------
    max_alu_count  = 0  
    alu_count_for_max_speed = max([len(leveled_tree[level]) for level in range(1,level_count,1)]) # this is upper limit to alu_count
    
    alu_count = None
    if(user_alu_count >= alu_count_for_max_speed):
        alu_count = alu_count_for_max_speed
    else:
        alu_count = user_alu_count
    #print(alu_count)
    #alu_count = user_alu_count 
    
    #-----------------    
    # scheduling loop
    #-----------------
    alu_status = [0 for i in range(alu_count)]     # required cycle time to complete operation for each ALU
    curr_done_level = 0
    ls = []
    curr_time = 0
    
    while done_count < task_count:
        curr_cycle_alu_work = {}
        curr_cycle_alu_names = []
        curr_process = []
        curr_alu_count = 0
        #--------------------
        # Update ALU status
        #--------------------
        for alu in range(alu_count):
            if(alu_status[alu] != 0):               # if alu was busy in previous cycle
                if(alu_status[alu] == 1):           # alu has done work
                    alu_status[alu] = 0            # Escape Plan
                    done_count = done_count+1
                else:
                    alu_status[alu] = alu_status[alu] - 1   # decrease required cycle count
                    curr_cycle_alu_work[alu] =  [ element for element in ls[curr_time-1][alu]]      # To copy by value
                    curr_cycle_alu_work[alu][2] = alu_status[alu]
                    curr_cycle_alu_names.append(alu)
                    curr_alu_count = curr_alu_count+1
                    curr_process.append(curr_cycle_alu_work[alu][1])
        
        #-------------------
        # Update done Level 
        #-------------------
        done_level_upgrade = True                   
        if curr_done_level+1 < level_count:
            for node in leveled_tree[curr_done_level+1].keys():
                done_level_upgrade = done_level_upgrade and done_flag[node]     
            if(done_level_upgrade):                     # if all noed in level are processed
                curr_done_level = curr_done_level +1      # Upgrade done level
        
        #-----------------
        # find candidates
        #-----------------
        candidates = []           
        for level in range(curr_done_level+1,level_count,1):
            for node in leveled_tree[level].keys():
                if(not done_flag[node]):        # node not processed
                    childs_processed = True     # if ready to process
                    for child in tree[node][1]:
                        childs_processed = childs_processed and done_flag[child] and (child not in curr_process)
                        
                    if(childs_processed):
                        candidates.append(node)
                        
        #print(candidates)
        
        #---------------------------
        # Assign Candidates to ALUs
        #---------------------------
        for alu in range(alu_count):
            if candidates == []:
                break
            if(alu_status[alu] == 0):            # free alu
                max_priority = 0
                selected = None
                del_index = None
                for index in range(len(candidates)):                 # find candidate with maximum priority
                    if(priority_list[candidates[index]] > max_priority):
                        max_priority = priority_list[candidates[index]]
                        selected = candidates[index]
                        del_index = index
                if(selected == None):                           # something went wrorg
                    print("blah blah")
                    return None
                operation = tree[selected][0]                     # update current cycle
                done_flag[selected] = True
                required_time = op_time[operation]                 # Just to copy by value 
                alu_status[alu] = required_time
                curr_cycle_alu_work[alu] = [operation,selected,required_time]
                curr_cycle_alu_names.append(alu)
                curr_alu_count = curr_alu_count+1
                candidates.pop(del_index)
                curr_process.append(selected)
        
        #print(curr_cycle_alu_work)        
        ls.append(curr_cycle_alu_work)
        curr_time = curr_time+1
        #print(curr_time-1,ls[curr_time-1])
        #if(curr_time == 100):
        #    break
        
    #---------------------
    # calculate alu_count
    #---------------------
    ls.pop()                # remove empty state because of do-while loop
    curr_time = curr_time-1    # get exact time also because of do-while loop 
    max_alu_count = max([len(ls[t]) for t in range(curr_time)]) 
    
    return [ls,curr_time,max_alu_count,alu_count_for_max_speed]   


    
    

    
#--------------------------------------------------------------------------------------------------
"""
6. Are Identical Nodes

    * Return if nodes are logically identical 
    * Current version can't identify all the logically identical nodes
    * Major part of future Work

    * Inputs : Nodes
    * Output : Boolean saying is nodes are logicalli identical
""" 
#--------------------------------------------------------------------------------------------------
def are_identical_nodes(node1,node2):
    if(node1[0] != node2[0]):  # operator different
        return False
    if(node1[0] not in commutative_op):      # not commutative_opertor
        if(node1[1] == node2[1]):          # same opearnd
            return True
        else:
            return False
    if(set(node1[1]) == set(node2[1])):     # operator commutative and operands are same -> same node
        return True
    else:
        return False
        
       


       
#--------------------------------------------------------------------------------------------------
"""
7. Remove Identiacl Nodes from tree

    * Removes logically identical nodes from tree and regenerate tree, leveled tree, Fanout 
      List and also modify Output nodes list accordingly
    * Useful to remove common nodes in combined trees and help to reduce hardware as well as execution time

    * Inputs : Leveld Tree, Tree, Fanout lists, Output nodes list 
    * Output : Leveld Tree, Tree, Fanout lists
    
    * Algo :
    
        For each level in leveled tree 
            for each node in level
                If tree is not visited 
                    select tree
                    for all remaining unvisited nodes in same level 
                        if node is identical to selected node
                            for each parent in Fanout list of node change update corresponding child to selected node
                            delete node from leveled tree
        rebuild tree and Fanout list                    
"""    
#--------------------------------------------------------------------------------------------------

def remove_identical_nodes(leveled_tree,out_list,tree,output_list):
    
    for level in range(len(leveled_tree)):             # traverse each level
        node_list = list(leveled_tree[level].keys())     # get list of all nodes 
        node_num = len(node_list)
        visited = [False for node in range(node_num)]   # set visited to false
        for j in range(node_num):
            if(not visited[j]):
                visited[j] = True                  # different node
                curr_node_val = leveled_tree[level][node_list[j]]
                curr_node_name = node_list[j]
                #-----------------------
                # find identical noddes
                #-----------------------
                for k in range(j+1,node_num,1):
                    if(not visited[k]):
                        if (are_identical_nodes(leveled_tree[level][node_list[k]],curr_node_val)):  
                            visited[k] = True       # node is visited and deleated
                            for upper_level_node in out_list[node_list[k]]:
                                node_level = tree[upper_level_node][2]
                                #----------------
                                # update parents
                                #----------------
                                for child in range(len(leveled_tree[node_level][upper_level_node][1])):
                                    if leveled_tree[node_level][upper_level_node][1][child] == node_list[k] :
                                        leveled_tree[node_level][upper_level_node][1][child] = curr_node_name
                            #---------------------------
                            # update Output nodes' list
                            #---------------------------
                            if(node_list[k] in output_list):
                                for x in range(len(output_list)):
                                    if(output_list[x] == node_list[k]):
                                        output_list[x] = curr_node_name
                                        break
                                        
                            del leveled_tree[level][node_list[k]]       # delete node
                            #del out_list[node_list[k]]
    #------------------------------
    # Rebuild Tree and Fanout list
    #------------------------------
    tree = {}
    for i in range(len(leveled_tree)):
        tree.update(leveled_tree[i])
    out_list = get_out_list(tree) 
    
    return [tree,leveled_tree,out_list]







    
#--------------------------------------------------------------------------------------------------
"""
8. Variable Life With Time

    * Generate Lists of all active variables at current time state
    * Also gives list of variables to be killed 
    * variable is useless if all its fanouts are calculated and it is not in output list

    * every var is generated in last cycle of its generartion
        i.e. suppose addition operation takes 2 cycles, then register which will be holding var will 
        be connnected to out of computing ALU in last cycle to satisfy setup time requirements of register
    * variable will perish after all the processes depending on it are completed   
        i.e. after their out var comes to existance + 1 cycle
    * computation starts with first clock cycle's rising edge ands all inputs also latch in regs
        so we don't need inputs to be constant during entire execution
        System can work with ready-ready protocall
    * Registers can be reused after death of corresponding variable     
        
    * Inputs : Schedule, Time Required, Leveled tree, Fanout Lists, Output Variables
    * Outputs : Active Variable List at each time cycle, List of Variables to be killed at each time cycle
    
    * Algo :
        Assign all input variable to cycle at t = 0 
        for t from 1 to last time cycle
            copy all variables from previous cycle to current cycle
            If variable in current cycle is dead (All outputs are processed)
                if variable not in output list delete it and add it to death list
            add newly added variables from processes to current cycle list
            update life list and death list with current variables
   
"""
#--------------------------------------------------------------------------------------------------
def variable_life_time(schedule,time,tree,leveled_tree,out_list,output_list):
    life_of_pi = [[] for i in range(time)]            # Life list for variables
    death_note = {node: False for node in tree.keys()}  # Process done Flags
    death_time = [[] for t in range(time)]            # Death time list  
    #--------------------------------------
    # Add inputs to variable list at t = 0
    #--------------------------------------
    for inp in leveled_tree[0].keys():
        life_of_pi[0].append(inp)                   # inputs are active from first rising edge
    active_alu = list(schedule[0].keys())
    #print("\nactive alu")
    #print(active_alu)
    for process in active_alu:
        if (schedule[0][process][2] == 1): # output ready in first cycle
            life_of_pi[0].append(schedule[0][process][1])
    #-----------
    # for t > 0
    #-----------
    for t in range(1,time,1):                      # t = 0 is already processed
        tmp_life = [var for var in life_of_pi[t-1]]
        curr_process = schedule[t]
        #------------------
        # remove dead vars
        #------------------
        for node in life_of_pi[t-1]:
            var_dead = True
            #print(node)
            for fan_out in out_list[node] :
                var_dead = var_dead and death_note[fan_out]
            if(var_dead):
                if(node not in output_list):        # No one can kill output
                    death_time[t].append(node)
                    tmp_life.remove(node)           # update death list
        #------------------------        
        # add newly created vars
        #------------------------
        active_alu = list(curr_process.keys())
        for process in active_alu:
            if(curr_process[process][2] == 1):      # out ready
                tmp_life.append(curr_process[process][1])
                death_note[curr_process[process][1]] = True
        #------------------
        # update life list
        #------------------
        life_of_pi[t] = tmp_life
        
    return [life_of_pi,death_time]




    
#--------------------------------------------------------------------------------------------------
"""
9. Binding 

    * Generate hardware binding list and some other stuffs
    * Inputs : Schedule, Time Required, Life of variables, ALU Count, Register count, Leveled tree
             Tree, Death times, Output nodes

    * Outputs :

        1. Bound List : 
            Binding solution indiactiong connection between registers, ALUs, Inputs and Outputs at every time step
            Format is explained data structures section at starting of file
            
        2. Store : 
            List of variables held by each register at each time step
            Stored in List of Lists format
            [[reg0,reg1,..for each reg...],...for each time instance.....]
            
        3. ALU In :
            List of all possible input registers for each ALU input
            Stored in list of list of list format
            [[[input0_ALU0],[input1_ALU0]],[[input0_ALU1],[input1_ALU1]],..for each ALU...]
            
        4. Reg In :
            List of all possible input registers for each register
            Stored in list of list format
            Inputs are indicated directly by their names
            
        5. Input List :
            List of all input variables with indices as address of coresponding input register
        
        6. Out Locations :
            Dictionary holding output register address for each output node 
        
        7. Var Address :
            Dictionary holding address of register where particular variable was stored
            
    * Algo
        
        for all input variable
            assign register and update register in list
            update register store
            set register as busy
            
         for each time step
            if (t > 0) copy previous store to current stote
            free registers holding dead variables
            
            for every process in current cycle
                add input variavle's register's address to ALU in
                if execution is in last cycle 
                    assign free register to output     *#*
                    add alu out to reg in list
                    set register busy
                    
                    if process is in output list
                        add it to output locations
            
         for each alu
            remove repeated elements in alu in
                
         for each register 
            remove repeated elements in reg in
        
    *#* First priority is given to register which is already in opuput list of ALU
        This will help to reduce number of inputs at each register
        
    *** Future 
        * Second level of scheduling can be done to reduce size of muxes at inputs of ALUs
        
"""    
#--------------------------------------------------------------------------------------------------

def binding(schedule,time,life_of_var,alu_count,reg_count,leveled_tree,tree,death_time,output_list):
    #-----------------------------------
    # generate variable as None or empty
    #-----------------------------------
    alu_in = [[[],[]] for alu in range(alu_count)]
    reg_in  = [[] for reg in range(reg_count)]
    var_names = list(tree.keys())
    var_address = {var: None for var in var_names}
    bound_list = [{} for t in range(time)]
    reg_busy = [False for reg in range(reg_count)]
    store = [[None for reg in range(reg_count)] for t in range(time)]
    input_list = list(leveled_tree[0].keys())
    level_count = len(leveled_tree)
    out_locations = {output_node: None for output_node in output_list}
    
    #---------------------------
    # Assign Inputs to registers
    #---------------------------
    i = 0
    for ins in input_list:   # blah blah with inputs
        reg_in[i].append(ins)
        var_address[ins] = i
        reg_busy[i] = True
        store[0][i] = ins
        i = i+1
        
    #---------------
    # Building Loop
    #---------------
    for t in range(time):
        curr_binding = {}
        if (t>0) :
            store[t] = [val for val in store[t-1]]
        #------------------------
        # Remove dead variables
        #------------------------
        for var in death_time[t]:                       # send dead vars to heaven
            #print(var,t)
            reg_busy[var_address[var]] = False
        #---------------------------------------
        # Update binding according to processes 
        #---------------------------------------
        for process in schedule[t].keys():
            operation = schedule[t][process][0]
            process_node = schedule[t][process][1]
            curr_alu_in = [var_address[inp] for inp in tree[process_node][1]]
            if(len(curr_alu_in) == 1):
                curr_alu_in.append(curr_alu_in[0])
            curr_alu_out = []
            #-----------------------------
            # if process is in last state
            #-----------------------------
            if schedule[t][process][2] == 1 :         # last cycle of op ->enable out
                assign_reg = None                  # first try to find reg already in out put
                for reg in range(reg_count):
                    if(not reg_busy[reg]):
                        if(process in reg_in[reg]):
                            assign_reg = reg
                            break
                            
                if(assign_reg == None):             # if non such var is there find other
                    for reg in range(reg_count):
                        if(not reg_busy[reg]):
                            assign_reg = reg
                            break
                
                if(assign_reg == None):
                    print("\n\nRegister not found\n")
                    return None
                #------------------------
                # Assign Output register
                #-------------------------
                reg_busy[assign_reg] = True    
                reg_in[assign_reg].append(process)
                curr_alu_out.append(assign_reg)
                var_address[process_node] = assign_reg
                #print(process," assigned to reg ",assign_reg)
                store[t][assign_reg] = process_node
                
                if(process_node in output_list):                # if output variable then add reg to output address
                    out_locations[process_node] = assign_reg
            #---------------------------
            # Update Alu In and Binding
            #---------------------------
            for num in range(len(curr_alu_in)):
                alu_in[process][num].append(curr_alu_in[num])
            
            curr_binding[process] = [operation,process_node,curr_alu_in,curr_alu_out]
            
        bound_list[t] = curr_binding
    
    #--------------------------
    # Remove repeated entries
    #--------------------------
    for alu in range(alu_count):
        alu_in[alu][0] = list(set(alu_in[alu][0]))
        alu_in[alu][1] = list(set(alu_in[alu][1]))
        
    for reg in range(reg_count):
        reg_in[reg] = list(set(reg_in[reg]))
        
    return [bound_list,store,alu_in,reg_in,input_list,out_locations,var_address]




    
#--------------------------------------------------------------------------------------------------
"""
10. Get Combined Tree from Infix Expressions

    * Inputs : List of infix expressions
    * Outputs : Combined tree, combined leveled tree, oputput node list for each expression

    * Steps
        1. for all given infix expressions generate tree, leveled tree, parents
        2. Combine all leveled trees using {combine_leveled_trees_with_signle_parent(leveled_trees)}
        3. Generate combined tree from combined leveled tree
    
"""
#--------------------------------------------------------------------------------------------------
def get_combined_trees(infix_inputs):
    num_of_trees = len(infix_inputs)
    output_list = []
    leveled_trees = []
    for i in range(num_of_trees):                     # generate trres and leveled trees for each expression
        postfix = infix2postfix(infix_inputs[i])
        #print(postfix)
        tree = None
        parent = None
        [tree,parent] = postfix2bdt(postfix,(str(i)+"n"))
        #print(tree)
        leveled_tree = get_leveled_tree(tree,parent)
        output_list.append(parent)
        leveled_trees.append(leveled_tree)
        
    combined_leveled_tree = combine_leveled_trees_with_signle_parent(leveled_trees) # generate combined leveled tree
    combined_tree = {}
    for i in range(len(combined_leveled_tree)):             # generate combined tree
        combined_tree.update(combined_leveled_tree[i])
        
    return [combined_tree,combined_leveled_tree,output_list]







#--------------------------------------------------------------------------------------------------
"""
11. Schedule and Bind 

    * Fuction takes list of infix expressions and generate scheduling and hardware binding solutions for them
      to be implemented in same unit
      
    * Just a cover function

    * Inputs : List of infix expressions, Maximum number of ALU units user can afford on hardware

    * Outputs : 
        1. Leveled Tree       : Combined Leveled tree for all expressions 
        2. Priority List      : Priority list of all execution nodes in combined tree of all expressions
        3. Scheduling         : Output of scheduling function (Format explained in Data Structures section)
        4. Life               : List of active variables at each time cycle
        5. Bound List         : Hardware binding of resisters, ALUs, inputs and outputs at each time step (Format in Data Structures Section)
        6. Store              : List of contents of each register at each time cycle
        7. Time               : Total execution time of set of expressions
        8. ALU count          : Number of ALUs used in scheduling and binding
        9. Reg count          : Number of registers used in binding
        10.Limit of ALU count : Max possibel number of required ALUs to get minimum execution time
        11.ALU in             : List of all possible input registers for each ALU
        12.Reg In             : List of all possible input variable inputs anf ALU outputs that can be assigned to Register
        13.Input List         : List of all input variables ordered by address of variable holding registre
        14.Output List        : List of output nodes of each expression
        15.Out Locations      : Dictionary of output nodes as keys and output holding register's address as value
        16.Var Address        : Dictionary for all variables holding address of register where it was/ is stored
    
"""
#--------------------------------------------------------------------------------------------------        
def schedule_and_bind(infix_inputs,user_alu_count):
    #print(infix_inputs)
    [tree,leveled_tree,output_list] = get_combined_trees(infix_inputs)
    out_list = get_out_list(tree)    # fanout list
    [tree,leveled_tree,out_list] = remove_identical_nodes(leveled_tree,out_list,tree,output_list)
    
    # print("\nLeveled Tree")
    # for level in range(len(leveled_tree)):
        # print(level," : ",leveled_tree[level])
    
    # print("\nOut_list")
    # print(out_list)
    
    # print("\ntree")
    # print(tree)
    
    # print("\nOutput_list")
    # print(output_list)
    
    priority_list = get_priority_list(tree,leveled_tree,out_list,output_list)
    
    # print("\nPriority List")
    # print(priority_list)
    
    [schedule,time,alu_count,upper_limit_alu_count] = ls_from_tree(tree,leveled_tree,priority_list,user_alu_count)
    
    # print("\nSchedule")
    # for t in range(time):
        # print(t," : ",schedule[t])
        
    # print("\n Alu Count : ",alu_count," Alu for mx speed : ",upper_limit_alu_count)
    
    [life,death_time] = variable_life_time(schedule,time,tree,leveled_tree,out_list,output_list)
    reg_count = max([len(t) for t in life])
    
    # print("\n Reg Count : ",reg_count)
    [bound_list,store,alu_in,reg_in,input_list,out_locations,var_address] = binding(schedule,time,life,alu_count,reg_count,leveled_tree,tree,death_time,output_list) 
    
    # print("\nBound List   : Store\n")
    # for t in range(time):
        # print(t," : ",bound_list[t]," : ",store[t])
    #print("\nALU in list")
    #for alu in range(alu_count):
    #    print(alu," : ",alu_in[alu])
    # print("\nReg In list")
    # for reg in range(reg_count):
        # print(reg," : ",reg_in[reg])
    # print("\nInput List : ",input_list)
    # print("\nOut List : ",output_list)
    # print("\n Out locations : ",out_locations)
    #print("----------------------------------------------------------------------------------------------------\n")
    return [leveled_tree,priority_list,schedule,life,bound_list,store,time,alu_count,reg_count,upper_limit_alu_count,alu_in,reg_in,input_list,output_list,out_locations,var_address]
#--------------------------------------------------------------------------------------------------    
