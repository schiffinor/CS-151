'''test_set_get.py
Tests the L-system class (Lsystem) set and get methods
Oliver W. Layton
CS151: Computational Thinking: Visual Media
Fall 2020
'''
import lsystem


def test_all():
    # Make a new lsystem
    lsys = lsystem.Lsystem()

    # Test out your set and getBase
    print('Test 1 Base Str:')
    lsys.setBase('X')
    baseStr = lsys.getBase()
    print(f'Your base string is {baseStr} and it should be X.')
    print('\nTest 2 Base Str:')
    lsys.setBase('F-F')
    baseStr = lsys.getBase()
    print(f'Your base string is {baseStr} and it should be F-F.')

    # Test out adding and getting your rules
    print('\nTest 3 One Rule:')
    lsys.addRule(['F', 'FF'])
    rule0 = lsys.getRule(0)
    print(f"Your rule is {rule0} and it should be ['F', 'FF'].")
    print('\nTest 4 Two Rules:')
    lsys.addRule(['X', 'F[+XL][-XL]FXL'])
    rule0 = lsys.getRule(0)
    rule1 = lsys.getRule(1)
    print(f"Your 1st rule is {rule0} and it should be ['F', 'FF'].")
    print(f"Your 2nd rule is {rule1} and it should be ['X', 'F[+XL][-XL]FXL'].")

    # Test out finding number of rules
    print('\nTest 5 Number of rules:')
    print(f'Number of rules is {lsys.numRules()} and should be 2.')
    print('\nTest 6 Number of rules:')
    lsys.addRule(['A', 'ABC'])
    print(f'Number of rules is {lsys.numRules()} and should be 3.')


if __name__ == "__main__":
    test_all()
