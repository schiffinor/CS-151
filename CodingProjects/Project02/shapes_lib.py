import turtle as t
import numpy as np
import math as m
'''
shapes_lib.py Roman Schiffino 151B Fall Semester
This is my module file late as it may be. 
It basically is a basic 3d renderer/3d point modeler.
'''
'''
This was such a headache to be quite honest. 3d modeling is really very annoying if you literally do it point by point.
I was able to save myself some pain by using for loops, conditionals and some frequently callable and very parametrizable functions,
still a pain though. Hope you like it! :)
P.S. Fun Fact: Almost everything is done to scale (I got in contact with the school to get original blueprints.)
However some creative liberties were tken for my sanity and to make things in my opinion slightly better looking than just maintaining scale.
Also didn't do the back really. Theoretically speaking you culd probably see it by throwing RotateY() on every point, but not worth it.
'''

#Basic parameters for the entire image. Theoretically these should all be ok to change and get differnt angles and zoom levels; however, that is not tested.
fov = 210
depth = 130
base = -70


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


def floor():
    '''
    This just creates a big old base for everything.
    If you want to see how it traces I would suggest disabling this function by commenting it out in main.py.
    Otherwise it'll take a very long time. This shape is huge.
    '''
    t.fillcolor("#5c6e0b")
    goto(*perspectiveMap(-900,base,depth-129,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(900,base,depth-129,fov))
    t.goto(*perspectiveMap(900,base,depth+100,fov))
    t.goto(*perspectiveMap(-900,base,depth+100,fov))
    t.goto(*perspectiveMap(-900,base,depth-129,fov))
    t.end_fill()


def RotateX(x,y,z,theta):
    '''
    Rotates a point (x,y,z) about the x axis using a rotation matrix.
    '''
    #Convert to radians.
    theta = m.pi*(theta/(180))
    #Vector form of (x,y,z)
    v1=np.array([[x],[y],[z]])
    #Rotation Matrix.
    rotation=np.array([[1,0,0],[0,m.cos(theta),-(m.sin(theta))],[0,m.sin(theta),m.cos(theta)]])
    transform=np.dot(rotation,v1)
    #Vector to Tuple.
    transform=np.reshape(transform,3)
    transform=tuple(transform)
    return transform    


def RotateZ(x,y,z,theta):
    '''
    Rotates a point (x,y,z) about the z axis using a rotation matrix.
    '''
    #Convert to radians.
    theta = m.pi*(theta/(180))
    #Vector form of (x,y,z)
    v1=np.array([[x],[y],[z]])
    #Rotation Matrix.
    rotation=np.array([[m.cos(theta),-(m.sin(theta)),0],[m.sin(theta),m.cos(theta),0],[0,0,1]])
    transform=np.dot(rotation,v1)
    #Vector to Tuple.
    transform=np.reshape(transform,3)
    transform=tuple(transform)
    return transform    


def RotateY(x,y,z,theta):
    '''
    Rotates a point (x,y,z) about the y axis using a rotation matrix.
    '''
    #Convert to radians.
    theta = m.pi*(theta/(180))
    #Vector form of (x,y,z)
    v1=np.array([[x],[y],[z]])
    #Rotation Matrix.
    rotation=np.array([[m.cos(theta),0,m.sin(theta)],[0,1,0],[-(m.sin(theta)),0,m.cos(theta)]])
    transform=np.dot(rotation,v1)
    #Vector to Tuple.
    transform=np.reshape(transform,3)
    transform=tuple(transform)
    return transform    


def perspectiveMap(x,y,z,fov):
    '''
    Truly the most core and important function in this project.
    This function basically takes any point in my "made up" 3d coordinate system and converts it into 2d screen coordinates.
    '''
    xProj = ((x)*(fov/z))
    yProj = ((y)*(fov/z))
    return (xProj,yProj)


def fullTransform(x,y,z,theta1,theta2,theta3):
    '''
    This function really just combines the three rotation functions to be slightly more concise in the many occasions where all 3 are called on the same point.
    '''
    point=RotateZ(*RotateY(*RotateX(x,y,z,theta1),theta2),theta3)
    return point


def polarCircle(xCenter,yCenter,zCenter,r,xRot,yRot,zRot):
    '''
    This is actually edited code from another of my projects.
    Basically just lets me define a circle in terms of center and radius.
    Then draw it at any angle in three axes of rotation and mapped to the clipping pane.
    Simple shape #2.
    '''
    # polar defined circle function converted to cartesian coordinates
    for deg in range(0,360):
    # unit conversion because radians.
        theta = m.radians(deg)
    # polar function converted to cartesian coordinates
        x = r*m.cos(theta)
        y = r*m.sin(theta)
    # removes initial origin line
        if deg == 0:
            t.up()
            t.goto(*perspectiveMap(*tuple(np.reshape(np.array([fullTransform(x,y,0,xRot,yRot,zRot)])+np.array([xCenter,yCenter,zCenter]),3)),fov))
            t.down()
    # calls function        
        else:
            t.goto(*perspectiveMap(*tuple(np.reshape(np.array([fullTransform(x,y,0,xRot,yRot,zRot)])+np.array([xCenter,yCenter,zCenter]),3)),fov))
    t.end_fill()


def polarSphere(xCenter,yCenter,zCenter,r,xRot,yRot,zRot):
    '''
    Like the last function but to draw a spere using spherical coordinates.
    This function was bust; however, it was written at like 5am or so so it very well may have some issues.
    '''
    # polar defined circle function converted to cartesian coordinates
    for deg2 in range(0,180):
        for deg in range(0,360):
    # unit conversion because radians.
            theta = m.radians(deg)
    # polar function converted to cartesian coordinates
            x = r*m.cos(theta)
            y = r*m.sin(theta)
    # removes initial origin line
            if deg == 0:
                t.up()
                t.goto(*perspectiveMap(*tuple(np.reshape(np.array([fullTransform(x,y,0,xRot,yRot,deg2)])+np.array([xCenter,yCenter,zCenter]),3)),fov))
                t.down()
    # calls function        
            else:
                t.goto(*perspectiveMap(*tuple(np.reshape(np.array([fullTransform(x,y,0,xRot,yRot,deg2)])+np.array([xCenter,yCenter,zCenter]),3)),fov))
        t.end_fill()


def polarCirclOffset(xCenter,yCenter,zCenter,zOff,r,xRot,yRot,zRot):
    '''
    Basically the same as the original polarCircle() function except for the fact that you can set the position of the axes of revolution.
    very useful in automating the drawing of many circles equidistant from a center.
    '''
    # polar defined circle function converted to cartesian coordinates
    for deg in range(0,360):
    # unit conversion because radians.
        theta = m.radians(deg)
    # polar function converted to cartesian coordinates
        x = r*m.cos(theta)
        y = r*m.sin(theta)
    # removes initial origin line
        if deg == 0:
            t.up()
            t.goto(*perspectiveMap(*tuple(np.reshape(np.array([fullTransform(x,y,zOff,xRot,yRot,zRot)])+np.array([xCenter,yCenter,zCenter]),3)),fov))
            t.down()
    # calls function        
        else:
            t.goto(*perspectiveMap(*tuple(np.reshape(np.array([fullTransform(x,y,zOff,xRot,yRot,zRot)])+np.array([xCenter,yCenter,zCenter]),3)),fov))
    t.end_fill()


'''
Disclaimer: from now on the functions aren't really too commentable. 
They mostly consist of 10's to 100's of points in a slightly convoluted layout.
The triangularization was because of some earlier tests with rotation that went badly.
However, I later deemed the triangularization unnecessary, so yeah don't mind that.
Also, The windows wouldn't be too bad to put in, it looks a little weird without all the windows, I just couldn't bare spending any longr on this.
'''


def mainBodyBack():
    '''
    For me to accurately describe what this is, you'd probably need to see the blue prints but this is basically,
    the shorther and wider part of miller's main body. 
    The part with no fancy trim.
    '''
    t.fillcolor("#a3695d")
    goto(*perspectiveMap(85,base,depth+20,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-85,base,depth+20,fov))
    t.goto(*perspectiveMap(-85,base+55,depth+20,fov))
    goto(*perspectiveMap(85,base,depth+20,fov))
    t.goto(*perspectiveMap(85,base+55,depth+20,fov))
    t.goto(*perspectiveMap(-85,base+55,depth+20,fov))
    t.end_fill()
    t.fillcolor("#f8f3ed") 
    goto(*perspectiveMap(-85,base+50,depth+20,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-85,base+55,depth+20,fov))
    t.goto(*perspectiveMap(85,base+55,depth+20,fov))
    t.goto(*perspectiveMap(85,base+50,depth+20,fov))
    t.goto(*perspectiveMap(-85,base+50,depth+20,fov))
    t.goto(*perspectiveMap(-85,base+52.5,depth+20,fov))
    t.goto(*perspectiveMap(85,base+52.5,depth+20,fov))
    t.goto(*perspectiveMap(85,base+50,depth+20,fov))
    t.goto(*perspectiveMap(-85,base+50,depth+20,fov))
    t.end_fill()


def mainBodyFront():
    '''
    On the other hand this is the taller but thinner part of miller.
    With the fancy trim.
    '''
    t.fillcolor("#a3695d")
    goto(*perspectiveMap(72.9,base,depth+20,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-72.9,base,depth+20,fov))
    t.goto(*perspectiveMap(-72.9,base+66,depth+20,fov))
    goto(*perspectiveMap(72.9,base,depth+20,fov))
    t.goto(*perspectiveMap(72.9,base+66,depth+20,fov))
    t.goto(*perspectiveMap(-72.9,base+66,depth+20,fov))
    t.end_fill()
    goto(*perspectiveMap(-72.9,base,depth+20,fov))
    t.fillcolor("#f8f3ed") 
    goto(*perspectiveMap(-72.9,base+50,depth+20,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-72.9,base+55,depth+20,fov))
    t.goto(*perspectiveMap(72.9,base+55,depth+20,fov))
    t.goto(*perspectiveMap(72.9,base+50,depth+20,fov))
    t.goto(*perspectiveMap(-72.9,base+50,depth+20,fov))
    t.goto(*perspectiveMap(-72.9,base+52.5,depth+20,fov))
    t.goto(*perspectiveMap(72.9,base+52.5,depth+20,fov))
    t.goto(*perspectiveMap(72.9,base+50,depth+20,fov))
    t.goto(*perspectiveMap(-72.9,base+50,depth+20,fov))
    t.end_fill()
    #This lays that nice brick texture on the left side. Basically just determines whether y is odd or even.
    #Also should probably mention positive x is right, positive y is up, and positive z is into the screen space.
    for ySub in range(0,65,5):
        t.fillcolor("#f8f3ed")
        if (ySub % 2) == 0:
            goto(*perspectiveMap(-67.9,base+ySub,depth+20,fov))
            t.begin_fill()
            t.goto(*perspectiveMap(-72.9,base+ySub,depth+20,fov))
            t.goto(*perspectiveMap(-72.9,base+ySub+5,depth+20,fov))
            t.goto(*perspectiveMap(-67.9,base+ySub+5,depth+20,fov))
            t.goto(*perspectiveMap(-67.9,base+ySub,depth+20,fov))
            t.end_fill()
        else:
            goto(*perspectiveMap(-62.9,base+ySub,depth+20,fov))
            t.begin_fill()
            t.goto(*perspectiveMap(-72.9,base+ySub,depth+20,fov))
            t.goto(*perspectiveMap(-72.9,base+ySub+5,depth+20,fov))
            t.goto(*perspectiveMap(-62.9,base+ySub+5,depth+20,fov))
            t.goto(*perspectiveMap(-62.9,base+ySub,depth+20,fov))
            t.end_fill()
    #This lays that nice brick texture on the right side. Basically just determines whether y is odd or even.
    for ySub in range(0,65,5):
        t.fillcolor("#f8f3ed")
        if (ySub % 2) == 0:
            goto(*perspectiveMap(67.9,base+ySub,depth+20,fov))
            t.begin_fill()
            t.goto(*perspectiveMap(72.9,base+ySub,depth+20,fov))
            t.goto(*perspectiveMap(72.9,base+ySub+5,depth+20,fov))
            t.goto(*perspectiveMap(67.9,base+ySub+5,depth+20,fov))
            t.goto(*perspectiveMap(67.9,base+ySub,depth+20,fov))
            t.end_fill()
        else:
            goto(*perspectiveMap(62.9,base+ySub,depth+20,fov))
            t.begin_fill()
            t.goto(*perspectiveMap(72.9,base+ySub,depth+20,fov))
            t.goto(*perspectiveMap(72.9,base+ySub+5,depth+20,fov))
            t.goto(*perspectiveMap(62.9,base+ySub+5,depth+20,fov))
            t.goto(*perspectiveMap(62.9,base+ySub,depth+20,fov))
            t.end_fill()
    #White base trim
    goto(*perspectiveMap(-72.9,base,depth+20,fov))
    t.fillcolor("#f8f3ed") 
    t.begin_fill()
    t.goto(*perspectiveMap(-72.9,base+15,depth+20,fov))
    t.goto(*perspectiveMap(72.9,base+15,depth+20,fov))
    t.goto(*perspectiveMap(72.9,base,depth+20,fov))
    t.goto(*perspectiveMap(-72.9,base,depth+20,fov))
    t.end_fill()


def mainBodyRoof():
    '''
    Pretty self explanatory the lower roof for the main body defined earlier.
    '''
    t.fillcolor("#7f9291")
    goto(*perspectiveMap(-84,base+53.5,depth+19,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-110,base+70,depth+40,fov))
    t.goto(*perspectiveMap(110,base+70,depth+40,fov))
    t.goto(*perspectiveMap(84,base+53.5,depth+19,fov))
    t.goto(*perspectiveMap(-84,base+53.5,depth+19,fov))
    t.end_fill()


def mainBodyTopRoof():
    '''
    Conversely this is the upper roof for the main body function.
    '''
    t.fillcolor("#7f9291")
    goto(*perspectiveMap(-74,base+65,depth+19,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(74,base+65,depth+19,fov))
    t.goto(*perspectiveMap(74,base+85,depth+40,fov))
    t.goto(*perspectiveMap(-74,base+85,depth+40,fov))
    t.goto(*perspectiveMap(-74,base+65,depth+19,fov))
    t.end_fill()


def leftWingRight():
    '''
    Right (inner) wall for the left wing.
    '''
    t.fillcolor("#a3695d")
    goto(*perspectiveMap(-85,base,depth+20,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-85,base,depth-35,fov))
    t.goto(*perspectiveMap(-85,base+55,depth-35,fov))
    goto(*perspectiveMap(-85,base,depth+20,fov))
    t.goto(*perspectiveMap(-85,base+55,depth+20,fov))
    t.goto(*perspectiveMap(-85,base+55,depth-35,fov))
    t.end_fill()
    t.fillcolor("#f8f3ed")
    goto(*perspectiveMap(-85,base+50,depth+20,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-85,base+55,depth+20,fov))
    t.goto(*perspectiveMap(-85,base+55,depth-35,fov))
    t.goto(*perspectiveMap(-85,base+50,depth-35,fov))
    t.goto(*perspectiveMap(-85,base+50,depth+20,fov))
    t.end_fill()
    t.begin_fill()
    t.goto(*perspectiveMap(-85,base+53.5,depth+20,fov))
    t.goto(*perspectiveMap(-85,base+53.5,depth-35,fov))
    t.goto(*perspectiveMap(-85,base+50,depth-35,fov))
    t.goto(*perspectiveMap(-85,base+50,depth+20,fov))
    t.end_fill()


def rightWingLeft():
    '''
    Left (inner) wing of the right wing. 
    '''
    t.fillcolor("#a3695d")
    goto(*perspectiveMap(85,base,depth+20,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(85,base,depth-35,fov))
    t.goto(*perspectiveMap(85,base+55,depth-35,fov))
    goto(*perspectiveMap(85,base,depth+20,fov))
    t.goto(*perspectiveMap(85,base+55,depth+20,fov))
    t.goto(*perspectiveMap(85,base+55,depth-35,fov))
    t.end_fill()
    t.fillcolor("#f8f3ed")
    goto(*perspectiveMap(85,base+50,depth+20,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(85,base+55,depth+20,fov))
    t.goto(*perspectiveMap(85,base+55,depth-35,fov))
    t.goto(*perspectiveMap(85,base+50,depth-35,fov))
    t.goto(*perspectiveMap(85,base+50,depth+20,fov))
    t.end_fill()
    t.begin_fill()
    t.goto(*perspectiveMap(85,base+53.5,depth+20,fov))
    t.goto(*perspectiveMap(85,base+53.5,depth-35,fov))
    t.goto(*perspectiveMap(85,base+50,depth-35,fov))
    t.goto(*perspectiveMap(85,base+50,depth+20,fov))
    t.end_fill()



def leftWingFront():
    '''
    Ok so here is when the commenting starts to get tricky. Here I baked a lot of the trim data into the main functions.
    However, basically the front panel of the left wing with some trim.
    If the color is #a3695d then its main body, if its #f8f3ed its trim.
    Anything else is windows. 
    '''
    #Body
    t.fillcolor("#a3695d")
    goto(*perspectiveMap(-85,base,depth-35,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-135,base,depth-35,fov))
    t.goto(*perspectiveMap(-135,base+55,depth-35,fov))
    goto(*perspectiveMap(-85,base,depth-35,fov))
    t.goto(*perspectiveMap(-85,base+55,depth-35,fov))
    t.goto(*perspectiveMap(-135,base+55,depth-35,fov))
    t.end_fill()
    goto(*perspectiveMap(-85,base+55,depth-35,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-110,base+70,depth-35,fov))
    t.goto(*perspectiveMap(-135,base+55,depth-35,fov))
    t.goto(*perspectiveMap(-85,base+55,depth-35,fov))
    t.end_fill()
    #Trim
    t.fillcolor("#f8f3ed") 
    t.begin_fill()
    t.goto(*perspectiveMap(-85,base+55,depth-35,fov))
    t.goto(*perspectiveMap(-135,base+55,depth-35,fov))
    t.goto(*perspectiveMap(-135,base+50,depth-35,fov))
    t.goto(*perspectiveMap(-85,base+50,depth-35,fov))
    t.goto(*perspectiveMap(-85,base+53.5,depth-35,fov))
    t.goto(*perspectiveMap(-135,base+53.5,depth-35,fov))
    t.goto(*perspectiveMap(-135,base+50,depth-35,fov))
    t.goto(*perspectiveMap(-85,base+50,depth-35,fov))
    t.end_fill()
    t.begin_fill()
    t.goto(*perspectiveMap(-85,base+55,depth-35,fov))
    t.goto(*perspectiveMap(-110,base+70,depth-35,fov))
    t.goto(*perspectiveMap(-135,base+55,depth-35,fov))
    t.goto(*perspectiveMap(-128,base+55,depth-35,fov))
    t.goto(*perspectiveMap(-110,base+66,depth-35,fov))
    t.goto(*perspectiveMap(-110,base+70,depth-35,fov))
    t.goto(*perspectiveMap(-110,base+66,depth-35,fov))
    t.goto(*perspectiveMap(-92,base+55,depth-35,fov))
    t.goto(*perspectiveMap(-85,base+55,depth-35,fov))
    t.end_fill()
    t.begin_fill()
    t.goto(*perspectiveMap(-85,base+55,depth-35,fov))
    t.goto(*perspectiveMap(-110,base+70,depth-35,fov))
    t.goto(*perspectiveMap(-135,base+55,depth-35,fov))
    t.goto(*perspectiveMap(-132,base+55,depth-35,fov))
    t.goto(*perspectiveMap(-110,base+68.5,depth-35,fov))
    t.goto(*perspectiveMap(-110,base+70,depth-35,fov))
    t.goto(*perspectiveMap(-110,base+68.5,depth-35,fov))
    t.goto(*perspectiveMap(-88,base+55,depth-35,fov))
    t.goto(*perspectiveMap(-85,base+55,depth-35,fov))
    t.end_fill()
    t.begin_fill()
    polarCircle(-110,base+60,depth-35,4,0,0,0)
    t.end_fill()
    #Window
    t.fillcolor("#504f55")
    t.begin_fill()
    polarCircle(-110,base+60,depth-35,2.5,0,0,0)
    t.end_fill()


def leftWingRoofRight():
    '''
    Right side of roof for left wing.
    '''
    t.fillcolor("#7f9291")
    goto(*perspectiveMap(-84,base+53.5,depth-36,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-110,base+70,depth-36,fov))
    t.goto(*perspectiveMap(-110,base+70,depth+40,fov))
    t.goto(*perspectiveMap(-84,base+53.5,depth+19,fov))
    t.goto(*perspectiveMap(-84,base+53.5,depth-36,fov))
    t.end_fill()


def lefttWingRoofleft():
    '''
    Left side of roof for left wing.
    '''
    t.fillcolor("#7f9291")
    goto(*perspectiveMap(-136,base+53.5,depth-36,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-110,base+70,depth-36,fov))
    t.goto(*perspectiveMap(-110,base+70,depth+40,fov))
    t.goto(*perspectiveMap(-136,base+53.5,depth+19,fov))
    t.goto(*perspectiveMap(-136,base+53.5,depth-36,fov))
    t.end_fill()


def rightWingFront():
    '''
    Same as above, basically the front panel of the left wing with some trim.
    If the color is #a3695d then its main body, if its #f8f3ed its trim.
    Anything else is windows. 
    '''
    #Body
    t.fillcolor("#a3695d")
    goto(*perspectiveMap(85,base,depth-35,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(135,base,depth-35,fov))
    t.goto(*perspectiveMap(135,base+55,depth-35,fov))
    goto(*perspectiveMap(85,base,depth-35,fov))
    t.goto(*perspectiveMap(85,base+55,depth-35,fov))
    t.goto(*perspectiveMap(135,base+55,depth-35,fov))
    t.end_fill()
    goto(*perspectiveMap(85,base+55,depth-35,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(110,base+70,depth-35,fov))
    t.goto(*perspectiveMap(135,base+55,depth-35,fov))
    t.goto(*perspectiveMap(85,base+55,depth-35,fov))
    t.end_fill()
    #Trim
    t.fillcolor("#f8f3ed") 
    t.begin_fill()
    t.goto(*perspectiveMap(85,base+55,depth-35,fov))
    t.goto(*perspectiveMap(135,base+55,depth-35,fov))
    t.goto(*perspectiveMap(135,base+50,depth-35,fov))
    t.goto(*perspectiveMap(85,base+50,depth-35,fov))
    t.goto(*perspectiveMap(85,base+53.5,depth-35,fov))
    t.goto(*perspectiveMap(135,base+53.5,depth-35,fov))
    t.goto(*perspectiveMap(135,base+50,depth-35,fov))
    t.goto(*perspectiveMap(85,base+50,depth-35,fov))
    t.end_fill()
    t.begin_fill()
    t.goto(*perspectiveMap(85,base+55,depth-35,fov))
    t.goto(*perspectiveMap(110,base+70,depth-35,fov))
    t.goto(*perspectiveMap(135,base+55,depth-35,fov))
    t.goto(*perspectiveMap(128,base+55,depth-35,fov))
    t.goto(*perspectiveMap(110,base+66,depth-35,fov))
    t.goto(*perspectiveMap(110,base+70,depth-35,fov))
    t.goto(*perspectiveMap(110,base+66,depth-35,fov))
    t.goto(*perspectiveMap(92,base+55,depth-35,fov))
    t.goto(*perspectiveMap(85,base+55,depth-35,fov))
    t.end_fill()
    t.begin_fill()
    t.goto(*perspectiveMap(85,base+55,depth-35,fov))
    t.goto(*perspectiveMap(110,base+70,depth-35,fov))
    t.goto(*perspectiveMap(135,base+55,depth-35,fov))
    t.goto(*perspectiveMap(132,base+55,depth-35,fov))
    t.goto(*perspectiveMap(110,base+68.5,depth-35,fov))
    t.goto(*perspectiveMap(110,base+70,depth-35,fov))
    t.goto(*perspectiveMap(110,base+68.5,depth-35,fov))
    t.goto(*perspectiveMap(88,base+55,depth-35,fov))
    t.goto(*perspectiveMap(85,base+55,depth-35,fov))
    t.end_fill()
    t.begin_fill()
    polarCircle(110,base+60,depth-35,4,0,0,0)
    t.end_fill()
    #Window
    t.fillcolor("#504f55")
    t.begin_fill()
    polarCircle(110,base+60,depth-35,2.5,0,0,0)
    t.end_fill()


def rightWingRoofLeft():
    '''
    Left side of roof for right wing.
    '''
    t.fillcolor("#7f9291")
    goto(*perspectiveMap(84,base+53.5,depth-36,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(110,base+70,depth-36,fov))
    t.goto(*perspectiveMap(110,base+70,depth+40,fov))
    t.goto(*perspectiveMap(84,base+53.5,depth+19,fov))
    t.goto(*perspectiveMap(84,base+53.5,depth-36,fov))
    t.end_fill()


def rightWingRoofRight():
    '''
    Right side of roof for right wing.
    '''
    t.fillcolor("#7f9291")
    goto(*perspectiveMap(136,base+53.5,depth-36,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(110,base+70,depth-36,fov))
    t.goto(*perspectiveMap(110,base+70,depth+40,fov))
    t.goto(*perspectiveMap(136,base+53.5,depth+19,fov))
    t.goto(*perspectiveMap(136,base+53.5,depth-36,fov))
    t.end_fill()


def leftWingLeft():
    '''
    Left (outer) wing of the left wing. 
    '''
    t.fillcolor("#a3695d")
    goto(*perspectiveMap(-135,base,depth-35,fov))    
    t.begin_fill()
    t.goto(*perspectiveMap(-135,base,depth+150,fov))
    t.goto(*perspectiveMap(-135,base+55,depth+150,fov))
    goto(*perspectiveMap(-135,base,depth-35,fov))    
    t.goto(*perspectiveMap(-135,base+55,depth-35,fov))  
    t.goto(*perspectiveMap(-135,base+55,depth+150,fov))
    t.end_fill()


def rightWingRight():
    '''
    Right (outer) wing of the right wing. 
    '''
    t.fillcolor("#a3695d")
    goto(*perspectiveMap(135,base,depth-35,fov))    
    t.begin_fill()
    t.goto(*perspectiveMap(135,base,depth+150,fov))
    t.goto(*perspectiveMap(135,base+55,depth+150,fov))
    goto(*perspectiveMap(135,base,depth-35,fov))    
    t.goto(*perspectiveMap(135,base+55,depth-35,fov))  
    t.goto(*perspectiveMap(135,base+55,depth+150,fov))
    t.end_fill()


def triRoofFront():
    '''
    Front of triange pediment at miller. Draws two triangles for design.
    '''
    goto(*perspectiveMap(-40,base+55,depth,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(0,base+70,depth,fov))
    t.goto(*perspectiveMap(40,base+55,depth,fov))
    t.goto(*perspectiveMap(-40,base+55,depth,fov))
    t.end_fill()
    goto(*perspectiveMap(-33,base+56.5,depth,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(0,base+69,depth,fov))
    t.goto(*perspectiveMap(33,base+56.5,depth,fov))
    t.goto(*perspectiveMap(-34,base+56.5,depth,fov))
    t.end_fill()


def triRoofBottom():
    '''
    Bottom of pediment depth reasons.
    '''
    goto(*perspectiveMap(-40,base+55,depth,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-40,base+55,depth+20,fov))
    t.goto(*perspectiveMap(40,base+55,depth+20,fov))
    t.goto(*perspectiveMap(40,base+55,depth,fov))
    t.goto(*perspectiveMap(-40,base+55,depth,fov))
    t.end_fill()


def triRoofTopLeft():
    '''
    Roof for pediment left side.
    '''
    t.fillcolor("#7f9291")
    goto(*perspectiveMap(-40,base+55,depth+20,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-40,base+55,depth-5,fov))
    t.goto(*perspectiveMap(0,base+70,depth-5,fov))
    goto(*perspectiveMap(-40,base+55,depth+20,fov))
    t.goto(*perspectiveMap(0,base+70,depth+20,fov))
    t.goto(*perspectiveMap(0,base+70,depth-5,fov))
    t.end_fill()


def triRoofTopRight():
    '''
    Roof for pediment right side.
    '''
    t.fillcolor("#7f9291")
    goto(*perspectiveMap(40,base+55,depth+20,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(40,base+55,depth-5,fov))
    t.goto(*perspectiveMap(0,base+70,depth-5,fov))
    goto(*perspectiveMap(40,base+55,depth+20,fov))
    t.goto(*perspectiveMap(0,base+70,depth+20,fov))
    t.goto(*perspectiveMap(0,base+70,depth-5,fov))
    t.end_fill()


def columnsBeams():
    '''
    This draws the columns that support the main pediment. It uses for loops to make it easier and draws three sides.
    '''
    for x in range(-32,38,10):
        goto(*perspectiveMap(x,base+47,depth+5,fov))
        t.begin_fill()
        t.goto(*perspectiveMap(x,base+47,depth+12,fov))
        t.goto(*perspectiveMap(x,base+18,depth+12,fov))
        t.goto(*perspectiveMap(x,base+18,depth+5,fov))
        t.goto(*perspectiveMap(x,base+47,depth+5,fov))
        t.end_fill()
        goto(*perspectiveMap(x+4,base+47,depth+5,fov))
        t.begin_fill()
        t.goto(*perspectiveMap(x+4,base+47,depth+12,fov))
        t.goto(*perspectiveMap(x+4,base+18,depth+12,fov))
        t.goto(*perspectiveMap(x+4,base+18,depth+5,fov))
        t.goto(*perspectiveMap(x+4,base+47,depth+5,fov))
        t.end_fill()
        goto(*perspectiveMap(x,base+47,depth+5,fov))
        t.begin_fill()
        t.goto(*perspectiveMap(x+4,base+47,depth+5,fov))
        t.goto(*perspectiveMap(x+4,base+18,depth+5,fov))
        t.goto(*perspectiveMap(x,base+18,depth+5,fov))
        t.goto(*perspectiveMap(x,base+47,depth+5,fov))
        t.end_fill()
    goto(*perspectiveMap(-35,base+47,depth+5,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-35,base+47,depth+15,fov))
    t.goto(*perspectiveMap(-35,base+55,depth+15,fov))
    t.goto(*perspectiveMap(-35,base+55,depth+5,fov))
    t.goto(*perspectiveMap(-35,base+47,depth+5,fov))
    t.end_fill()
    goto(*perspectiveMap(35,base+47,depth+5,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(35,base+47,depth+15,fov))
    t.goto(*perspectiveMap(35,base+55,depth+15,fov))
    t.goto(*perspectiveMap(35,base+55,depth+5,fov))
    t.goto(*perspectiveMap(35,base+47,depth+5,fov))
    t.end_fill()
    goto(*perspectiveMap(-35,base+47,depth+5,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(35,base+47,depth+5,fov))
    t.goto(*perspectiveMap(35,base+47,depth+15,fov))
    t.goto(*perspectiveMap(-35,base+47,depth+15,fov))
    t.goto(*perspectiveMap(-35,base+47,depth+5,fov))
    t.end_fill()
    goto(*perspectiveMap(-35,base+55,depth+5,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(35,base+55,depth+5,fov))
    t.goto(*perspectiveMap(35,base+47,depth+5,fov))
    t.goto(*perspectiveMap(-35,base+47,depth+5,fov))
    t.goto(*perspectiveMap(-35,base+55,depth+5,fov))
    t.end_fill()
    

def frontBaseTop():
    '''
    This draws the floor for the miller main entrance.
    '''
    goto(*perspectiveMap(-40,base+18,depth,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-40,base+18,depth+20,fov))
    t.goto(*perspectiveMap(40,base+18,depth+20,fov))
    t.goto(*perspectiveMap(40,base+18,depth,fov))
    t.goto(*perspectiveMap(-40,base+18,depth,fov))
    t.end_fill()


def frontBaseFront():
    '''
    This draws the front of the main entrance base/floor.
    '''
    goto(*perspectiveMap(-40,base,depth,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-40,base+18,depth,fov))
    t.goto(*perspectiveMap(40,base+18,depth,fov))
    t.goto(*perspectiveMap(40,base,depth,fov))
    t.goto(*perspectiveMap(-40,base,depth,fov))
    t.end_fill()


def front():
    '''
    Calls all the main front entrance functions in correct clipping order.
    '''
    t.fillcolor("#f8f3ed") 
    frontBaseTop()
    frontBaseFront()
    columnsBeams()
    triRoofTopLeft()
    triRoofTopRight()
    t.fillcolor("#f8f3ed") 
    triRoofBottom()
    triRoofFront()
    stairs()


def stairs():
    '''
    This draws the stairs. Not much more to say.
    '''
    depthOff = depth-1.6
    #Top stairs
    for yOff in range(18,9,-1):
        #Stair Tread 
        goto(*perspectiveMap(-20,base+yOff-1,depthOff,fov))
        t.begin_fill()
        t.goto(*perspectiveMap(-20,base+yOff-1,depthOff,fov))
        t.goto(*perspectiveMap(20,base+yOff-1,depthOff,fov))
        t.goto(*perspectiveMap(20,base+yOff-1,depthOff+1.6,fov))
        t.goto(*perspectiveMap(-20,base+yOff-1,depthOff+1.6,fov))
        t.end_fill()
        #Stair Riser
        goto(*perspectiveMap(-20,base+yOff-1,depthOff+1.6,fov))
        t.begin_fill()
        t.goto(*perspectiveMap(-20,base+yOff,depthOff+1.6,fov))
        t.goto(*perspectiveMap(20,base+yOff,depthOff+1.6,fov))
        t.goto(*perspectiveMap(20,base+yOff-1,depthOff+1.6,fov))
        t.goto(*perspectiveMap(-20,base+yOff-1,depthOff+1.6,fov))
        t.end_fill()
        depthOff -= 1.6
    depthOff -= 6.4
    #Wide step tread.
    goto(*perspectiveMap(-20,base+yOff-2,depthOff+6.4,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-20,base+yOff-2,depthOff,fov))
    t.goto(*perspectiveMap(20,base+yOff-2,depthOff,fov))
    t.goto(*perspectiveMap(20,base+yOff-2,depthOff+6.4,fov))
    t.goto(*perspectiveMap(-20,base+yOff-2,depthOff+6.4,fov))
    t.end_fill()
    #Wide step riser
    goto(*perspectiveMap(-20,base+yOff-2,depthOff+6.4,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-20,base+yOff-1,depthOff+6.4,fov))
    t.goto(*perspectiveMap(20,base+yOff-1,depthOff+6.4,fov))
    t.goto(*perspectiveMap(20,base+yOff-2,depthOff+6.4,fov))
    t.goto(*perspectiveMap(-20,base+yOff-2,depthOff+6.4,fov))
    t.end_fill()
    depthOff -= 1.6
    #Lower steps.
    for yOff in range(8,0,-1):
        #Stair tread
        goto(*perspectiveMap(-20,base+yOff-1,depthOff+1.6,fov))
        t.begin_fill()
        t.goto(*perspectiveMap(-20,base+yOff-1,depthOff,fov))
        t.goto(*perspectiveMap(20,base+yOff-1,depthOff,fov))
        t.goto(*perspectiveMap(20,base+yOff-1,depthOff+1.6,fov))
        t.goto(*perspectiveMap(-20,base+yOff-1,depthOff+1.6,fov))
        t.end_fill()
        #Stair riser.
        goto(*perspectiveMap(-20,base+yOff-1,depthOff+1.6,fov))
        t.begin_fill()
        t.goto(*perspectiveMap(-20,base+yOff,depthOff+1.6,fov))
        t.goto(*perspectiveMap(20,base+yOff,depthOff+1.6,fov))
        t.goto(*perspectiveMap(20,base+yOff-1,depthOff+1.6,fov))
        t.goto(*perspectiveMap(-20,base+yOff-1,depthOff+1.6,fov))
        t.end_fill()
        depthOff -= 1.6
    #Balustrades or Stringer I guess.
    goto(*perspectiveMap(-20,base+18,depth,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-20,base+9,depth-14.4,fov))
    t.goto(*perspectiveMap(-24,base+9,depth-14.4,fov))
    t.goto(*perspectiveMap(-24,base+18,depth,fov))
    t.goto(*perspectiveMap(-20,base+18,depth,fov))
    t.end_fill()
    goto(*perspectiveMap(-20,base+9,depth-14.4,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-20,base+9,depth-20.8,fov))
    t.goto(*perspectiveMap(-24,base+9,depth-20.8,fov))
    t.goto(*perspectiveMap(-24,base+9,depth-14.4,fov))
    t.goto(*perspectiveMap(-20,base+9,depth-14.4,fov))
    t.end_fill()
    goto(*perspectiveMap(-20,base+9,depth-14.4,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(-20,base,depth-35.8,fov))
    t.goto(*perspectiveMap(-24,base,depth-35.8,fov))
    t.goto(*perspectiveMap(-24,base+9,depth-20.8,fov))
    t.goto(*perspectiveMap(-20,base+9,depth-20.8,fov))
    t.end_fill()
    goto(*perspectiveMap(20,base+18,depth,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(20,base+9,depth-14.4,fov))
    t.goto(*perspectiveMap(24,base+9,depth-14.4,fov))
    t.goto(*perspectiveMap(24,base+18,depth,fov))
    t.goto(*perspectiveMap(20,base+18,depth,fov))
    t.end_fill()
    goto(*perspectiveMap(20,base+9,depth-14.4,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(20,base+9,depth-20.8,fov))
    t.goto(*perspectiveMap(24,base+9,depth-20.8,fov))
    t.goto(*perspectiveMap(24,base+9,depth-14.4,fov))
    t.goto(*perspectiveMap(20,base+9,depth-14.4,fov))
    t.end_fill()
    goto(*perspectiveMap(20,base+9,depth-14.4,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(20,base,depth-35.8,fov))
    t.goto(*perspectiveMap(24,base,depth-35.8,fov))
    t.goto(*perspectiveMap(24,base+9,depth-20.8,fov))
    t.goto(*perspectiveMap(20,base+9,depth-20.8,fov))
    t.end_fill()


def towerLevel1():
    '''
    Lowest part of bell tower.
    '''
    t.fillcolor("#a3695d")
    goto(*perspectiveMap(-22.5,base+55,depth+12.5,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(22.5,base+55,depth+12.5,fov))
    t.goto(*perspectiveMap(22.5,base+97,depth+12.5,fov))
    t.goto(*perspectiveMap(-22.5,base+97,depth+12.5,fov))
    t.goto(*perspectiveMap(-22.5,base+55,depth+12.5,fov))
    t.end_fill()


def towerLevel1Trim():
    '''
    First trim band at top of towerLevel1()
    '''
    t.fillcolor("#f8f3ed")
    goto(*perspectiveMap(-22.5,base+97,depth+12.5,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(22.5,base+97,depth+12.5,fov))
    t.goto(*perspectiveMap(25,base+100,depth+10,fov))
    t.goto(*perspectiveMap(-25,base+100,depth+10,fov))
    t.goto(*perspectiveMap(-22.5,base+97,depth+12.5,fov))
    t.end_fill()
    goto(*perspectiveMap(-22.5,base+103,depth+12.5,fov))
    t.begin_fill()
    t.goto(*perspectiveMap(22.5,base+103,depth+12.5,fov))
    t.goto(*perspectiveMap(25,base+100,depth+10,fov))
    t.goto(*perspectiveMap(-25,base+100,depth+10,fov))
    t.goto(*perspectiveMap(-22.5,base+103,depth+12.5,fov))
    t.end_fill()


def towerLevel2():
    '''
    Second tower level.
    '''
    t.fillcolor("#f8f3ed")
    goto(*perspectiveMap(*hexPointer(0,base+109,depth+40,20,0,0,0,0),fov))
    #Second tier of second level.
    #Iterates through points at each angle of a hexagon.
    #Basically draws points between corresponding points (angles based) of two hexagons at differnt y.
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+109,depth+40,20,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+135,depth+40,20,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+135,depth+40,20,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+109,depth+40,20,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+109,depth+40,20,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+109,depth+40,20,0,0,0,1+count),fov))
    #First tier of second level.
    goto(*perspectiveMap(*hexPointer(0,base+103,depth+40,22,0,0,0,0),fov))
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+103,depth+40,22,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+109,depth+40,22,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+109,depth+40,22,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+103,depth+40,22,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+103,depth+40,22,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+103,depth+40,22,0,0,0,1+count),fov))
    #Draws 6 double nested rectangeles equidistant from a center at 60 degree increments.
    #Clock tower clock well.
    angledRectangle(0,base+124,depth+40,0,0,-10*m.sqrt(3),16,16,0,0,0)
    angledRectangle(0,base+124,depth+40.5,0,0,-10*m.sqrt(3),14,14,0,0,0)
    angledRectangle(0,base+124,depth+40,0,0,-10*m.sqrt(3),16,16,0,-60,0)
    angledRectangle(0,base+124,depth+40.5,0,0,-10*m.sqrt(3),14,14,0,-60,0)
    angledRectangle(0,base+124,depth+40,0,0,-10*m.sqrt(3),16,16,0,60,0)
    angledRectangle(0,base+124,depth+40.5,0,0,-10*m.sqrt(3),14,14,0,60,0)
    #Clock face.
    polarCircle(0,base+124,depth+40.5-10*m.sqrt(3),6,0,0,0)
    t.fillcolor("black")
    #Clock Center.
    t.begin_fill()
    polarCircle(0,base+124,depth+40-10*m.sqrt(3),1,0,0,0)
    t.end_fill()
    #Clock minute hand.
    t.begin_fill()
    angledRectangle(0,base+124,depth+40.5,0,-3,-10*m.sqrt(3),1,6,0,0,-30)
    t.end_fill()
    #Clock hour hand.
    t.begin_fill()
    angledRectangle(0,base+124,depth+40.5,0,-2,-10*m.sqrt(3),1,4,0,0,60)
    t.end_fill()


def towerLevel3():
    '''
    Third tower level.
    Trim baked in.
    '''
    #Trim top.
    t.fillcolor("#f8f3ed")
    goto(*perspectiveMap(*hexPointer(0,base+182.5,depth+40,17,0,0,0,0),fov))
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+182.5,depth+40,17,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+185,depth+40,13,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+185,depth+40,13,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+182.5,depth+40,17,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+182.5,depth+40,17,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+182.5,depth+40,17,0,0,0,1+count),fov))
    goto(*perspectiveMap(*hexPointer(0,base+180,depth+40,15,0,0,0,0),fov))
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+180,depth+40,15,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+182.5,depth+40,17,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+182.5,depth+40,17,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+180,depth+40,15,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+180,depth+40,15,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+180,depth+40,15,0,0,0,1+count),fov))
    #Trim bottom.
    goto(*perspectiveMap(*hexPointer(0,base+158.5,depth+40,18,0,0,0,0),fov))
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+158.5,depth+40,18,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+160,depth+40,15,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+160,depth+40,15,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+158.5,depth+40,18,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+158.5,depth+40,18,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+158.5,depth+40,18,0,0,0,1+count),fov))
    goto(*perspectiveMap(*hexPointer(0,base+157,depth+40,16,0,0,0,0),fov))
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+157,depth+40,16,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+158.5,depth+40,18,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+158.5,depth+40,18,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+157,depth+40,16,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+157,depth+40,16,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+157,depth+40,16,0,0,0,1+count),fov))
    #Second tier of tower level three.
    goto(*perspectiveMap(*hexPointer(0,base+160,depth+40,15,0,0,0,0),fov))
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+160,depth+40,15,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+180,depth+40,15,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+180,depth+40,15,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+160,depth+40,15,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+160,depth+40,15,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+160,depth+40,15,0,0,0,1+count),fov))
    #First tier of tower level three.
    goto(*perspectiveMap(*hexPointer(0,base+141.5,depth+40,16,0,0,0,0),fov))
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+141.5,depth+40,16,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+157,depth+40,16,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+157,depth+40,16,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+141.5,depth+40,16,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+141.5,depth+40,16,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+141.5,depth+40,16,0,0,0,1+count),fov))
    #Bell tower tier one door.
    windowBase(0,base+148,depth+40,0,0,-8*m.sqrt(3),0,11,8)
    #Bell tower tier two windows.
    windowArch(0,base+167,depth+40,0,0,-7.5*m.sqrt(3),0,14,8)
    windowArch(0,base+167,depth+40,0,0,-7.5*m.sqrt(3),-60,14,8)
    windowArch(0,base+167,depth+40,0,0,-7.5*m.sqrt(3),60,14,8)


def towerLevel5():
    '''
    Bell tower cupula if I'm not mistaken.
    '''
    t.fillcolor("#4e4241")
    #Top spike.
    t.begin_fill()
    goto(*perspectiveMap(*hexPointer(0,base+230,depth+40,6,0,0,0,0),fov))
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+230,depth+40,6,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+260,depth+40,0,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+260,depth+40,0,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+230,depth+40,6,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+230,depth+40,6,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+230,depth+40,6,0,0,0,1+count),fov))
    #Cupula.
    goto(*perspectiveMap(*hexPointer(0,base+215,depth+40,11,0,0,0,0),fov))
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+215,depth+40,11,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+230,depth+40,6,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+230,depth+40,6,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+215,depth+40,11,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+215,depth+40,11,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+215,depth+40,11,0,0,0,1+count),fov))
    t.end_fill()
    #Trim.
    goto(*perspectiveMap(*hexPointer(0,base+212.5,depth+40,11,0,0,0,0),fov))
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+212.5,depth+40,11,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+215,depth+40,14,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+215,depth+40,14,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+212.5,depth+40,11,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+212.5,depth+40,11,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+212.5,depth+40,11,0,0,0,1+count),fov))
    goto(*perspectiveMap(*hexPointer(0,base+210,depth+40,12,0,0,0,0),fov))
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+210,depth+40,12,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+212.5,depth+40,14,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+212.5,depth+40,14,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+210,depth+40,12,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+210,depth+40,12,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+210,depth+40,12,0,0,0,1+count),fov))
    


def towerLevel4():
    '''
    Fourth tower level.
    Trim baked in. 
    '''
    t.fillcolor("#f8f3ed")
    #Second tier of tower level four.
    goto(*perspectiveMap(*hexPointer(0,base+200,depth+40,12,0,0,0,0),fov))
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+200,depth+40,12,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+210,depth+40,12,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+210,depth+40,12,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+200,depth+40,12,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+200,depth+40,12,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+200,depth+40,12,0,0,0,1+count),fov))
    #Trim.
    goto(*perspectiveMap(*hexPointer(0,base+200,depth+40,12,0,0,0,0),fov))
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+200,depth+40,12,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+197.5,depth+40,15,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+197.5,depth+40,15,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+200,depth+40,12,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+200,depth+40,12,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+200,depth+40,12,0,0,0,1+count),fov))
    goto(*perspectiveMap(*hexPointer(0,base+197.5,depth+40,15,0,0,0,0),fov))
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+197.5,depth+40,15,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+195,depth+40,13,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+195,depth+40,13,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+197.5,depth+40,15,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+197.5,depth+40,15,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+197.5,depth+40,15,0,0,0,1+count),fov))
    #First tier of tower level four.
    goto(*perspectiveMap(*hexPointer(0,base+185,depth+40,13,0,0,0,0),fov))
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+185,depth+40,13,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+195,depth+40,13,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+195,depth+40,13,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+185,depth+40,13,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+185,depth+40,13,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+185,depth+40,13,0,0,0,1+count),fov))    


def windowBase(x,y,z,xOff,yOff,zOff,angle,height,width):
    '''
    Draws a basic rectangular Window at (x,y,z)+(xOff,yOff,zOff) at an angle of y-Rotation relative the the y axis at (x,0,z).
    Complex Shape #1.
    '''
    #Glass.
    t.fillcolor("#51525e")
    t.begin_fill()
    angledRectangle(x,y,z,xOff,yOff,zOff,width,height,0,angle,0)
    t.end_fill()
    #Framing.
    t.fillcolor("#f8f3ed")
    t.begin_fill()
    angledRectangle(x,y,z,xOff,yOff,zOff,width/5.33,height,0,angle,0)
    t.end_fill()
    t.begin_fill()
    angledRectangle(x,y-height/6.1,z,xOff,yOff,zOff,width,height/7.33,0,angle,0)
    t.end_fill()
    t.begin_fill()
    angledRectangle(x,y+height/6.1,z,xOff,yOff,zOff,width,height/7.33,0,angle,0)
    t.end_fill()


def windowArch(x,y,z,xOff,yOff,zOff,angle,height,width):
    '''
    Draws a arched rectangular Window at (x,y,z)+(xOff,yOff,zOff) at an angle of y-Rotation relative the the y axis at (x,0,z).
    Complex SHape #2.
    '''
    t.fillcolor("#51525e")
    t.begin_fill()
    polarCirclOffset(x,y+height/2,z,zOff,width/2,0,angle,0)
    t.end_fill()
    t.begin_fill()
    angledRectangle(x,y,z,xOff,yOff,zOff,width,height,0,angle,0)
    t.end_fill()
    t.fillcolor("#f8f3ed")
    t.begin_fill()
    angledRectangle(x,y+width/4,z,xOff,yOff,zOff,width/5.33,height+width/2,0,angle,0)
    t.end_fill()
    t.begin_fill()
    angledRectangle(x,y+width/8-(height+width/2)/10,z,xOff,yOff,zOff,width,(height+width/2)/12,0,angle,0)
    t.end_fill()
    t.begin_fill()
    angledRectangle(x,y+width/8+(height+width/2)/10,z,xOff,yOff,zOff,width,(height+width/2)/12,0,angle,0)
    t.end_fill()
    t.begin_fill()
    angledRectangle(x,y+width/8+3*(height+width/2)/10,z,xOff,yOff,zOff,width,(height+width/2)/12,0,angle,0)
    t.end_fill()
    t.begin_fill()
    angledRectangle(x,y+width/8-3*(height+width/2)/10,z,xOff,yOff,zOff,width,(height+width/2)/12,0,angle,0)
    t.end_fill()


def towerLevel2Trim():
    '''
    Trim for tower leve two.
    '''
    t.fillcolor("#f8f3ed")
    goto(*perspectiveMap(*hexPointer(0,base+138.25,depth+40,23,0,0,0,0),fov))
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+138.25,depth+40,23,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+141.5,depth+40,20,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+141.5,depth+40,20,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+138.25,depth+40,23,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+138.25,depth+40,23,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+138.25,depth+40,20,0,0,0,1+count),fov))
    goto(*perspectiveMap(*hexPointer(0,base+135,depth+40,20,0,0,0,0),fov))
    for count in range(6):
        t.begin_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+135,depth+40,20,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+138.25,depth+40,23,0,0,0,count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+138.25,depth+40,23,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+135,depth+40,20,0,0,0,1+count),fov))
        t.goto(*perspectiveMap(*hexPointer(0,base+135,depth+40,20,0,0,0,count),fov))
        t.end_fill()
        t.goto(*perspectiveMap(*hexPointer(0,base+135,depth+40,20,0,0,0,1+count),fov))
        
    
def angledRectangle(xCenter,yCenter,zCenter,xAxis,yAxis,zAxis,width,height,xRot,yRot,zRot):
    '''
    Prtty simple draws width*height rectangle centered at (x,y,z)+(xOff,yOff,zOff) at an angle of y-Rotation relative the the y axis at (x,0,z).
    Simple shape #1.
    '''
    bottomRight = tuple(np.reshape(np.array([fullTransform(width/2+xAxis,-height/2+yAxis,zAxis,xRot,yRot,zRot)])+np.array([xCenter,yCenter,zCenter]),3))
    bottomLeft = tuple(np.reshape(np.array([fullTransform(-width/2+xAxis,-height/2+yAxis,zAxis,xRot,yRot,zRot)])+np.array([xCenter,yCenter,zCenter]),3))
    topRight = tuple(np.reshape(np.array([fullTransform(width/2+xAxis,height/2+yAxis,zAxis,xRot,yRot,zRot)])+np.array([xCenter,yCenter,zCenter]),3))
    topLeft = tuple(np.reshape(np.array([fullTransform(-width/2+xAxis,height/2+yAxis,zAxis,xRot,yRot,zRot)])+np.array([xCenter,yCenter,zCenter]),3))
    goto(*perspectiveMap(*bottomRight,fov))
    t.goto(*perspectiveMap(*bottomLeft,fov))
    t.goto(*perspectiveMap(*topLeft,fov))
    t.goto(*perspectiveMap(*topRight,fov))
    t.goto(*perspectiveMap(*bottomRight,fov))


def hexPointer(xCenter,yCenter,zCenter,sideLength,xRot,yRot,zRot,counter):
    '''
    Polar defined hexagon function converted to cartesian coordinates, returns value considering all rotations and at specific 60 degree counter point.
    '''
    deg = 60*counter
    # unit conversion because radians.
    theta = m.radians(deg)
    # polar function converted to cartesian coordinates
    x = sideLength*m.cos(theta)
    y = 0
    z = sideLength*m.sin(theta)
    #3D rotation.
    point_pre = fullTransform(x,y,z,xRot,yRot,zRot)
    #Add points as vectors.
    point = np.array([point_pre]) + np.array([(xCenter,yCenter,zCenter)])
    #Convert to tuple.
    point=np.reshape(point,3)
    point=tuple(point)
    return point
