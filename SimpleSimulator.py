import sys
import matplotlib.pyplot as plt
inst=[x.rstrip("\n") for x in sys.stdin.readlines()]
c=len(inst)
for i in range(256-c):
    inst.append("0"*16)
def prt():
    temp=list(reg.values())[:-1]
    temp=['0'*(16-len(bin(x)[2:]))+bin(x)[2:] for x in temp]
    print(f'{"0"*(8-len(bin(PC)[2:]))+bin(PC)[2:]} {" ".join(temp)} 000000000000{list(reg.values())[-1]}')
    return
PC=0
n=0
var={}
reg={"000": 0, "001": 0, "010": 0, "011": 0, "100": 0, "101": 0, "110": 0, "FLAG": "0000"}
clk=0
while PC<c:
    plt.plot(clk,PC,'bo')
    i=inst[PC]
    if i[:5]=='10000':#add-A
        reg[i[13:16]]=reg[i[7:10]]+reg[i[10:13]]   
        if reg[i[13:16]]>65535:
            reg[i[13:16]]%=65536
            reg['FLAG']='1'+reg['FLAG'][1:]
        prt()
        PC+=1 
    elif i[:5]=='10001':#sub-A
        reg[i[13:16]]=reg[i[7:10]]-reg[i[10:13]]   
        if reg[i[13:16]]<0:
            reg[i[13:16]]=0
            reg['FLAG']='1'+reg['FLAG'][1:]
        prt()
        PC+=1 
    elif i[:5]=='10010':#movImm-B
        reg['FLAG']='0000'
        reg[i[5:8]]=int(i[8:16],2)
        prt()
        PC+=1 
    elif i[:5]=='10011':#movReg-C
        if i[10:13]=='111':
            reg[i[13:16]]=int(('000000000000'+reg['FLAG']),2)
        else:
            
            reg[i[13:16]]=reg[i[10:13]]
        reg['FLAG']='0000'
        prt()
        PC+=1 
    elif i[:5]=='10100':#load-D
        reg[i[5:8]]=int(inst[int(str(i[8:16]),2)],2) 
        plt.plot(clk,int(str(i[8:16]),2),'bo')
        prt()
        PC+=1 
    elif i[:5]=='10101':#store-D
        inst[int(str(i[8:16]),2)]='0'*(16-len(bin(reg[i[5:8]])[2:]))+bin(reg[i[5:8]])[2:]
        plt.plot(clk,int(str(i[8:16]),2),'bo')
        prt()
        PC+=1 
    elif i[:5]=='10110':#mul-A
        reg[i[13:16]]=reg[i[7:10]]*reg[i[10:13]]   
        if reg[i[13:16]]>65535:
            reg[i[13:16]]%=65536
            reg['FLAG']='1'+reg['FLAG'][1:]
        prt()
        PC+=1 
    elif i[:5]=='10111':#div-C
        reg['000']=reg[i[10:13]]//reg[i[13:16]]
        reg['001']=reg[i[10:13]]%reg[i[13:16]]
        prt()
        PC+=1 
    elif i[:5]=='11000':#rs-B
        reg[i[5:8]]//=2**int(i[8:16],2)
        prt()
        PC+=1 
    elif i[:5]=='11001':#ls-B
        reg[i[5:8]]*=2**int(i[8:16],2)
        prt()
        PC+=1 
    elif i[:5]=='11010':#XOR-A
        reg[i[13:16]]=reg[i[7:10]]^reg[i[10:13]]
        prt()
        PC+=1 
    elif i[:5]=='11011':#OR-A
        reg[i[13:16]]=reg[i[7:10]]|reg[i[10:13]]
        prt()
        PC+=1 
    elif i[:5]=='11100':#AND-A
        reg[i[13:16]]=reg[i[7:10]]&reg[i[10:13]]
        prt()
        PC+=1 
    elif i[:5]=='11101':#invert-C
        #reg[i[13:16]]=int(''.join(['1' if x=='0' else '0' for x in str(bin(reg[i[10:13]])[2:])]),2)
        reg[i[13:16]]=(2**16-1)^(reg[i[10:13]])
        prt()
        PC+=1 
    elif i[:5]=='11110':#cmp-C
        if reg[i[10:13]]<reg[i[13:16]]:
            reg['FLAG']=reg['FLAG'][:1]+'1'+reg['FLAG'][2:]
        elif reg[i[10:13]]>reg[i[13:16]]:
            reg['FLAG']=reg['FLAG'][:2]+'1'+reg['FLAG'][-1]
        elif reg[i[10:13]]==reg[i[13:16]]:
            reg['FLAG']=reg['FLAG'][:3]+'1'
        prt()
        PC+=1 
    elif i[:5]=='11111':#uncon_jmp-E
        prt()
        PC=int(i[8:16],2)
        reg['FLAG']='0000'
    elif i[:5]=='01100':#jlt-E
        if reg['FLAG'][1]=='1':
            reg['FLAG']='0000'
            prt()
            PC=int(i[8:16],2)
        else:
            reg['FLAG']='0000'
            prt()
            PC+=1
        
    elif i[:5]=='01101':#jgt-E
        if reg['FLAG'][2]=='1':
            reg['FLAG']='0000'
            prt()
            PC=int(i[8:16],2)
        else:
            reg['FLAG']='0000'
            prt()
            PC+=1
    elif i[:5]=='01111':#je-E
        if reg['FLAG'][3]=='1':
            reg['FLAG']='0000'
            prt()
            PC=int(i[8:16],2)
        else:
            reg['FLAG']='0000'
            prt()
            PC+=1
        
    elif i[:5]=='01010':#hlt
        reg['FLAG']='0000'
        prt()
        break
    else:
        PC+=1
    clk+=1
for x in inst:
    print(x)
#plt.show()

"""import math
flag=0
a=["-","K","M","G"] #to get exponent *10
bit={1:0,2:2,3:3,4:0} #bit to byte
Byte={1:-3,2:-1,3:0,4:0} #bit,nibble,byte

def query1(i,r,space,arr,type):
    num_exp=math.log(int(space[0]),2)
    #print(num_exp)
    for j in range(1,4):
        if(a[j]==space[1][0]):
            break
    if type==4:
        CPU=int(input('Enter CPU bits:'))
        num_itr=math.log(int(CPU),2)
        arr[4]=num_itr
    add_bit=int(num_exp+(j*10)-arr[type])    
    op_i=i-add_bit-r
    fill_bits=i-op_i-(2*r)
    print("Number of bits required for representing the address are :",add_bit)
    print("Number of opcode bits: ",op_i)
    print("Number of filler bits in Instruction type 2: ",fill_bits)
    print("Maximum number of instructions ISA can support:",2**op_i)
    print("Maximum number of registers ISA can support: ",2**r)


while(1):
    query=int(input("Enter 1 for query 1,2 for query 2 and 0 for exit: "))
    if(query==1):
        print("Enter the total memory space :")
        space=[j for j in input().split(" ")] #change
        print("\n1. Bit Addressable Memory \n2.Nibble Addressable Memory \n3.Byte Addressable Memory \n4.Word Addressable Memory")
        type=int(input("Enter memory type :\n"))     
        i=int(input("Enter the length of instruction in (bits):\n"))
        r=int(input("Enter the length of register (bits):\n"))
       
        if("b" in space[1][1]):
            query1(i,r,space,bit,type)
        elif("B" in space[1][1]):
           query1(i,r,space,Byte,type)
    elif(query==2):
        part=int(input("Type 1/Type 2: "))
        if(part==1):
            print("Enter the total memory space :")
            space=[j for j in input().split(" ")] #change
            print("\n1. Bit Addressable Memory \n2.Nibble Addressable Memory \n3.Byte Addressable Memory \n4.Word Addressable Memory")
            type=int(input("Enter memory type :\n"))
            change_type=int(input("Enter memory that needs to be changed to:\n"))
            CPU=int(input('Enter CPU bits:'))
            bit[4]=int(math.log(CPU,2))  
            Byte[4]=int(math.log(CPU,2))
            print(f'Number of pins saved/required: {bit[type]-bit[change_type]}')  

        if(part==2):
            CPU=int(input("Enter the bits of CPU: "))
            bit[4]=int(math.log(CPU,2))
            Byte[4]=int(math.log(CPU,2))
            addr_pins=int(input("Enter number of address pins: "))
            print("\n1. Bit Addressable Memory \n2.Nibble Addressable Memory \n3.Byte Addressable Memory \n4.Word Addressable Memory")
            type=int(input("Enter memory type :\n"))
            ans=addr_pins+bit[type]-3
            for j in range(1,4):
                if(ans//10==a[j]):
                    break
            print(f'The memory would be: {2**(ans-(j*10))} {a[j]}B')       
    elif(query==0):
        exit(0)"""




