# Title        : Genrate Text File to Show Binding Result
# Developed by : Yogesh Mahajan (y.mahajan456@gmail.com)    (14D070022 @ IITB EE)
#                OV Shashank    (shashank[at]ee.iitb.ac.in) (14D070021 @ IITB EE)
#                Avineil Jain   (avineil96[at]ee.iitb.ac.in)(14D170002 @ IITB EE)   

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

def gen_binging_text(file_name,binding):
    f = open(file_name+".txt",'w')
    [leveled_tree,priority_list,schedule,life,bound_list,store,time,alu_count,reg_count,upper_limit_alu_count,alu_in,reg_in,input_list,output_list,out_locations,var_address] = binding
    
    f.write("_____________________Binding Result___________________________\n")
    f.write("\nLeveled Tree")
    for level in range(len(leveled_tree)):
        f.write(str(level)+" : "+str(leveled_tree[level])+"\n")

    f.write("\nOutput_list")
    f.write(str(output_list)+"\n")

    f.write("\nPriority List")
    f.write(str(priority_list))

    f.write("\nSchedule")
    for t in range(time):
        f.write(str(t)+" : "+str(schedule[t])+"\n")
        
    f.write("\n Alu Count : "+str(alu_count)+" Alu for mx speed : "+str(upper_limit_alu_count)+"\n")

    f.write("\nBound List   : Store\n")
    for t in range(time):
        f.write(str(t)+" : "+str(bound_list[t])+" : "+str(store[t])+"\n")
    f.write("\nALU in list")
    for alu in range(alu_count):
        f.write(str(alu)+" : "+str(alu_in[alu])+"\n")
    f.write("\nReg In list")
    for reg in range(reg_count):
        f.write(str(reg)+" : "+str(reg_in[reg])+"\n")
    f.write("\nInput List : "+str(input_list))
    f.write("\nOut List : "+str(output_list))
    f.write("\n Out locations : "+str(out_locations))


    f.write("\n f.write Var Addresses: \n")
    for var in var_address.keys():
        f.write(str(var) +" : "+str(var_address[var])+"\n")
        
    f.write("\nlife is\n")
    for l in range(len(life)):
        f.write(str(l)+" "+str(life[l])+"\n")
    f.close()