f = open('test.txt','w')

import random
rm = 2**14

for i in range(1):
    for j in range(4):
        for k in range(4):
            for l in range(4):
                
                a = i*(rm) + random.randint(0,rm)
                b = j*(rm) + random.randint(0,rm)
                c = k*(rm) + random.randint(0,rm)
                d = l*(rm) + random.randint(0,rm)
                
                a_str = bin(a)[2:].zfill(16)
                b_str = bin(b)[2:].zfill(16)
                c_str = bin(c)[2:].zfill(16)
                d_str = bin(d)[2:].zfill(16)
                
                out0 = (a+b)+(c+d)
                out1 = (a+b)^(c+d)+(rm*4-(a+b+1))
                out2 = (a+b)&(c+d)|(a^b)+(c|d)
                
                print(str(out0) , " " , str(out1) , " " , str(out2))
                
               
                if(out1<0):
				    out1 = 2**16 + out1
				                
                out0_str = bin(out0)[2:].zfill(40)
                out1_str = bin(out1)[2:].zfill(40)
                out2_str = bin(out2)[2:].zfill(40)
                print(out0_str, " ",out1_str," ",out2_str)
                out0_str = out0_str[-16:]
                out1_str = out1_str[-16:]
                out2_str = out2_str[-16:]
                print(out0_str, " ",out1_str," ",out2_str)
                f.write(a_str + " " + b_str + " " + c_str + " " + d_str + " " + out0_str + " " + out1_str + " " + out2_str + "\n");
f.close()
                
    
