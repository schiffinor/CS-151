'''
lab4_snowman.py
Roman Schiffino 151B Fall Semester
This is my 2nd lab file for project number 4. 
It does what the lab ask me to do.
'''

import graphics as gr

width = 600
height = 600
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


def snowman_test():
    '''
    Main function that creates the screen, creates the snowman, draws it to the screen.
    '''

    screen = gr.GraphWin("Yeah, We SnowManin'", width, height)
    
    snowman_init(300,300,1)
    for drawer in range(len(shapeList)):
        shapeList[drawer].draw(screen)

    # Makes the screen close on click.
    screen.getMouse()
    screen.close()


if __name__ == "__main__":
    snowman_test()