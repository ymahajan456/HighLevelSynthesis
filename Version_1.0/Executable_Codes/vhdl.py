# Title:        VHDL Classes
# Developed by : Yogesh Mahajan (y.mahajan456@gmail.com)    (14D070022 @ IITB EE)
#                OV Shashank    (shashank[at]ee.iitb.ac.in) (14D070021 @ IITB EE)
#                Avineil Jain   (avineil96[at]ee.iitb.ac.in)(14D170002 @ IITB EE)   
# Description:  This file contains several class to make data handling easy

from copy import copy
from copy import deepcopy

# Note: In the following code all strings are maintained as lists
#       with each element representing a new line. Finally the join method
#       along with \n is used to create the printable version

library = {
    "ieee":"LIBRARY IEEE;", 
    "numeric": "USE ieee.numeric_std.all;", 
    "std_logic": "USE ieee.std_logic_1164.all;", 
    "work":"LIBRARY work;","math":"USE ieee.math_real.all;"
    }

'''
The Following class stores objects of type std_logic and
also its vector form and provides methods for easy
utilisation and manipulation
'''
class std_logic:
    allowed_symbols = ['0','1','Z','U','X','W','L','H','-']     # Allowed symbols in std_logic
    
    '''
    Checks if the value or the default value is valid or not
    based on the allowed symbols
    '''
    def valid(self):
        if self.is_value:
            for val in self.value:
                if not val.upper() in std_logic.allowed_symbols:
                    return False
        else:
            for val in self.default:
                if not val.upper() in self.default:
                    return False
        return True
        
    '''
    Constructor
    Inputs: name, length, type="", default = [] for objects
        or value, length for static values
    name - string; length - integer, type - string, default - string; value - string
    Incase of invalid inputs it deletes self
    '''
    def __init__(self, *args):          
        self.vector = (args[1] != 0)
        if not self.vector:
            self.length = 1 
        else:
            self.length = args[1]
        self.value = 0
        if (args[0].isdigit()):
            self.is_value = True
            self.value = list(args[0])
        else:
            self.name = args[0]
            self.default = []
            if len(args)>3 and isinstance(self.length,int):
                self.default = list(args[3])
            self.is_value = False
            self.type = ""
            if len(args)>2:
                self.type = args[2]
        if isinstance(self.length,int) and ((not (self.valid())) or ((not self.is_value) and 
                                             self.default and (not self.length == len(self.default))) or 
                                            (self.is_value and (not self.length == len(self.value)))):
            exit("Invalid Default or Value! Exiting.")

    '''
    Method to convert to a string representation as in VHDL
    '''
    def __str__(self):
        if self.is_value:
            string = '"' + "".join(self.value) + '"'
        else:
            if not self.type == "":
                string = self.name + ": " + self.type + " "
            else:
                string = self.name + ": "
            string += "STD_LOGIC"
            if self.vector:
                string += "_VECTOR" 
                if isinstance(self.length, int):
                    string += "( 0 TO " + str(self.length - 1) + " )"
                else:
                    string += "( 0 TO " + str(self.length) +" - 1)"
                if self.default:
                    string += ' := "' + "".join(self.default) + '"'
                else:
                    string += " := (others => '0')"
            else:
                if self.default:
                    string += " := '" + "".join(self.default) + "'"
                else:
                    string += " := '0'" 
        return string

    '''
    Checks if self is equal to other is all respects 
    other than the name
    '''
    def __eq__(self, other):
        if(isinstance(other, std_logic)):
            return (self.length == other.length and self.is_value == other.is_value and self.default == other.default and
                    self.type == other.type and self.value == other.value and self.vector == other.vector)
        else:
            return False

    '''
    Copy Constructor
    Returns a new copy of self
    '''
    def __copy__(self):
        if(self.vector):
            length = self.length
        else:
            length = 0
        if(self.is_value):
            new_copy = std_logic(self.value, length)
        else:
            new_copy = std_logic(self.name, length, self.type, self.default)
        return new_copy
   

'''
The Following class stores objects of type integer
and provides methods for easy utilisation and manipulation
'''
 
class integers:
    '''
    Constructor
    Inputs: name, type="", default = [] for objects
        or value for static values
    name - string; type - string, default - integer; value - integer
    Incase of invalid inputs it deletes self
    '''
    def __init__(self, *args):          #name, type="", default = 0
        if (args[0].isdigit()):
            self.is_value = True
            self.value = args[0]
        else:
            self.name = args[0]
            if len(args)>2:
                self.default = args[2]
            else:
                self.default = 0
            self.is_value = False
            self.value = 0
            self.type = ""
            if len(args)>1:
                self.type = args[1]
        if not ((self.is_value and isinstance(value,int)) or (not(self.is_value) and (self.default,int))):
            del(self)

    '''
    Method to convert to a string representation as in VHDL
    '''
    def __str__(self):
        if self.is_value:
            string = str(self.value)
        else:
            if not self.type == "":
                string = self.name + ": " + self.type + " "
            else:
                string = self.name + ": "
            string += "INTEGER " 
            string += ' := ' + str(self.default)
        return string

    '''
    Copy Constructor
    Returns a new copy of self
    '''
    def __copy__(self):
        if(self.is_value):
            new_copy = integers(self.value)
        else:
            new_copy = integers(self.name, self.type, self.default)
        return new_copy

    '''
    Checks if self is equal to other is all respects 
    other than the name
    '''
    def __eq__(self, other):
        if(isinstance(other, integers)):
            return (self.is_value == other.is_value and self.default == other.default and
                    self.type == other.type and self.value == other.value)
        else:
            return False

'''
Class to hold a vhdl entity and its architecture
It provides various mathods to make the creation
of a VHDL code for the particular component pretty easy
'''
class vhdl_component:

    '''
    Constructor
    Inputs: name - string (Name of the component)
            ports - list of std_logic or integer types
                (Ports of the component)
            [generic] - list of integer types
                (Generic ports of the component)
    '''
    def __init__(self, name, ports, generic = []):
        self.name = name
        self.ports = deepcopy(ports)
        self.generic = deepcopy(generic)
        self.instance = 0

    '''
    Method to store the architecture
    Sort of redundant
    '''
    def store_architecture(self, architecture):
        self.architecture = architecture

    '''
    Returns a string containing the entity
    For the format of the string refer to the note
    at the beggining of this code
    '''
    def create_entity(self):
        string = ["ENTITY " + self.name + " IS"]
        generic = self.generic
        ports = self.ports
        if generic:
            string.append("\tGENERIC(")
            for gen in generic:
                string.append("\t\t" + str(gen) + ";")
            string[len(string)-1] = "\t\t" + str(generic[len(generic)-1]) + ");"

        string.append("\tPORT(")
        for port in ports:
            string.append("\t\t" + str(port) + ";")
        string[len(string)-1] = "\t\t" + str(ports[len(ports)-1]) + ");"
        string.append("END ENTITY;")
        return string

    '''
    Returns a string containing the component
    For the format of the string refer to the note
    at the beggining of this code
    '''
    def create_component(self):
        string = ["COMPONENT " + self.name + " IS"]
        generic = self.generic
        ports = self.ports
        if generic:
            string.append("\tGENERIC(")
            for gen in generic:
                string.append("\t\t" + str(gen) + ";")
            string[len(string)-1] = "\t\t" + str(generic[len(generic)-1]) + ");"

        string.append("\tPORT(")
        for port in ports:
            string.append("\t\t" + str(port) + ";")
        string[len(string)-1] = "\t\t" + str(ports[len(ports)-1]) + ");"
        string.append("END COMPONENT;")
        return string

    '''
    Returns a string containing an instance
    For the format of the string refer to the note
    at the beggining of this code.

    If no name is provided, the name is auto_generated 
    based on the instance count which is maintained by the class

    Also the port maps are also auto-generated if the generic_name and
    port_name are not provided, else the names from there lists are used
    They are supposed to be list of strings and must exactly match
    the generic and port maps, otherwise an exception would occur
    '''
    def create_instance(self, name = [], generic_name = [], port_name = []):
        to_return = []
        generic = self.generic
        ports = self.ports

        if not name:
            name = self.name + str(self.instance)
        string = [name + ": " + self.name]
        if generic:
            string.append("\tGENERIC MAP(")
            for i in range(len(generic)):
                if (generic_name):
                    to_append = "\t\t" + generic[i].name + " => " + generic_name[i]
                else:
                    to_append = "\t\t" + generic[i].name + " => " + generic[i].name + "_" + name
                    self_copy = copy(generic[i])
                    self_copy.name = generic[i].name + "_" + name
                    self_copy.type = ""
                    to_return.append(self_copy)
                if i == len(generic) - 1:
                    string.append(to_append)
                    string.append("\t)")
                else:
                    to_append += ","
                    string.append(to_append)
        string.append("\tPORT MAP(")
        for i in range(len(ports)):
            if (port_name):
                to_append = "\t\t" + ports[i].name + " => " + port_name[i]
            else:
                to_append = "\t\t" + ports[i].name + " => " + ports[i].name + "_" + name
                self_copy = copy(ports[i])
                self_copy.name = ports[i].name + "_" + name
                self_copy.type = ""
                to_return.append(self_copy)
            if i == len(ports) - 1:
                string.append(to_append)
                string.append("\t);")
            else:
                to_append += ","
                string.append(to_append)
        self.instance += 1
        return [string, to_return]
    
    '''
    This creates a string which completes the entire component
    The libraries that might be required must be provided as a
    list of strings which are the keys in the library dictionary
    as defined above.

    Again the format of the string returned is as mentioned
    in the note at the start of the code.
    '''
    def create_complete(self, libraries = ["ieee", "numeric", "std_logic"]):
        string = [library[i] for i in libraries] + [""] + \
            self.create_entity() + [""] + self.architecture
        return string
