'''
lab5_snowman_animation.py
Roman Schiffino 151B Fall Semester
This is my 2nd lab file for project number 5 . 
It does what the lab ask me to do.
'''

import graphicsPlus as gr
import time as t
import random as r
import tkinter as tk

width = 1540
height = 870
# Creates empty list of shapes to be drawn.
shapeList = []


def snowman_init(x, y, scale):
    '''
    Creates and returns a list of Zelle Graphics objects to make up a snowman.
    Minimally, this is just three equal sized circles stack on top of each other
    with two smaller circles for the eyes

    Parameters:
    -----------
    x: int. x coordinate for the top circle center.
    y: int. y coordinate for the top circle center.
    scale: float. Scaled size of the snowman.

    Returns:
    -----------
    list with 5 Zelle Circle objects in it.
    '''
    radius = 30*scale
    eyeRadius = 3*scale
    
    snowmanBase = gr.Circle(gr.Point(x,y),radius)
    snowmanBase.setFill("white")
    snowmanBase.setOutline("black")
    snowmanBase.setWidth(2)
    shapeList.append(snowmanBase)

    snowmanMid = gr.Circle(gr.Point(x,y+2*radius*scale),radius)
    snowmanMid.setFill("white")
    snowmanMid.setOutline("black")
    snowmanMid.setWidth(2)
    shapeList.append(snowmanMid)

    snowmanTop = gr.Circle(gr.Point(x,y+4*radius*scale),radius)
    snowmanTop.setFill("white")
    snowmanTop.setOutline("black")
    snowmanTop.setWidth(2)
    shapeList.append(snowmanTop)

    snowmanEyeLeft = gr.Circle(gr.Point(x-scale*radius/2, y),eyeRadius)
    snowmanEyeLeft.setFill("white")
    snowmanEyeLeft.setOutline("black")
    snowmanEyeLeft.setWidth(2)
    shapeList.append(snowmanEyeLeft)

    snowmanEyeRight = gr.Circle(gr.Point(x+scale*radius/2, y),eyeRadius)
    snowmanEyeRight.setFill("white")
    snowmanEyeRight.setOutline("black")
    snowmanEyeRight.setWidth(2)
    shapeList.append(snowmanEyeRight)


def snowman_animate(shapes, frame, screen):
    '''
    Move the snowman at the current iteration of the animation (frame).

    Parameters:
    -----------
    shapes: list with the 5 Zelle Circle objects in it that make up the snowman
    frame: int. Current iteration of the animation
    screen: GraphWin. Screen/canvas that the snowman is on.
        NOTE: The `screen` is not needed for lab.
    '''
    for drawer in range(len(shapeList)):
        shapeList[drawer].move(-(20*(frame%2)-10),5)


def snowman_test():
    '''
    Main function that creates the screen, creates the snowman, draws it to the screen.
    '''

    screen = gr.GraphWin("Yeah, We SnowManin'", width, height)
    # Honestly this logo is barely viible but I made the effort so here it is.
    logo = tk.PhotoImage(file="Project05\Daco_6135086.png")
    # Unfortunately because of tkinters scaling, which I only found out about too late. I have to use not 1080p, and I got around that by creating a fullscreen function.
    # Regardless lead to not as clean an ouput as I had hoped.
    screen.setCoords(960,540,-960,-540)
    # Sets Icon.
    screen.master.iconphoto(False, logo)
    snowman_init(0,-300,1)

    for drawer in range(len(shapeList)):
        shapeList[drawer].draw(screen)

    for iter in range(1000):
        snowman_animate(shapeList,iter,screen)
        t.sleep(1/24)
        if screen.checkMouse() is not None:
            break


if __name__ == "__main__":
    snowman_test()