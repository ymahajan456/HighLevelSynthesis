# Title        : Infix To Postfix
# Developed by : Yogesh Mahajan (y.mahajan456@gmail.com)    (14D070022 @ IITB EE)
#                OV Shashank    (shashank[at]ee.iitb.ac.in) (14D070021 @ IITB EE)
#                Avineil Jain   (avineil96[at]ee.iitb.ac.in)(14D170002 @ IITB EE)   
# Description  : Converts Infix notation to postfix notation 
#--------------------------------------------------------------------------------------------------

# Arithmatic Operators precedence and Associtivity directories
precedence = {}
precedence['@'] = 14    # exponent
precedence['*'] = 13    # mul
precedence['/'] = 13    # div
precedence['%'] = 13    # modulo
precedence['+'] = 12    # add
precedence['-'] = 12    # sub

# assoc = 1 -> right associtivity
assoc = {}
assoc['@'] = True
assoc['*'] = False
assoc['/'] = False
assoc['%'] = False
assoc['+'] = False
assoc['-'] = False
#---------------------
# Logical Operators precedence and Associtivity directories

precedence['!'] = 24     # NOT
precedence['&'] = 3     # AND
precedence['^'] = 3     # XOR
precedence['|'] = 3     # OR

# assoc = True -> right associtivity

assoc['!'] = True
assoc['&'] = False
assoc['^'] = False
assoc['|'] = False

precedence['('] = 1
assoc['('] = False

#--------------------------------------------------------------------------------------------------
from stack import Stack

op_list = list(precedence.keys())     # operator list
ban_list = [j for j in op_list]
ban_list.append(")")
#print("\n", op_list,"\n")
       # operator stack
#--------------------------------------------------------------------------------------------------
def get_var_string(inp,i):        # modify i in the name of i
    var_name = ""
    lent = len(inp)
    #print("\n",i)
    while((inp[i] not in ban_list)):
        var_name = var_name + str(inp[i])
        i = i + 1
        if(i == lent):
            break
    return [var_name,i-1]

#--------------------------------------------------------------------------------------------------        
def infix2postfix(inp):
    postfix = []        # output list
    op_stack = Stack()
    i = 0;
    #print(len(inp))
    while i < len(inp):
        token = inp[i]
        if (token not in ban_list):
            [var,i] = get_var_string(inp,i)
            postfix.append(var)
            #print(var)
            
        elif token == '(':
            op_stack.push(token)
            
        elif token == ')':
            balanced = False
            while not op_stack.is_empty():
                if(op_stack.peek() != '('):
                    postfix.append(op_stack.pop())
                else:
                    op_stack.pop()
                    balanced = True
                    break
            if(not balanced):
                print("\n Error: Unbalanced Paranthesis_1!\n")
                return None
        
        elif (token in op_list):
            if (not op_stack.is_empty()):
                temp = op_stack.peek()
                while (not op_stack.is_empty() and (((not assoc[token]) and (precedence[token] <= precedence[temp])) or ((assoc[token]) and (precedence[token] < precedence[temp])))):
                    postfix.append(op_stack.pop())
                    temp = op_stack.peek()
                    
            op_stack.push(token)
         
        else:
            print("\n Error: Unrecognisez code!\n")
            return None
            
        i = i+1

        
       
    while(not op_stack.is_empty()):
        if(op_stack.peek() == '('):
            print("\n Error: Unbalanced Paranthesis_2!\n")
            return None
        postfix.append(op_stack.pop())
        
    return postfix
#--------------------------------------------------------------------------------------------------    
    
#inp = str(inp("Enter\n"))
#inp = "a+b+c+d+e+f"
#pp = infix2postfix(inp)
#print("\n")
#print(pp)
