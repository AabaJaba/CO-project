import sys
sys.tracebacklimit=0
var=[];lab={};hltcount=0;varcount=0;actualcount=0;regop={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"};instructions=["var","add","sub","mov","ld","st","mul","div","rs","ls","xor","or","and","not","cmp","jmp","jgt","je","addf","subf","movf","hlt","FLAGS"]
inst=[x.rstrip("\n").split() for x in sys.stdin.readlines()]
flgchck=list(regop.keys())
flgchck.remove('FLAGS') 
templist=[x for x in inst if x!=[]]
def typea(i):
    assert len(i)==4, f'Error in line {inst.index(i)}: This instruction must contain 3 arguments, not {len(i)-1}'# invalid instruction length 
    assert i[1] in regop.keys() and i[2] in regop.keys() and i[3] in regop.keys(), f'Error in line {inst.index(i)}: Enter Valid register values'
    i[1]=regop[i[1]]
    i[2]=regop[i[2]]
    i[3]=regop[i[3]]         
    i.insert(1,'00')
def typeb(i):
    assert len(i)==3, f'Error in line {inst.index(i)}: This instruction must contain 2 arguments, not {len(i)-1}'# invalid instruction length 
    assert i[1] in regop.keys(), f'Error in line {inst.index(i)}: Enter valid register values'
    i[1]=regop[i[1]]
    i[2]=i[2].lstrip('$')
    assert i[2].isdigit(), f'Error in line {inst.index(i)}: Imm must be a whole number, whereas Imm = {i[2]}' #float error
    assert 0<=int(i[2])<=255, f'Error in line {inst.index(i)}: Imm must lie between 0-255, whereas Imm = {i[2]}' #over 8bit error
    i[2]=bin(int(i[2]))[2:]
    i[2]=('0'*(8-len(i[2]))) + i[2]
def typec(i):
    assert len(i)==3, f'Error in line {inst.index(i)}: This instruction must contain 2 arguments, not {len(i)-1}'#invalid instruction length
    assert i[1] in regop.keys() and i[2] in regop.keys(), f'Error in line {inst.index(i)}: Enter Valid register values'#invalid register values
    i[1]=regop[i[1]]
    i[2]=regop[i[2]]
    i.insert(1,'00000')
def typed(i):
    assert len(i)==3, f'Error in line {inst.index(i)}: This instruction must contain 2 arguments, not {len(i)-1}'#invalid instruction length
    assert i[1] in regop.keys(), f'Error in line {inst.index(i)}: Enter Valid Register Values'
    i[1]=regop[i[1]]
    assert i[2] not in lab.keys(), f'Error in line {inst.index(i)}: Use of labels in place of variables is forbidden'#label instead of variable
    assert i[2] in var, f'Error in line {inst.index(i)}: "{i[2]}" has not been defined'#var not declared
    i[2]=bin(int((len(templist)-len(var))+(var.index(i[2]))))[2:]
    i[2]=('0'*(8-len(i[2]))) + i[2]
def typee(i):
    assert len(i)==2, f'Error in line {inst.index(i)}: This instruction must contain 1 arguments, not {len(i)-1}'#invalid instruction length
    assert i[1] not in var, f'Error in line {inst.index(i)}: Use of variables in place of labels is forbidden'#variable instead of label
    assert i[1] in lab.keys(), f'Error in line {inst.index(i)}: "{i[1]}" has not been defined'#label not declared
    i[1]=bin(lab[i[1]])[2:]
    i[1]=('0'*(11-len(i[1]))) + i[1] 
for i in range(len((inst))):
    if inst[i]==[]:
        varcount+=1
        continue
    else:
        actualcount+=1
    if inst[i][0]=='var':
        assert len(inst[i])==2, f"Error in line {i}:This instruction can't contain more than one argument" #more than 1 argument 
        assert inst[i][1] not in instructions, f'Error in line{i}: "{inst[i][0]}" is an invalid var name, var names can not be same as instructions' #var name can't be same as instruction name
        assert varcount==i, "All variables must be defined at the start of the code"#var defined between code
        assert inst[i][1] not in var, f"Error in line {i}: Can't redefine a variable"#var redefine
        var.append(inst[i][1])
        varcount+=1
varcount=0
actualcount=0
for i in range(len((inst))):
    if inst[i]==[]:
        varcount+=1
        continue
    else:
        actualcount+=1
    if len(inst[i])>=2:
        assert inst[i][1]!=":", f'Error in line {i}: label cannot contain spaces' #label has spaces error
    if inst[i][0][-1]==":":#lables
        assert len(inst[i])>1, f'Error in line {i}: label is empty'#empty label error 
        inst[i][0]=inst[i][0].rstrip(":")
        assert inst[i][0] not in instructions, f'Error in line {i}: "{inst[i][0]}" is an invalid label name, label names can not be same as instructions' #label name can't be same as instruction name
        assert inst[i][0] not in lab.keys(), f"Error in line {i}: Can't redefine a label"#label redefine 
        assert inst[i][1]!="var", f"Error in line {i}:Can't label the line in which variables are defined"#labeled var def line  
        assert inst[i][0] not in var, f"Error in line{i}: Can't use variable name as label name" #var name as label 
        lab[inst[i].pop(0)]=actualcount-1-len(var)
varcount=0
actualcount=0
for i in range(len((inst))):
    if inst[i]==[]:
        varcount+=1
        continue
    else:
        actualcount+=1
    if 'FLAGS' in inst[i]:#flags
        assert inst[i][0]=='mov' and inst[i][2] in flgchck and inst[i][1]=='FLAGS', f'Error in line {i}: Invalid use of FLAGS register'#invalid flag use
    if inst[i][0]=='add':
        inst[i][0]='10000'
        typea(inst[i])
    elif inst[i][0]=='sub':
        inst[i][0]='10001'
        typea(inst[i])
    elif inst[i][0]=='mov' and inst[i][2][0]=='$':
        inst[i][0]='10010'
        typeb(inst[i])
    elif inst[i][0]=='mov' and inst[i][2]:
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
    elif inst[i][0]=='hlt': 
        assert hltcount==0, f'Error in line {i}:"hlt" must be used only once'  
        assert "hlt" in templist[-1], f'Error in line {i}:"hlt" must be the last instruction'
        hltcount+=1
        inst[i][0]='0101000000000000'
    elif inst[i][0] not in instructions:
            assert False, f'Error in line {i}: Invalid Argument'
assert hltcount!=0, '"hlt" instruction is absent'
inst=[x for x in inst if x!=[]]
assert actualcount<=256, "Instruction input can't be greater than 256 lines" #greater than 256 lines input
inst=[x for x in inst if x[0]!='var']#removing var from list
for x in inst:
    print(*x,sep='')
