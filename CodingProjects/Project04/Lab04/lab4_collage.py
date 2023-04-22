'''
lab4_collage.py
Roman Schiffino 151B Fall Semester
This is my lab file for project number 4. 
It does what the lab ask me to do.
'''

import graphics as gr

def main():
    '''
    This is the main function, this fucntion defines our three shapes,
    and adds them to our list. Finally these functions are then drawn from a loop.
    This first draws a rectangle, then an oval, and finally a triangle.
    '''
    # Here we create the screen. 
    width = 600
    height = 600
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
    shapeList = [rectangirella, ovalella, polygonella]

    # This loops through our list and draws all our functions.
    for drawer in range(len(shapeList)):
        shapeList[drawer].draw(screen)

    # Makes the screen close on click.
    screen.getMouse()
    screen.close()


# This runs the whole thing.
if __name__ == '__main__':
    main()