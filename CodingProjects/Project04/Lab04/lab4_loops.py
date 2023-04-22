'''lecture_15_loops.py
Review two ways to loop thru a list
Oliver W. Layton
CS 151: Computational Thinking: Visual Media
Fall 2021
'''

myList = ['a', 'b', 'c']

# Method 1
for letter in myList:
    print(letter)

print('Done!')

# Method 2
for i in range(len(myList)):
    print(myList[i])
print('Done!')