'''
Roman Schiffino assignment 2 lucas num.py
'''


#Initial values.
l = [2,1]
#List Addition
for i in range(2,101):
    li=l[i-1]+l[i-2]
    #Update list
    l.append(li)
    #Prints list placement and value.
    print(i,":",l[i])
sum = sum(l)
print("sum =",sum)