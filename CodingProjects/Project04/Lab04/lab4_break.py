'''lecture_15_break.py
Use the break keyword to get out of a loop prematurely
Oliver W. Layton
CS 151: Computational Thinking: Visual Media
Fall 2021
'''
for i in range(10):
    print('i =', i)

    if i == 5:
        break
print('Done!')
