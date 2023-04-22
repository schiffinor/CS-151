'''test_buildString.py
Tests the L-system class with the Koch snowflake L-system (systemKoch.txt).
Focuses on buildString and L-system iterations
Oliver W. Layton
CS151: Computational Thinking: Visual Media
Fall 2020
'''
import lsystem


def testKoch():
    print('Testing replace and buildString with systemKoch.txt...')

    filename = 'systemKoch.txt'

    try:
        f = open(filename, 'r')
        f.close()
    except FileNotFoundError:
        print('Could not find', filename, '. Is it in your lab folder?')
        exit()

    lsys = lsystem.Lsystem(filename=filename)

    print('--------------------------')
    nIter = 0
    lstr = lsys.buildString(nIter)
    print('Your L-system string after', nIter, 'iterations:\n', lstr)
    print('It should be:\n', 'F++F++F')
    print('--------------------------')

    print('--------------------------')
    nIter = 1
    lstr = lsys.buildString(nIter)
    print('Your L-system string after', nIter, 'iterations:\n', lstr)
    print('It should be:\n', 'F-F++F-F++F-F++F-F++F-F++F-F')
    print('--------------------------')

    print('--------------------------')
    nIter = 2
    lstr = lsys.buildString(nIter)
    print('Your L-system string after', nIter, 'iterations:\n', lstr)
    print('It should be:\n', ' F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F++F-F++F-F' +
          '-F-F++F-F++F-F++F-F-F-F++F-F++F-F++F-F-F-F++F-F', sep='')
    print('--------------------------')

    print('--------------------------')
    nIter = 3
    lstr = lsys.buildString(nIter)
    print('The length of L-system string after', nIter, 'iterations:\n', len(lstr))
    print('It should be:\n', ' ' + str(448), sep='')
    print('--------------------------')


if __name__ == "__main__":
    testKoch()
