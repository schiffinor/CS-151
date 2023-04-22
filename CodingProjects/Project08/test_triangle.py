'''test_triangle.py
Tests the TurtleInterpreter class by instructing it to draw a blue, thick, triangle
Oliver W. Layton
CS151: Computational Thinking: Visual Media
Fall 2020
'''
import turtle_interpreter as ti


def test_triangle():

    terp = ti.TurtleInterpreter(width=800, height=800, bgColor='white')
    terp.setColor('blue')
    terp.setWidth(10)
    terp.goto(-200, -200, 60)

    print('The screen height / width is:')
    print(str(terp.getScreenHeight()), '/', str(terp.getScreenWidth()))
    print('and should be')
    print('800 / 800')

    lsysString = 'F++F++F'
    dist = 200
    angle = 60
    terp.drawString(lsysString, dist, angle)
    terp.hold()


if __name__ == '__main__':
    test_triangle()
