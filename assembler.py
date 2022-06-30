regop={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
with open("g:/My Drive/code/CO project/test.txt","r") as f:#open txt file
    inst=[x.rstrip("\n").split() for x in f.readlines()]
inst=[x for x in inst if x!=[]] #remove empty lines
def typea(i):
    i[1]=regop[i[1]]
    i[2]=regop[i[2]]
    i[3]=regop[i[3]]         
    i.insert(1,'00')
def typeb(i):
    i[1]=regop[i[1]]
    i[2]=float(i[2].lstrip('$'))
    i[2]=bin(int(i[2]))[2:]
    i[2]=('0'*(8-len(i[2]))) + i[2]
def typec(i):
    i[1]=regop[i[1]]
    i[2]=regop[i[2]]
    i.insert(1,'00000')
def typed(i):
    i[1]=regop[i[1]]
    i[2]=bin(inst.index(i)+1)[2:]
    i[2]=('0'*(8-len(i[2]))) + i[2]
def typee(i):
    i[1]=bin(inst.index(i)+1)[2:]
    i[1]=('0'*(11-len(i[1]))) + i[1] 
hltcount=0
for i in inst:
    if i[0]=='var':
        continue    
    elif i[0]=='add':
        i[0]='10000'
        typea(i)
    elif i[0]=='sub':
        i[0]='10001'
        typea(i)
    elif i[0]=='mov' and i[2][0]=='$':
        i[0]='10010'
        typeb(i)
    elif i[0]=='mov' and i[2] in regop.keys():
        i[0]='10011'
        typec(i)
    elif i[0]=='ld':
        i[0]='10100'
        typed(i)
    elif i[0]=='st':
        i[0]='10101'
        typed(i)
    elif i[0]=='mul':
        i[0]='10110'
        typea(i)
    elif i[0]=='div':
        i[0]='10111'
        typec(i)
    elif i[0]=='rs':
        i[0]='11000'
        typeb(i)
    elif i[0]=='ls':
        i[0]='11001'
        typeb(i)
    elif i[0]=='xor':
        i[0]='11010'
        typea(i)
    elif i[0]=='or':
        i[0]='11011'
        typea(i)
    elif i[0]=='and':
        i[0]='11100'
        typea(i)
    elif i[0]=='not':
        i[0]='11101'
        typec(i)
    elif i[0]=='cmp':
        i[0]='11110'
        typec(i)
    elif i[0]=='jmp':
        i[0]='11111'
        typee(i)
    elif i[0]=='jlt':
        i[0]='01100'
        typee(i)
    elif i[0]=='jgt':
        i[0]='01101'
        typee(i)
    elif i[0]=='je':
        i[0]='01111'
        typee(i)
    elif i[0]=='hlt':
        hltcount+=1
        i[0]='0101000000000000'
    else:
        continue
inst=[x for x in inst if x[0]!='var']#removing var from list  
for x in inst:
    print(*x,sep='')


    






    










