'''test_drawString.py
Tests both the Lsystem and TurtleInterpreter classes.
L-system files, distance, and angles are passed in by command-line arguments
Oliver W. Layton
CS151: Computational Thinking: Visual Media
Fall 2020
'''
import sys
import lsystem
import turtle_interpreter as ti


def main(args):

    if len(args) < 4:
        print('Usage: python3 test_drawString.py <L-system filename> <distance> <angle>')
        exit()
    filename = args[1]
    dist = float(args[2])
    angle = float(args[3])

    lsys = lsystem.Lsystem(filename=filename)

    nIter = 2
    lsysString = lsys.buildString(nIter)

    terp = ti.TurtleInterpreter(width=800, height=800, bgColor='white')
    terp.setColor('purple')
    terp.setWidth(2)

    terp.drawString(lsysString, dist, angle)
    terp.hold()


if __name__ == '__main__':
    main(sys.argv)
