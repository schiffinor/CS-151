'''
lab5_collage_animation.py
Roman Schiffino 151B Fall Semester
This is my lab file for project number 5. 
It does what the lab ask me to do.
'''

import graphicsPlus as gr
import time as t
import random as r


def randColor():
    '''
    Defines a random color and returns a tuple fro the rgb value.
    '''
    Colors = (r.randint(0,255),r.randint(0,255),r.randint(0,255))
    hexColor = '#{:02x}{:02x}{:02x}'.format(*Colors)
    return hexColor


def compColor(hexColor):
    modif =hexColor.lstrip("#")
    tupColor = (int(modif[0:2], 16), int(modif[2:4], 16), int(modif[0:2], 16))
    complementColor = tuple(int(255-tupColor[i]) for i in range(len(tupColor)))
    hexFormat = '#{:02x}{:02x}{:02x}'.format(*complementColor)
    return hexFormat


def main():
    '''
    This is the main function, this fucntion defines our three shapes,
    and adds them to our list. Finally these functions are then drawn from a loop.
    This first draws a rectangle, then an oval, and finally a triangle.
    '''
    # Here we create the screen. 
    width = 600
    height = 600
    global screen
    screen = gr.GraphWin("Yeah, We Collagin'", width, height)

    # This is our rectangle.
    rectangirella = gr.Rectangle(gr.Point(100,300),gr.Point(200,500))
    rectangirella.setFill("#E97451")
    rectangirella.setOutline("#800020")
    rectangirella.setWidth(2)

    # This is our oval.
    ovalella = gr.Oval(gr.Point(150,300),gr.Point(350,400))
    ovalella.setFill("#C04000")
    ovalella.setOutline("#000080")
    ovalella.setWidth(2)

    # This is out triangle.
    polygonella = gr.Polygon(gr.Point(200,300),gr.Point(300,400),gr.Point(250,550))
    polygonella.setFill("#4682B4")
    polygonella.setOutline("#0818A8")
    polygonella.setWidth(2)

    # This is our handy dandy shape list.
    global shapeList
    shapeList = [rectangirella, ovalella, polygonella]

    # This loops through our list and draws all our functions.
    for drawer in range(len(shapeList)):
        shapeList[drawer].draw(screen)

    # Makes the screen close on click.


def animation():
    for iter in range(1000):
        for drawer in range(len(shapeList)):
            shapeList[drawer].move(r.randint(-10,10),r.randint(-10,10))
            color = randColor()
            shapeList[drawer].setFill(color)
            shapeList[drawer].setOutline(compColor(color))
        t.sleep(0.5)
        if screen.checkMouse() is not None:
            break

# This runs the whole thing.
if __name__ == '__main__':
    main()
    animation()