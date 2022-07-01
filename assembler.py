var=[];lab={};hltcount=0;varcount=0;regop={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
with open("CO project/test.txt","r") as f:#open txt file
    inst=[x.rstrip("\n").split() for x in f.readlines()]
inst=[x for x in inst if x!=[]] #remove empty lines
assert len(inst)<=256, "Instruction input can't be greater than 256 lines" #greater than 256 lines input
flgchck=list(regop.keys())
flgchck.remove('FLAGS') 
for x in inst:
    if 'FLAGS' in x:
        assert x[0]=='mov' and x[1] in flgchck and x[2]=='FLAGS', f'Error in line {inst.index(x)+1}: Invalid FLAGS register use'#invalid flag use
def typea(i):
    assert len(i)==4, f'Error in line {inst.index(i)+1}: This instruction must contain 3 arguments, not {len(i)-1}'# invalid instruction length 
    assert i[1] in regop.keys() and i[2] in regop.keys() and i[3] in regop.keys(), 'Enter Valid register values'
    i[1]=regop[i[1]]
    i[2]=regop[i[2]]
    i[3]=regop[i[3]]         
    i.insert(1,'00')
def typeb(i):
    assert len(i)==3, f'Error in line {inst.index(i)+1}: This instruction must contain 2 arguments, not {len(i)-1}'# invalid instruction length 
    assert i[1] in regop.keys(), 'Enter valid register values'
    i[1]=regop[i[1]]
    i[2]=i[2].lstrip('$')
    try:
        i[2]=float(i[2])
    except:
        print(f'Error in line {i}: Imm must be an integer, whereas Imm = {i[2]}')
    assert i[2].is_integer(), f'Error in line {i}: Imm must be a whole number, whereas Imm = {i[2]}' #float error
    assert 0<=i[2]<=255, f'Error in line {i}: Imm must lie between 0-255, whereas Imm = {i[2]}' #over 8bit error
    i[2]=bin(int(i[2]))[2:]
    i[2]=('0'*(8-len(i[2]))) + i[2]
def typec(i):
    assert len(i)==3, f'Error in line {inst.index(i)+1}: This instruction must contain 2 arguments, not {len(i)-1}'#invalid instruction length
    assert i[1] in regop.keys() and i[2] in regop.keys(), 'Enter Valid register values'#invalid register values
    i[1]=regop[i[1]]
    i[2]=regop[i[2]]
    i.insert(1,'00000')
def typed(i):
    assert len(i)==3, f'Error in line {inst.index(i)+1}: This instruction must contain 2 arguments, not {len(i)-1}'#invalid instruction length
    assert i[1] in regop.keys(), 'Enter Valid Register Values'
    i[1]=regop[i[1]]
    assert i[2] not in lab.keys(), f'Error in line {inst.index(i)+1}: Use of labels in place of variables is forbidden'#label instead of variable
    assert i[2] in var, f'Error in line {inst.index(i)+1}: "{i[2]}" has not been defined'#var not declared
    i[2]=bin(int((len(inst)-len(var))+(var.index(i[2]))))[2:]
    i[2]=('0'*(8-len(i[2]))) + i[2]
def typee(i):
    assert len(i)==2, f'Error in line {inst.index(i)+1}: This instruction must contain 1 arguments, not {len(i)-1}'#invalid instruction length
    assert i[1] not in var, f'Error in line {inst.index(i)+1}: Use of labels in place of variables is forbidden'#variable instead of label
    assert i[1] in lab.keys(), f'Error in line {inst.index(i)+1}: "{i[1]}" has not been defined'#label not declared
    i[1]=bin(lab[i[1]])[2:]
    i[1]=('0'*(11-len(i[1]))) + i[1] 
for i in range(len((inst))):#labels
    if inst[i][0][-1]==":":
        inst[i][0]=inst[i][0].rstrip(":")
        assert inst[i][0].isalnum() and not inst[i][0][0].isnumeric(), f'Error in line {i}: Invalid label name' #invalid label
        lab[inst[i].pop(0)]=i
        if len(inst[i])==0:#empty label
            inst[i].append("xx")
for i in range(len((inst))):
    if inst[i][0]=='var':
        assert len(inst[i])==2, f"Error in line {i}:This instruction can't contain more than one argument" #more than 1 argument 
        assert inst[i][1].isalnum() and not inst[i][1][0].isnumeric(), f'Error in line {i}: Invalid variable name' #invalid variable
        assert varcount==i, "All variables must be defined at the start of the code"#var defined between code
        assert inst[i][1] not in var, f"Error in line {i}: Can't redefine a variable"#var redefine
        var.append(inst[i][1])
        varcount+=1
    elif inst[i][0]=='add':
        inst[i][0]='10000'
        typea(inst[i])
    elif inst[i][0]=='sub':
        inst[i][0]='10001'
        typea(inst[i])
    elif inst[i][0]=='mov' and inst[i][2][0]=='$':
        inst[i][0]='10010'
        typeb(inst[i])
    elif inst[i][0]=='mov' and inst[i][2] in regop.keys():
        inst[i][0]='10011'
        typec(inst[i])
    elif inst[i][0]=='ld':
        inst[i][0]='10100'
        typed(inst[i])
    elif inst[i][0]=='st':
        inst[i][0]='10101'
        typed(inst[i])
    elif inst[i][0]=='mul':
        inst[i][0]='10110'
        typea(inst[i])
    elif inst[i][0]=='div':
        inst[i][0]='10111'
        typec(inst[i])
    elif inst[i][0]=='rs':
        inst[i][0]='11000'
        typeb(inst[i])
    elif inst[i][0]=='ls':
        inst[i][0]='11001'
        typeb(inst[i])
    elif inst[i][0]=='xor':
        inst[i][0]='11010'
        typea(inst[i])
    elif inst[i][0]=='or':
        inst[i][0]='11011'
        typea(inst[i])
    elif inst[i][0]=='and':
        inst[i][0]='11100'
        typea(inst[i])
    elif inst[i][0]=='not':
        inst[i][0]='11101'
        typec(inst[i])
    elif inst[i][0]=='cmp':
        inst[i][0]='11110'
        typec(inst[i])
    elif inst[i][0]=='jmp':
        inst[i][0]='11111'
        typee(inst[i])
    elif inst[i][0]=='jlt':
        inst[i][0]='01100'
        typee(inst[i])
    elif inst[i][0]=='jgt':
        inst[i][0]='01101'
        typee(inst[i])
    elif inst[i][0]=='je':
        inst[i][0]='01111'
        typee(inst[i])
    elif inst[i][0]=='addf':
        inst[i][0]=='00000'
        typea(inst[i])
    elif inst[i][0]=='subf':
        inst[i][0]=='00001'
        typea(inst[i])
    elif inst[i][0]=='movf':
        inst[i][0]=='00010'
        typeb(inst[i])
    elif inst[i][0]=='hlt':   
        assert i==len(inst)-1, f'Error in line {i}:"hlt" must be the last instruction'
        assert hltcount==0, f'Error in line {i}:"hlt" must be used only once'
        hltcount+=1
        inst[i][0]='0101000000000000'
    elif inst[i][0]=='xx':
        inst[i][0]="0000000000000000"
    else:
        assert False, f'Error in line {i}: Syntax error, "{"".join(inst[i])}" is not a valid argument'#invalid instruction
assert hltcount!=0, '"hlt" instruction is absent'
inst=[x for x in inst if x[0]!='var']#removing var from list
inst=["".join(x)+"\n" for x in inst]
result=open('CO project/result.txt','w')
result.writelines(inst)
