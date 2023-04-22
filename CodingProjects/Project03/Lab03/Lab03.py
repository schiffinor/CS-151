import random as r
import turtle as t
'''
Lab03.py Roman Schiffino 151B Fall Semester
This is the lab file it draws a mondrian out of random sized rectangles of random colors.
'''


def goto(x,y):
    '''
    Goes to a point (x,y) without leaving a trail.
    '''
    t.up()
    t.goto(x,y)
    t.down()


def rect(width,length):
    '''
    Draws a rectangle given a length and width.
    '''
    t.seth(90)
    for iter in range(2):
        t.fd(length)
        t.right(90)
        t.fd(width)
        t.right(90)


def randTupCor():
    '''
    Creates and returns a tuple of x and y coordinates for the rectangle to be drawn.
    '''
    Coords = (r.randint(-500,500),r.randint(-500,500))
    return Coords


def randTupDims():
    '''
    Creates and returns a tuple for width and length for each rectangle.
    '''
    Dimensions = (r.randint(50,150),r.randint(50,150))
    return Dimensions


def randColor():
    '''
    Defines a random color and returns a tuple fro the rgb value.
    '''
    Colors = (r.randint(0,255),r.randint(0,255),r.randint(0,255))
    return Colors


def main():
    '''
    Main function this function is called to start the program it calls all the other functions
    it also makes sure that their are various levels of overlap governed by the random sample function and if statements.
    '''
    #These statments make it so my color values work and make it so the painting draws mor quickly.
    t.tracer(False)
    t.colormode(255)
    #This selects a random 40% of the 200 rectangles to be filled.
    filling = r.sample(range(200),80)
    filling = set(filling)
    #This is the for loop that governs the printing of all the rectangles.
    for iter in range(200):
        #The goto() and rect() functions have the asterisk added so that the code unpacks the random tuple functions and treate their outputs as independent arguments.
        if iter in set (filling):
            #Filled rectangles.
            t.fillcolor(randColor())
            t.begin_fill()
            goto(*randTupCor())
            rect(*randTupDims())
            t.end_fill()
        else:
            #Unfilled rectangles.
            goto(*randTupCor())
            rect(*randTupDims())
    #Makes sure that everything is drawn.
    t.update()
    t.exitonclick()

#Prevents main from being called from anywhere else. 
if __name__== '__main__':
    main()