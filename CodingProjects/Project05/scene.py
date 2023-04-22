'''
scene.py
Roman Schiffino 151B Fall Semester
This is my project file for project number 5. 
'''

import graphicsPlus as gr
import numpy as np
import math as m
import tkinter as tk
import inspect as ins
from compund_shapes import *

width = 1540
height = 870
fov = 360
# Honestly this logo is barely viible but I made the effort so here it is.
logo = tk.PhotoImage(file="Project04\Daco_6135086.png")
screen = gr.GraphWin("Yeah, We Doin' a Project.'", width=width, height=height)
# Unfortunately because of tkinters scaling, which I only found out about too late. I have to use not 1080p, and I got around that by creating a fullscreen function.
#Regardless lead to not as clean an ouput as I had hoped.
screen.setCoords(-960,-540,960,540)
# Sets Icon.
screen.master.iconphoto(False, logo)
# Sets inital screenstate as not fullscreen.
screen.master.attributes("-fullscreen", False)
# Creates empty list of shapes to be drawn.
shapeList = []


def screenFull(self, event=''):
    '''
    Sooooooo long story short this function right here gave me a lot of grief. I had hoped to make it just toggleable with <F11>;
    however, unfortunately when I made the function change the togglestate it broke everything... So just use <F11> to fullscreen and <Escape> to exit fullscreen.
    '''
    screen.master.attributes("-fullscreen", True)


def screenEsc(self, event=''):
    '''
    Same Story as above this is the toggle off function.
    '''
    screen.master.attributes("-fullscreen", False)


def main():
    screen.bind_all("<F11>", screenFull)
    screen.bind_all("<Escape>", screenEsc)
    color = ("#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C","#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C","#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C")
    pillar_v3(8,0,0,200,20,300,0,0,0,22.5,color)
    for drawer in range(len(shapeList)):
        shapeList[drawer].draw(screen)
    screen.getMouse()
    screen.close()

main()