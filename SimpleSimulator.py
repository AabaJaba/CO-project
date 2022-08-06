import sys
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
while PC<c:
    i=inst[PC]
    if i[:5]=='10000':#add-A
        reg[i[13:16]]=reg[i[7:10]]+reg[i[10:13]]   
        if reg[i[13:16]]>65536:
            reg[i[13:16]]=65536
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
        reg[i[5:8]]=int(i[8:16],2)
        prt()
        PC+=1 
    elif i[:5]=='10011':#movReg-C
        if reg[i[7:10]]=='111':
            reg[i[13:16]]='000000000000'+reg['FLAG']
        else:
            reg[i[13:16]]=reg[i[7:10]]
        prt()
        PC+=1 
    elif i[:5]=='10100':#load-D
        
        reg[i[5:8]]=int(inst[int(str(i[8:16]),2)],2)
        prt()
        PC+=1 
    elif i[:5]=='10101':#store-D
        inst[int(str(i[8:16]),2)]='0'*(16-len(bin(reg[i[5:8]])[2:]))+bin(reg[i[5:8]])[2:]
        prt()
        PC+=1 
    elif i[:5]=='10110':#mul-A
        reg[i[13:16]]=reg[i[7:10]]*reg[i[10:13]]   
        if reg[i[13:16]]>65536:
            reg[i[13:16]]=65536
            reg['FLAG']='1'+reg['FLAG'][1:]
        prt()
        PC+=1 
    elif i[:5]=='10111':#div-C
        reg['000']=reg[i[10:13]]/reg[i[13:16]]
        reg['001']=reg[i[10:13]]%reg[i[13:16]]
        prt()
        PC+=1 
    elif i[:5]=='11000':#rs-B
        reg[i[5:8]]=int(bin(reg[i[5:8]])[:2][:-int(i[8:16],2)],2)
        prt()
        PC+=1 
    elif i[:5]=='11001':#ls-B
        reg[i[5:8]]=int(bin(reg[i[5:8]])[:2]+'0'*int(i[8:16],2),2)
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
        reg[i[13:16]]=int(''.join(['1' if x=='0' else '0' for x in str(bin(reg[i[10:13]])[2:])]),2)
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
            prt()
            PC=int(i[8:16],2)
        else:
            reg['FLAG']='0000'
            prt()
            PC+=1
        reg['FLAG']='0000'
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
            prt()
            PC=int(i[8:16],2)
        else:
            reg['FLAG']='0000'
            prt()
            PC+=1
        reg['FLAG']='0000'
    elif i[:5]=='01010':#hlt
        prt()
        break
        
for x in inst:
    print(x)
