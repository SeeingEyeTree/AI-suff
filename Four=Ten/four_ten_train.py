
'''
first 4 numbers are the numbers that are being used
4th index [4] is addtion if 1 == True if 0 == False
[5] subtraction
[6] multiplication
[7] division
[8] parantheses
'''
A=11
S=12
M=13
D=14
P=15
NA=16
#1-10 , 16-
problems_training_data=[
[1,2,3,4,1,1,1,1,1],
[2,5,0,3,1,1,1,1,1],
[1,1,1,7,1,1,1,1,1],
[1,1,3,7,1,1,1,1,1],
[1,2,3,9,1,1,1,1,1],
[1,9,5,6,1,1,1,1,1],,
[3,1,8,5,1,1,1,1,1],
[6,9,1,7,1,1,1,1,1],
[0,6,4,1,1,1,1,0,1],
[1,5,4,9,1,1,1,0,1],
[6,5,3,1,1,1,1,1,1],
[4,0,3,7,1,1,1,1,1],
[4,5,0,8,1,1,1,1,1],
[4,2,1,1,1,1,1,1,1],
[7,2,1,2,1,1,1,1,1],
[2,1,4,9,1,1,1,1,1],
[6,5,1,1,1,1,1,1,1],
[9,7,1,5,1,1,1,1,1],
[3,2,3,7,1,1,1,1,1],
[3,4,2,9,1,1,1,1,1],
[8,7,5,6,1,1,1,1,1],
[0,1,4,5,1,1,1,1,1],
[2,0,2,6,1,1,1,1,1],
[1,2,9,2,1,1,1,1,1],
[1,4,7,2,1,1,1,1,1],
[3,1,3,4,1,1,1,1,1],
[8,3,6,1,1,1,1,1,1],
[2,5,7,9,1,1,1,1,1],
[2,7,4,3,1,1,1,1,1],
[3,6,9,3,1,1,1,1,1],
[4,9,5,8,1,1,1,1,1],
[6,7,4,6,1,1,1,1,1],
[0,6,2,6,1,1,1,1,1],
[3,0,8,7,1,1,1,1,1],
[8,8,4,1,1,1,1,1,1],
[3,2,3,6,1,1,1,1,1],
[8,9,6,2,1,1,1,1,1],
[3,3,5,4,1,1,1,1,1],
[3,3,7,9,1,1,1,1,1],
[4,5,5,4,1,1,1,1,1],
[9,5,9,5,1,1,1,1,1],
[7,5,3,0,1,1,1,1,1],
[3,7,2,1,1,1,1,1,1],
[6,6,2,3,1,1,1,1,1]

            ]

solutions_traning_data=[
[1,A,2,A,3,A,4,NA,NA],
[2,M,5,A,3,M,0,NA,NA],
[1,A,1,M,1,A,7,NA,NA],
[7,A,3,M,1,M,1,NA,NA],
[1,M,3,S,2,A,9,NA,NA],
[9,A,1,M,6,S,5,NA,NA],
[1,M,P,5,S,3,P,A,8],
[9,S,6,M,1,A,7,NA,NA],
[6,A,4,A,0,M,1,NA,NA],
[1,M,5,S,4,A,9,NA,NA],
[5,M,3,A,1,S,6,NA,NA],
[4,M,0,A,3,A,7,NA,NA],
[0,A,5,M,P,8,D,4,P],
[4,M,2,A,1,A,1,NA,NA],
[7,A,2,S,1,A,2,NA,NA],
[1,M,2,M,P,9,S,4,P],
[6,A,5,M,1,S,1,NA,NA],
[9,A,7,S,5,S,1,NA,NA],
[3,M,P,3,S,2,P,A,7],
[3,S,4,D,2,A,9,NA,NA],
[5,S,P,8,S,7,P,A,6],
[0,A,1,A,4,A,5,NA,NA],
[2,A,0,A,2,A,6,NA,NA],
[1,M,2,D,2,A,9,NA,NA],
[4,S,2,A,1,A,7,NA,NA],
[3,M,1,A,3,A,4,NA,NA],
[8,A,6,S,3,S,1,NA,NA],
[2,M,7,S,P,9,S,5,P],
[4,A,7,S,3,D,3,NA,NA],
[9,A,6,D,P,3,A,3,P],
[9,S,8,A,5,A,4,NA,NA],
[4,A,5,M,P,7,S,6,P],
[6,A,6,S,2,A,0,NA,NA],
[8,M,0,A,3,A,7,NA,NA],
[8,A,8,D,2,M,1,NA,NA],
[6,A,3,S,2,A,3,NA,NA],
[9,M,8,D,6,S,2,NA,NA],
[3,D,3,A,5,A,4,NA,NA],
[9,S,3,A,7,S,3,NA,NA],
[4,D,4,M,5,A,5,NA,NA],
[9,D,9,M,5,A,5,NA,NA],
[7,A,3,A,5,M,0,NA,NA],
[3,A,7,M,P,2,S,1,P]

                                                                                               
            ]

def countx(passedlis,x):
    count=0
    for i in passedlis:
        if i == x:
            count+=1
    return count


simplfied=[]

for i in solutions_traning_data:
    solution=[]
    for x in i:
        if x == A:
           solution.append(0) 
        elif x == M:
            solution.append(1)
        elif x == S:
            solution.append(2)
        elif x == D:
            solution.append(3)
        elif x == P:
            solution.append(4)
    simplfied.append(solution)
for_ai=[]

for i in simplfied:
    holder=[]
    if countx(i, 4)==0:
        if countx(i, 0)==3:
            holder.append(0)
            #All add
        elif countx(i,0)==2 and countx(i,1)==1:
            holder.append(1)
            #2 add on mulityp
        elif countx(i,1)==2 and countx(i,0)==1:
            holder.append(3)
            #2 multpy add 1
        elif countx(i,1)==1 and countx(i,2)==1 and countx(i,0)==1:
            holder.append(4)
            # multipy 1, add, 1, subtract 1
        elif countx(i,0)==2 and countx(i,2)==1:
            holder.append(5)
            #2 add 1 subtraction
        elif countx(i,0)==1 and countx(i,2)==2:
            holder.append(6)
            #1 add, 2 subtracion
        elif countx(i,2)==1 and countx(i,3)==1 and countx(i,0)==1:
            holder.append(7)
            #1 add, dev, sub
        elif countx(i,1)==1 and countx(i,3)==1 and countx(i,0)==1:
            holder.append(8)
            # 1 mult 1 dev 1 add
        else:
            holder.append(f'addpat {i}')
    else:
        holder.append(9)
    for_ai.append(holder)
print(for_ai)
