'''test_read.py
Tests the L-system class (Lsystem) read method with the following L-systems:
- systemKoch.txt (one rule)
- systemC.txt (two rules)
Oliver W. Layton
CS151: Computational Thinking: Visual Media
Fall 2020
'''
import lsystem


def testKoch():
    print('Testing systemKoch.txt...')

    filename = 'systemKoch.txt'

    try:
        f = open(filename, 'r')
        f.close()
    except FileNotFoundError:
        print('Could not find', filename, '. Is it in your lab folder?')
        exit()

    lsys = lsystem.Lsystem(filename=filename)

    print('Your base string is\n', lsys.getBase(), 'and it should be\n F++F++F')
    print('There is', lsys.numRules(), 'rules and there should be 1')
    rule = lsys.getRule(0)
    print('Your rule is\n', rule, ' and should be\n [\'F\', \'F-F++F-F\']')

    print('\nTesting out your set methods...')
    print('Trying to set the base string with F++F...')
    lsys.setBase('F++F')
    print('Your base string is\n', lsys.getBase(), 'and it should be\n F++F')
    print('Trying to add the rule [+, -]...')
    lsys.addRule(['+', '-'])
    print('There are', lsys.numRules(), 'rules and there should be 2')
    rule1 = lsys.getRule(0)
    rule2 = lsys.getRule(1)
    print('Your 1st rule is\n', rule1, ' and should be\n [\'F\', \'F-F++F-F\']')
    print('Your 2nd rule is\n', rule2, ' and should be\n [\'+\', \'-\']')


def testC():
    print('Testing systemC.txt...')

    filename = 'systemC.txt'

    try:
        f = open(filename, 'r')
        f.close()
    except FileNotFoundError:
        print('Could not find', filename, '. Is it in your lab folder?')
        exit()

    lsys = lsystem.Lsystem()
    lsys.read(filename)

    print('Your base string is\n', lsys.getBase(), 'and it should be\n X')
    print('There are', lsys.numRules(), 'rules and there should be 2')
    rule1 = lsys.getRule(0)
    rule2 = lsys.getRule(1)
    print('Your 1st rule is\n', rule1, ' and should be\n [\'X\', \'F[+XL][-XL]FXL\']')
    print('Your 2nd rule is\n', rule2, ' and should be\n [\'F\', \'FF\']')


if __name__ == '__main__':
    print('----------------------------------------------------------')
    testKoch()
    print('----------------------------------------------------------')
    testC()
