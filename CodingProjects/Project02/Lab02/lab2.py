import turtle as t
'''
Lab2.py Roman Schiffino 151B Fall Semester
This is the lab file it does what thge lab asks to do it has several triangle drawing functions built in but the final function just calls a pattern.
'''
'''
A runing theme throughout this code is that by making my code such that our triangle would be automatically centered about (0,0), 
thereby making some things easier, I also made many things significantly more difficult. This is most notable in the stacking section. 
However, I was unwilling to rewrite my original programs, thus I just problem solved.
'''

def triangle(scale):
    '''
    Takes a scale parameter and then darws a triangle centered about (0,0) with sidelength  equal to 100*scale.
    The centroid is calculated using some basic trigonometry.
    '''
    sideLength=100*scale
    t.up()
    #We use properties of similar triangles and of 30-60-90 triangles to determine the position of the centroid.
    t.setpos(-sideLength/2,-sideLength/(2*(3**(1/2))))
    t.down()
    t.seth(60)
    for iter in range(3):
        t.fd(sideLength)
        t.right(120)


def goto(x,y):
    '''
    Goes to a point without leaving a line.
    '''
    t.up()
    t.goto(x,y)
    t.down()


def triangle_2(scale,x,y):
    '''
    Takes a scale parameter, an x offset, and a y offset, and then draws a triangle centered about (x_offset,y_offset) with sidelength  equal to 100*scale.
    '''
    sideLength=100*scale
    t.up()
    # Calculates Offset such that whatever triangle is centered (ie has centroid) at (x,y).
    t.setpos((-sideLength/2)+x,(-sideLength/(2*(3**(1/2)))+y))
    t.down()
    t.seth(60)
    # Main loop to draw Triangle.
    for iter in range(3):
        t.fd(sideLength)
        t.right(120)
    #Determines and returns height parameter for center of next triangle.
    maximum = (sideLength*(3**(1/2))/2)-sideLength/(2*(3**(1/2)))+sideLength/(4*(3**(1/2)))
    print(t.pos())
    return maximum


def triangleStack(scale,x,y):
    '''
    Takes a scale and offset to place a triangle stack at. The shape starts with a triangle of sidelength equal to 100*scale centered about (x,y).
    Then goes up and draws the other two triangles.
    '''
    scaleCoeff1 = scale
    scaleCoeff2 = scale/2
    scaleCoeff3 = scale/4
    #This coupled with return value from triangle_2() function provides where to center the next triange in the stack.
    height1 = triangle_2(scaleCoeff1,x,y)
    height2 = height1 + triangle_2(scaleCoeff2,x,height1+y)
    height3 = height2 + triangle_2(scaleCoeff3,x,height2+y)


triangleStack(1,0,0)
triangleStack(1/2,75,-14.4338)
triangleStack(1/3,116.5,-19.245)
t.exitonclick()