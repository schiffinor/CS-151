import better_shape_lib as sl
import turtle as t
import math as m
import random as r
'''
surreal.py Roman Schiffino 151B Fall Semester
This is my project file.
It basically is a basic 3d renderer/3d point modeler. Now with animation. 
'''


def surreal():
    '''
    Ok this basically calls the main composition from the better shape library. However, the twist here is that it also enables the animation.
    To use the animation just press space once the window is first drawn. It can be run as many times as you'd like.
    It also runs faster on better computers.
    '''
    #This makes it so that my keypress thingy works right. To be quite honest I'm not entirely sure why it doesn't work without all the extra bells and whistles but haha we don't talk abt that.
    screen = t.Screen()
    #Ultimate speed.
    t.tracer(False)
    sl.composition_fella()
    t.hideturtle()
    sl.wall()
    sl.windowpane(0,0,100,250,125,"#f8f3ed",0,0,0)
    t.update()
    #PRESS SPACE PLEASE :)
    #Either way this is the user input animation thingy.
    screen.onkeypress(sl.windowOpen,'space')
    screen.listen()
    t.update()
    t.exitonclick()


surreal()