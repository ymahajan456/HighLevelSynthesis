# Title : postfix to binary tree
# Developed by : Yogesh Mahajan (y.mahajan456@gmail.com)    (14D070022 @ IITB EE)
#                OV Shashank    (shashank[at]ee.iitb.ac.in) (14D070021 @ IITB EE)
#                Avineil Jain   (avineil96[at]ee.iitb.ac.in)(14D170002 @ IITB EE)   
# Description : Convert postfix expression to binary expression tree
#--------------------------------------------------------------------------------------------------
from stack import Stack

class Op_Node:
    childs_count = 0
    childs = []             #just names of child nodes
    level = None
    
    def __init__(self):
       self.name = None
       
    def __init__(self,name,*vars):
        self.name = name
        if(len(vars) > 0):
            self.childs = vars[0]
            self.childs_count = len(vars[0])
            
    def __str__(self):
        return str([self.name,self.childs,self.level])
        
    def node_obj2list(self):
        return [self.name,self.childs,self.level]
#---------------------------------------------------------------------------------------------------                
# Operand count of operators not having 2 operands 
ns_operand_count = {}       # ns for non standard -> not having 2 operands
ns_operand_count['!'] = 1

op_list = ['@','%','*','/','+','-','!','&','^','|']

ns_op = list(ns_operand_count.keys())
#--------------------------------------------------------------------------------------------------
def postfix2bdt(postfix,prefix = 'n'):
    tmp_stack = Stack()
    node_list = {}
    node_names = []
    for token in postfix:
        if(token not in op_list):
            if(token not in node_names):
                new_var = Op_Node(token)
                new_var.level = 0
                node_names.append(token)
                node_list[token] = new_var
                
            tmp_stack.push(token)
            
        else:
            operands_list = []
            if(token in ns_op):
                for i in range(ns_operand_count[token]):
                    new_operand_node_name = tmp_stack.pop()
                    if(new_operand_node_name != None):
                        operands_list.append(new_operand_node_name)
                    else:
                        print("\nNumber of operands mismatch for operator : ", token,"\n")
                        return None
            else:
                for i in range(2):
                    new_operand = tmp_stack.pop()
                    if(new_operand != None):
                        operands_list.append(new_operand)
                    else:
                        print("\nNumber of operands mismatch for operator : ", token,"\n")
                        return None
                        
            level_count = 0
            for child in operands_list:
                if(level_count < node_list[child].level):
                    level_count = node_list[child].level
                    
            node_name = prefix+str(len(node_names))
            node_names.append(node_name)
            
            new_op_node = Op_Node(token,operands_list)
            new_op_node.level = level_count+1
            
            node_list[node_name] = new_op_node
            tmp_stack.push(node_name)
            
    bt = {node:node_list[node].node_obj2list() for node in node_names}
    
    parent_node = tmp_stack.pop()
    return [bt,parent_node]
#--------------------------------------------------------------------------------------------------

