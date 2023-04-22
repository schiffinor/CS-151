'''
compound_shapes.py
Roman Schiffino 151B Fall Semester
This is my module file for project number 5. 
The functions contained here are all awfully math intensive and difficult to commentate, but I've done my best.
'''


import graphicsPlus as gr
import numpy as np
import math as m
import tkinter as tk
import inspect as ins
import statistics as s
import time as t
import random as r
import bisect as b


# Variable that must exist globally.
fov = 360


if __name__ == '__main__':
    # This is just o not make a mess of things so that my variables work and so that two windows aren't opened.
    width = 1540
    height = 870
    # Honestly this logo is barely viible but I made the effort so here it is.
    logo = tk.PhotoImage(file="Project05\Daco_6135086.png")
    screen = gr.GraphWin("Yeah, We Doin' a Project.'", width=width, height=height, autoflush=False)
    

def compColor(hexColor):
    '''
    This gets the complement to the initial color. 
    It is effectively the oposite or negative color. 
    That is that 255,255,255 "white" is the inputted color plus the returned color.
    Oh also I modified the Graphics plus package, getFill() command to return hex instead of tuples.
    This is because I prefer hex.
    ''' 
    # This takes an inputted string and removes the #
    modif = hexColor.lstrip("#")
    # Turns hex code into tuples in 255 format.
    tupColor = (int(modif[0:2], 16), int(modif[2:4], 16), int(modif[0:2], 16))
    # Calculates the complement color.
    complementColor = tuple(int(255-tupColor[i]) for i in range(len(tupColor)))
    # reformats tuple as hex.
    hexFormat = '#{:02x}{:02x}{:02x}'.format(*complementColor)
    # Returns hex color.
    return hexFormat


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
    This function basically takes any point in my "made up" 3d coordinate 
    system and converts it into 2d screen coordinates.
    '''
    xProj = ((x)*(fov/z))
    yProj = ((y)*(fov/z))
    return (xProj,yProj)


def fullTransform(x,y,z,theta1,theta2,theta3):
    '''
    This function really just combines the three rotation functions to be slightly more 
    concise in the many occasions where all 3 are called on the same point.
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
    output = []
    # polar defined circle function converted to cartesian coordinates
    for deg in range(0,360):
    # unit conversion because radians.
        theta = m.radians(deg)
    # polar function converted to cartesian coordinates
        x = r*m.cos(theta)
        y = r*m.sin(theta)
    # removes initial origin line
        output.append(perspectiveMap(*tuple(np.reshape(np.array([fullTransform(x,y,0,xRot,yRot,zRot)])+np.array([xCenter,yCenter,zCenter]),3)),fov))
    return output


def polarCirclOffset(xCenter,yCenter,zCenter,zOff,r,xRot,yRot,zRot):
    '''
    Basically the same as the original polarCircle() function except for the fact that you can set the position of the axes of revolution.
    very useful in automating the drawing of many circles equidistant from a center.
    '''
    output = []
    # polar defined circle function converted to cartesian coordinates
    for deg in range(0,360):
    # unit conversion because radians.
        theta = m.radians(deg)
    # polar function converted to cartesian coordinates
        x = r*m.cos(theta)
        y = r*m.sin(theta)
    # removes initial origin line
        output.append(perspectiveMap(*tuple(np.reshape(np.array([fullTransform(x,y,zOff,xRot,yRot,zRot)])+np.array([xCenter,yCenter,zCenter]),3)),fov))
        return output


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


def getRelRad(sideCount, sideLength):
    '''
    This is a function that gets the radius between  a point at the center of a face of a polygon
    and the center of said polygon. 
    '''
    rad = (sideLength/2)/(m.tan(m.radians(180)/sideCount))
    return rad


def getInfRad(sideCount, sideLength):
    '''
    Uhhh, do I remember my naming scheme... no. Can I ecplain what this does?
    Sure, basically this defines radius as the length between 
    the center of the pillar and one of its edges.
    '''
    rad = (sideLength/2)/(m.sin(m.radians(180)/sideCount))
    return rad



def polyPoint2(sideCount,xCenter,yCenter,zCenter,sideLength,xRot,yRot,zRot,counter):
    '''
    This is the first function in the polypoint series. Basically you define a side count (ie tpye of polygon),
    a side length then (x,y,z) for centers, and rotations. FYI for this function only yRot is effective.
    Anyhow, you put in a counter value and it gives a point at counter*(360/sidecount) starting from mathematical
    0 degrees on the xz-plane.
    '''
    degPer = 360/sideCount
    deg = degPer*counter
     # unit conversion because radians.
    theta = m.radians(deg)
    rad = getInfRad(sideCount, sideLength)
    # polar function converted to cartesian coordinates
    x = rad*m.cos(theta)
    y = 0
    z = rad*m.sin(theta)
    #3D rotation.
    point_pre = fullTransform(x,y,z,xRot,yRot,zRot)
    #Add points as vectors.
    point = np.array([point_pre]) + np.array([(xCenter,yCenter,zCenter)])
    #Convert to tuple.
    point=np.reshape(point,3)
    point=tuple(point)
    return point


def sidePolyPoint2(sideCount,xCenter,yCenter,zCenter,sideLength,xRot,yRot,zRot,counter):
    '''
    This is the second function in the polypoint series. Basically you define a side count (ie tpye of polygon),
    a side length then (x,y,z) for centers, and rotations. FYI for this function only xRot is effective.
    Anyhow, you put in a counter value and it gives a point at counter*(360/sidecount) starting from mathematical
    0 degrees on the yz-plane.
    '''
    degPer = 360/sideCount
    deg = degPer*counter
     # unit conversion because radians.
    theta = m.radians(deg)
    rad = getInfRad(sideCount, sideLength)
    # polar function converted to cartesian coordinates
    x = 0
    y = rad*m.cos(theta)
    z = rad*m.sin(theta)
    #3D rotation.
    point_pre = fullTransform(x,y,z,xRot,yRot,zRot)
    #Add points as vectors.
    point = np.array([point_pre]) + np.array([(xCenter,yCenter,zCenter)])
    #Convert to tuple.
    point=np.reshape(point,3)
    point=tuple(point)
    return point


def frontPolyPoint2(sideCount,xCenter,yCenter,zCenter,sideLength,xRot,yRot,zRot,counter):
    '''
    This is the third function in the polypoint series. Basically you define a side count (ie tpye of polygon),
    a side length then (x,y,z) for centers, and rotations. FYI for this function only zRot is effective.
    Anyhow, you put in a counter value and it gives a point at counter*(360/sidecount) starting from mathematical
    0 degrees on the xy-plane.
    '''
    degPer = 360/sideCount
    deg = degPer*counter
     # unit conversion because radians.
    theta = m.radians(deg)
    rad = getInfRad(sideCount, sideLength)
    # polar function converted to cartesian coordinates
    x = rad*m.cos(theta)
    y = rad*m.sin(theta)
    z = 0
    #3D rotation.
    point_pre = fullTransform(x,y,z,xRot,yRot,zRot)
    #Add points as vectors.
    point = np.array([point_pre]) + np.array([(xCenter,yCenter,zCenter)])
    #Convert to tuple.
    point=np.reshape(point,3)
    point=tuple(point)
    return point


def polyPoint3(sideCount,xCenter,yCenter,zCenter,sideLength,xRot,yRot,zRot,counter):
    '''
    This is the fourth function in the polypoint series. Basically you define a side count (ie tpye of polygon),
    a side length then (x,y,z) for centers, and rotations. FYI for this function only yRot is effective.
    Anyhow, you put in a counter value and it gives a point at counter*(360/sidecount) starting from mathematical
    0 degrees on the xz-plane. The only difference between this and polypoint2 is the fact that this appends an extra set of data
    to the output. The direction the ray is cast at (ie theta).
    '''
    degPer = 360/sideCount
    deg = degPer*counter
     # unit conversion because radians.
    theta = m.radians(deg)
    rad = getInfRad(sideCount, sideLength)
    # polar function converted to cartesian coordinates
    x = rad*m.cos(theta)
    y = 0
    z = rad*m.sin(theta)
    #3D rotation.
    point_pre = fullTransform(x,y,z,xRot,yRot,zRot)
    #Add points as vectors.
    point = np.array([point_pre]) + np.array([(xCenter,yCenter,zCenter)])
    #Convert to tuple.
    point=np.reshape(point,3)
    point=tuple(point)
    point = point + (theta,)
    return point


def polyPoint4(sideCount,xCenter,yCenter,zCenter,sideLength,xRot,yRot,zRot,counter):
    '''
    This is the fourth function in the polypoint series. Basically you define a side count (ie tpye of polygon),
    a side length then (x,y,z) for centers, and rotations. FYI for this function only yRot is effective.
    Anyhow, you put in a counter value and it gives a point at counter*(360/sidecount) starting from mathematical
    0 degrees on the xz-plane. The only difference between this and polypoint2 is the fact that this appends an extra set of data
    to the output the direction the ray is cast at (ie theta), that it, for some reason I can no longer remember, adds a 45 degree
    offset to the degree count, finally it uses the relRad function defined earlier.
    '''
    degPer = 360/sideCount
    deg = degPer*counter
     # unit conversion because radians.
    theta = m.radians(45+deg)
    rad = getRelRad(sideCount, sideLength)
    # polar function converted to cartesian coordinates
    x = rad*m.cos(theta)
    y = 0
    z = rad*m.sin(theta)
    #3D rotation.
    point_pre = fullTransform(x,y,z,xRot,yRot,zRot)
    #Add points as vectors.
    point = np.array([point_pre]) + np.array([(xCenter,yCenter,zCenter)])
    #Convert to tuple.
    point=np.reshape(point,3)
    point=tuple(point)
    point = point + (theta,)
    return point


def pillar_init(sideCount,x,y,z,sideLength,height,xRot,yRot,zRot,color):
    '''
    Woohoo, this is the first 3D graphics zelle function I've written. Basically it uses polypoint2 to define however many
    polygons defined by sidecount for the pillar. These polygons are named using some handy string and python functions to 
    ensure that the functions are more easily callable and recognizable for troubleshooting and faux-lighting purposes. To
    be honest most of the parameters are just directly passed to polypoint2. I think the code is pretty self explanatory.
    If its hard to understand, I don't believe words are super effective in explaining this and pictures work better, I 
    honestly drew everything out to figure it out.
    '''
    # Creates an empty list to temporarily store all our polygons for the pillar shape. This is necessary so that we can handle clipping better.
    tempList = []
    for count in range(sideCount):
        point1 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y,z,sideLength,xRot,yRot,zRot,count),fov))
        point2 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y+height,z,sideLength,xRot,yRot,zRot,count),fov))
        point3 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y+height,z,sideLength,xRot,yRot,zRot,1+count),fov))
        point4 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y,z,sideLength,xRot,yRot,zRot,1+count),fov))
        # Wow dynamically named variables epic.
        pillarNameFace = "pillarFace" + str(count+1)
        globals()[pillarNameFace] = gr.Polygon(point1,point2,point3,point4)
        # Wow coloring, I attempt to create artificial lighting by changine the color order for all of these functions. It's honestly hard to explain so I won't.
        globals()[pillarNameFace].setFill(color[count])
        tempList.append(globals()[pillarNameFace])
        print(globals()[pillarNameFace])


def sidePillar_init(sideCount,x,y,z,sideLength,height,xRot,yRot,zRot,color):
    '''
    This is like pillar_init except it creates a pillar parallel the x-axis. Basically it uses polypoint2 to define however
    many polygons defined by sidecount for the pillar. These polygons are named using some handy string and python functions
    to ensure that the functions are more easily callable and recognizable for troubleshooting and faux-lighting purposes.
    To be honest most of the parameters are just directly passed to polypoint2. I think the code is pretty self explanatory.
    If its hard to understand, I don't believe words are super effective in explaining this and pictures work better, I 
    honestly drew everything out to figure it out. Oh, also because this clips differently based on y coordinates we had to 
    add a if statement to handle clipping order based on y position. Essentially clipping order means if there is overlap we
    need to draw the things that are in front last. 
    '''
    # Creates an empty list to temporarily store all our polygons for the pillar shape. This is necessary so that we can handle clipping better.
    tempList = []
    # Here is that if statement I mentioned.
    if y >= 0:
        # Basically we do -1 so that clipping works right.
        for count in range(-1,sideCount-1):
            point1 = gr.Point(*perspectiveMap(*sidePolyPoint2(sideCount,x,y,z,sideLength,xRot,yRot,zRot,count),fov))
            point2 = gr.Point(*perspectiveMap(*sidePolyPoint2(sideCount,x+height,y,z,sideLength,xRot,yRot,zRot,count),fov))
            point3 = gr.Point(*perspectiveMap(*sidePolyPoint2(sideCount,x+height,y,z,sideLength,xRot,yRot,zRot,1+count),fov))
            point4 = gr.Point(*perspectiveMap(*sidePolyPoint2(sideCount,x,y,z,sideLength,xRot,yRot,zRot,1+count),fov))
            # More dynamically named variables wow!
            sidePillarNameFace = "sidePillarFace" + str(count+1)
            globals()[sidePillarNameFace] = gr.Polygon(point1,point2,point3,point4)
            # Wow coloring.
            globals()[sidePillarNameFace].setFill(color[count+1])
            tempList.append(globals()[sidePillarNameFace])
            print(sidePillarNameFace)
            print(globals()[sidePillarNameFace])
    else:
        # Here clipping does work well as is so remains unchanged.
        for count in range(sideCount):
            point1 = gr.Point(*perspectiveMap(*sidePolyPoint2(sideCount,x,y,z,sideLength,xRot,yRot,zRot,count),fov))
            point2 = gr.Point(*perspectiveMap(*sidePolyPoint2(sideCount,x+height,y,z,sideLength,xRot,yRot,zRot,count),fov))
            point3 = gr.Point(*perspectiveMap(*sidePolyPoint2(sideCount,x+height,y,z,sideLength,xRot,yRot,zRot,1+count),fov))
            point4 = gr.Point(*perspectiveMap(*sidePolyPoint2(sideCount,x,y,z,sideLength,xRot,yRot,zRot,1+count),fov))
            # Huzzah, even more dynamically named variables.
            sidePillarNameFace = "sidePillarFace" + str(count+1)
            globals()[sidePillarNameFace] = gr.Polygon(point1,point2,point3,point4)
            # Wow coloring.
            globals()[sidePillarNameFace].setFill(color[count])
            tempList.append(globals()[sidePillarNameFace])
            print(sidePillarNameFace)
            print(globals()[sidePillarNameFace])


def frontPillar_init(sideCount,x,y,z,sideLength,height,xRot,yRot,zRot,color):
    '''
    This is again like pillar_init except it creates a pillar parallel the z-axis. Basically it uses polypoint2 to define however
    many polygons defined by sidecount for the pillar. These polygons are named using some handy string and python functions
    to ensure that the functions are more easily callable and recognizable for troubleshooting and faux-lighting purposes.
    To be honest most of the parameters are just directly passed to polypoint2. I think the code is pretty self explanatory.
    If its hard to understand, I don't believe words are super effective in explaining this and pictures work better, I 
    honestly drew everything out to figure it out. Oh, also because this clips differently based on y coordinates we had to 
    add a if statement to handle clipping order based on y position. Essentially clipping order means if there is overlap we
    need to draw the things that are in front last.
    '''
    tempList = []
    # Yet another clipping mess to be solved by if statements.
    # Also I try to make my commenting somewhat entertaining because I know my projects are really long and can be somewhat hard to read. Thanks for taking the time.
    if y >= 0:
        # Again -1 for clipping handling.
        for count in range(-1,sideCount-1):
            point1 = gr.Point(*perspectiveMap(*frontPolyPoint2(sideCount,x,y,z,sideLength,xRot,yRot,zRot,count),fov))
            point2 = gr.Point(*perspectiveMap(*frontPolyPoint2(sideCount,x,y,z-height,sideLength,xRot,yRot,zRot,count),fov))
            point3 = gr.Point(*perspectiveMap(*frontPolyPoint2(sideCount,x,y,z-height,sideLength,xRot,yRot,zRot,1+count),fov))
            point4 = gr.Point(*perspectiveMap(*frontPolyPoint2(sideCount,x,y,z,sideLength,xRot,yRot,zRot,1+count),fov))
            # Wow do these dynamically named variables get old?
            frontPillarNameFace = "frontPillarFace" + str(count+1)
            globals()[frontPillarNameFace] = gr.Polygon(point1,point2,point3,point4)
            # Wow coloring.
            globals()[frontPillarNameFace].setFill(color[count+1])
            tempList.append(globals()[frontPillarNameFace])
            print(frontPillarNameFace)
            print(globals()[frontPillarNameFace])
    else:
        # Works as is, lets go.
        for count in range(sideCount):
            point1 = gr.Point(*perspectiveMap(*frontPolyPoint2(sideCount,x,y,z,sideLength,xRot,yRot,zRot,count),fov))
            point2 = gr.Point(*perspectiveMap(*frontPolyPoint2(sideCount,x,y,z-height,sideLength,xRot,yRot,zRot,count),fov))
            point3 = gr.Point(*perspectiveMap(*frontPolyPoint2(sideCount,x,y,z-height,sideLength,xRot,yRot,zRot,1+count),fov))
            point4 = gr.Point(*perspectiveMap(*frontPolyPoint2(sideCount,x,y,z,sideLength,xRot,yRot,zRot,1+count),fov))
            # Even more dynamically named variables. These are totally not the same function recycled for different uses.
            frontPillarNameFace = "frontPillarFace" + str(count+1)
            globals()[frontPillarNameFace] = gr.Polygon(point1,point2,point3,point4)
            # Wow coloring.
            globals()[frontPillarNameFace].setFill(color[count])
            tempList.append(globals()[frontPillarNameFace])
            print(frontPillarNameFace)
            print(globals()[frontPillarNameFace])


def polyFrustrum(sideCount,x,y,z,sideLengthTop,sideLengthBottom,height,xRot,yRot,zRot,color):
    '''
    A nicer more convnient version of the function below. However, less viable and mosular. Basically contructs a frustrum of however many sides,
    of whatever sidelengths (top and bottom), at whatever rotation (not really on this one you can only really rotate y) 
    as you saw in y I have to make a new version of poly point and aeverything else to handle z or x properly.
    '''
    tempList = []
    # Ahhhh clipping for some reason now requires me to make it a +1, there is rhyme and reason to it; however, I just coded, saw if it worked, if it didn't I just trouble-shot.
    for count in range(1,sideCount+1):
        point1 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,count),fov))
        point2 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,count),fov))
        point3 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,1+count),fov))
        point4 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,1+count),fov))
        # I don't even know what to say, even more dynamically named variables.
        pillarNameFace = "pillarFace" + str(count+1)
        globals()[pillarNameFace] = gr.Polygon(point1,point2,point3,point4)
        # Wow coloring.
        globals()[pillarNameFace].setFill(color[count-1])
        tempList.append(globals()[pillarNameFace])
        print(globals()[pillarNameFace])


def polyFrustrumClipMask(sideCount,x,y,z,sideLengthTop,sideLengthBottom,height,xRot,yRot,zRot,color):
    '''
    Haha! A great source of convenience and inconvenience very paradoxical; regardless, basically this creates our frustrums. But does not add 
    any shape with any point existng at z<=0 to the draw list. Works almost exactly as you might expect.
    '''
    tempList = []
    # Hey thats pretty nice, clipping luickily works as it does above, lets hope it stays that way... It won't but hey we can hope.
    for count in range(1,sideCount+1):
        point1 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,count),fov))
        point2 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,count),fov))
        point3 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,1+count),fov))
        point4 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,1+count),fov))
        # This is getting repetitive, dynamically named variables.
        pillarNameFace = "pillarFace" + str(count+1)
        globals()[pillarNameFace] = gr.Polygon(point1,point2,point3,point4)
        # Wow coloring.
        globals()[pillarNameFace].setFill(color[count-1])
        # Lo and behold, clipping handling. Basically this awfully long boolean checks whether the z-coordinate for any of the points in a polygon face are less than or equal to 0 before adding it to the list.
        # We have to do this because anything drawn at z = 0 will throw an error because you can't divide by 0 (look at perspective map to understand), if any point is drawn at z < 0,
        # then it just draws something weird because your asking the renderer to draw something that exists behind the camera. I wish I had just coded it to truncate the shape; however, it's too late for that.
        if polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,count)[2] >= 0 and polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,count)[2] >= 0 and polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,1+count)[2] >= 0 and polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,1+count)[2] >= 0: 
            tempList.append(globals()[pillarNameFace])
        print(globals()[pillarNameFace])
    # This is made to handle a clipping issue below. Basically the issue is that I used the outline function to differentiate windows from their frames.
    # However, I had hoped that the width of the outline had a maximum bound of defined polygon, unfortunately it actually just kind of works like an outward glow.
    # This results in overlap and as such clipping. I avoid that by just rendering an empty boundinmg box the same size as the original polygon just over the same shape.
    # Same clipping handling as above.
    for count in range(1,sideCount+1):
        point1 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,count),fov))
        point2 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,count),fov))
        point3 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,1+count),fov))
        point4 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,1+count),fov))
        # Dynamically named variables.
        pillarSubFace = "pillarSubFace" + str(count+1)
        globals()[pillarSubFace] = gr.Polygon(point1,point2,point3,point4)
        # Same basic clipping handleing as seen above.
        if polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,count)[2] >= 0 and polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,count)[2] >= 0 and polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,1+count)[2] >= 0 and polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,1+count)[2] >= 0:
            tempList.append(globals()[pillarSubFace])


def polyFrustrumWindowClipMask(sideCount,x,y,z,sideLengthTop,sideLengthBottom,height,xRot,yRot,zRot,colorFill,colorOutline):
    '''
    Yet another thing that excitedly does not work as intended so I honestly just found a cheap solution around. Baically unfortunately if I am to increase the outline of the shape 
    it functions more like a general glow rather tan the internal glow I had hoped for. As such it messed up clipping. 
    Thus I just threw the subface on everything (empty overlay of same shape). And threw the call for this function lower in the load order.
    Honestly this solution honestly just came to me becaus of my experience modding games, (just overwrite anything that you don't want to see. "incredible practice ikr definitely never leads to issues")
    '''
    tempList = []
    # Pretty much the exact same thing as seen above (as above being polyFrustrumClipmask()). So I won't get into detail, just explaining the basics.
    for count in range(1,sideCount+1):
        point1 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,count),fov))
        point2 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,count),fov))
        point3 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,1+count),fov))
        point4 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,1+count),fov))
        # Dynamically named variables.
        pillarNameFace = "pillarFace" + str(count+1)
        globals()[pillarNameFace] = gr.Polygon(point1,point2,point3,point4)
        # This sets the inner window glass color.
        globals()[pillarNameFace].setFill(colorFill[count-1])
        # This sets the window frame color.
        globals()[pillarNameFace].setOutline(colorOutline[count-1])
        # This sets the size of the window frame.
        globals()[pillarNameFace].setWidth(15)
        # Same clipping mask as defined a couple times before.
        if polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,count)[2] >= 0 and polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,count)[2] >= 0 and polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,1+count)[2] >= 0 and polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,1+count)[2] >= 0: 
            tempList.append(globals()[pillarNameFace])
    # Same bounding box fix as defined earlier for similar reasons.    
    for count in range(1,sideCount+1):
        point1 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,count),fov))
        point2 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,count),fov))
        point3 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,1+count),fov))
        point4 = gr.Point(*perspectiveMap(*polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,1+count),fov))
        # Dynamically renamed variables.
        pillarSubFace = "pillarSubFace" + str(count+1)
        globals()[pillarSubFace] = gr.Polygon(point1,point2,point3,point4)
        # Same clipping mask.
        if polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,count)[2] >= 0 and polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,count)[2] >= 0 and polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,1+count)[2] >= 0 and polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,1+count)[2] >= 0:
            tempList.append(globals()[pillarSubFace])


def rotatorator(x,y,z,xCen,yCen,zCen,xRot,yRot,zRot):
    radialPoint = np.array([(x,y,z)]) - np.array([(xCen,yCen,zCen)])
    point = np.reshape(radialPoint,3)
    point = tuple(point)
    point = fullTransform(*point,xRot,yRot,zRot)
    point = np.array([(point)]) + np.array([(xCen,yCen,zCen)])
    point = np.reshape(point,3)
    point = tuple(point)
    return point


def pillar_v3(sideCount,x,y,z,sideLength,height,xRot,yRot,zRot,yPointPreRotator,color,varName=None):
    '''
    Woohoo, this is the first 3D graphics zelle function I've written. Basically it uses polypoint2 to define however many
    polygons defined by sidecount for the pillar. These polygons are named using some handy string and python functions to 
    ensure that the functions are more easily callable and recognizable for troubleshooting and faux-lighting purposes. To
    be honest most of the parameters are just directly passed to polypoint2. I think the code is pretty self explanatory.
    If its hard to understand, I don't believe words are super effective in explaining this and pictures work better, I 
    honestly drew everything out to figure it out.
    '''
    # Creates an empty list to temporarily store all our polygons for the pillar shape. This is necessary so that we can handle clipping better.
    tempList = []
    tempShapeList = []
    radList = []
    clipList = []
    faceList = []
    orderedFaceList = []
    for count in range(sideCount):
        prePoint1 = rotatorator(*polyPoint2(sideCount,x,y-(1/2)*height,z,sideLength,0,yPointPreRotator,0,count),x,y,z,xRot,yRot,zRot,height)
        if prePoint1[2] <= 0:
            prePoint1 = rotatorator(*polyPoint2(sideCount,x,y-z+1,z,sideLength,0,yPointPreRotator,0,count),x,y,z,xRot,yRot,zRot,height)
        prePoint2 = rotatorator(*polyPoint2(sideCount,x,y+(1/2)*height,z,sideLength,0,yPointPreRotator,0,count),x,y,z,xRot,yRot,zRot,height)
        if prePoint2[2] <= 0:
            prePoint2 = rotatorator(*polyPoint2(sideCount,x,y+z-1,z,sideLength,0,yPointPreRotator,0,count),x,y,z,xRot,yRot,zRot,height)
        prePoint3 = rotatorator(*polyPoint2(sideCount,x,y+(1/2)*height,z,sideLength,0,yPointPreRotator,0,1+count),x,y,z,xRot,yRot,zRot,height)
        if prePoint3[2] <= 0:
            prePoint3 = rotatorator(*polyPoint2(sideCount,x,y+z-1,z,sideLength,0,yPointPreRotator,0,1+count),x,y,z,xRot,yRot,zRot,height)
        prePoint4 = rotatorator(*polyPoint2(sideCount,x,y-(1/2)*height,z,sideLength,0,yPointPreRotator,0,1+count),x,y,z,xRot,yRot,zRot,height)
        if prePoint4[2] <= 0:
            prePoint4 = rotatorator(*polyPoint2(sideCount,x,y-z+1,z,sideLength,0,yPointPreRotator,0,1+count),x,y,z,xRot,yRot,zRot,height)
        aveRad =  max([(m.sqrt(((prePoint1[0])**2)+((prePoint1[1])**2)+((prePoint1[2])**2))),(m.sqrt(((prePoint2[0])**2)+((prePoint2[1])**2)+((prePoint2[2])**2))),(m.sqrt(((prePoint3[0])**2)+((prePoint3[1])**2)+((prePoint3[2])**2))),(m.sqrt(((prePoint4[0])**2)+((prePoint4[1])**2)+((prePoint4[2])**2)))])
        radList.append(aveRad)
        pointList = [prePoint1,prePoint2,prePoint3,prePoint4]
        faceList.append(pointList)
        point1 = gr.Point(*perspectiveMap(*prePoint1,fov))
        point2 = gr.Point(*perspectiveMap(*prePoint2,fov))
        point3 = gr.Point(*perspectiveMap(*prePoint3,fov))
        point4 = gr.Point(*perspectiveMap(*prePoint4,fov))
        # Wow dynamically named variables epic.
        pillarNameFace = "pillarFace" + str(count+1)
        globals()[pillarNameFace] = gr.Polygon(point1,point2,point3,point4)
        # Wow coloring, I attempt to create artificial lighting by changine the color order for all of these functions. It's honestly hard to explain so I won't.
        globals()[pillarNameFace].setFill(color[count])
        tempList.append(globals()[pillarNameFace])
    # Clipping is handled well by default here so we just append our templist as is to the main shapelist.
    clipper = list(zip(range(len(radList)),radList))
    clipper.sort(key = lambda zippedVal: zippedVal[1], reverse = True)
    for order in range(len(clipper)):
        clipList.append((clipper[order])[0])
        orderedFaceList.append(faceList[clipList[order]])
        tempShapeList.append(tempList[clipList[order]])
    if varName is not None:
        globals()[varName] = tempShapeList
        return globals()[varName]



def polyFrustrum_v3(sideCount,x,y,z,sideLengthTop,sideLengthBottom,height,xRot,yRot,zRot,yPointPreRotator,color,varName=None):
    '''
    A nicer more convnient version of the function below. However, less viable and mosular. Basically contructs a frustrum of however many sides,
    of whatever sidelengths (top and bottom), at whatever rotation (not really on this one you can only really rotate y) 
    as you saw in y I have to make a new version of poly point and aeverything else to handle z or x properly.
    '''
    tempList = []
    tempShapeList = []
    radList = []
    clipList = []
    faceList = []
    orderedFaceList = []
    # Ahhhh clipping for some reason now requires me to make it a +1, there is rhyme and reason to it; however, I just coded, saw if it worked, if it didn't I just trouble-shot.
    for count in range(sideCount):
        prePoint1 = rotatorator(*polyPoint2(sideCount,x,y,z,sideLengthBottom,0,yPointPreRotator,0,count),x,y,z,xRot,yRot,zRot,height)
        if prePoint1[2] <= 0:
            prePoint1 = rotatorator(*polyPoint2(sideCount,x,y,z,sideLengthBottom,0,yPointPreRotator,0,count),x,y,z,xRot,yRot,zRot,height)
        prePoint2 = rotatorator(*polyPoint2(sideCount,x,y+height,z,sideLengthTop,0,yPointPreRotator,0,count),x,y,z,xRot,yRot,zRot,height)
        if prePoint2[2] <= 0:
            prePoint2 = rotatorator(*polyPoint2(sideCount,x,y+z-1,z,sideLengthTop,0,yPointPreRotator,0,count),x,y,z,xRot,yRot,zRot,height)
        prePoint3 = rotatorator(*polyPoint2(sideCount,x,y+height,z,sideLengthTop,0,yPointPreRotator,0,1+count),x,y,z,xRot,yRot,zRot,height)
        if prePoint3[2] <= 0:
            prePoint3 = rotatorator(*polyPoint2(sideCount,x,y+z-1,z,sideLengthTop,0,yPointPreRotator,0,1+count),x,y,z,xRot,yRot,zRot,height)
        prePoint4 = rotatorator(*polyPoint2(sideCount,x,y,z,sideLengthBottom,0,yPointPreRotator,0,1+count),x,y,z,xRot,yRot,zRot,height)
        if prePoint4[2] <= 0:
            prePoint4 = rotatorator(*polyPoint2(sideCount,x,y,z,sideLengthBottom,0,yPointPreRotator,0,1+count),x,y,z,xRot,yRot,zRot,height)
        maxRad =  max([(m.sqrt(((prePoint1[0])**2)+((prePoint1[1])**2)+((prePoint1[2])**2))),(m.sqrt(((prePoint2[0])**2)+((prePoint2[1])**2)+((prePoint2[2])**2))),(m.sqrt(((prePoint3[0])**2)+((prePoint3[1])**2)+((prePoint3[2])**2))),(m.sqrt(((prePoint4[0])**2)+((prePoint4[1])**2)+((prePoint4[2])**2)))])
        radList.append(maxRad)
        pointList = [prePoint1,prePoint2,prePoint3,prePoint4]
        faceList.append(pointList)
        point1 = gr.Point(*perspectiveMap(*prePoint1,fov))
        point2 = gr.Point(*perspectiveMap(*prePoint2,fov))
        point3 = gr.Point(*perspectiveMap(*prePoint3,fov))
        point4 = gr.Point(*perspectiveMap(*prePoint4,fov))
        # I don't even know what to say, even more dynamically named variables.
        pillarNameFace = "pillarFace" + str(count+1)
        globals()[pillarNameFace] = gr.Polygon(point1,point2,point3,point4)
        # Wow coloring.
        globals()[pillarNameFace].setFill(color[count-1])
        tempList.append(globals()[pillarNameFace])
    clipper = list(zip(range(len(radList)),radList))
    clipper.sort(key = lambda zippedVal: zippedVal[1], reverse = True)
    for order in range(len(clipper)):
        clipList.append((clipper[order])[0])
        orderedFaceList.append(faceList[clipList[order]])
        tempShapeList.append(tempList[clipList[order]])
    if varName is not None:
        globals()[varName] = tempShapeList
        return globals()[varName]
    

def rocket_init_(sideCount,x,y,z,sideLengthTop,sideLengthBottom,heightCyl,heightCon,xRot,yRot,zRot,yPointPreRotator,color,varName=None,zVal=False):
    '''
    My newest abomination of code. Basically combines the frustrum and the pillar from before,
    adds a bunch of automatic clipping handling and some other cool features.
    It also outputs everything as a list, as do all my functions so that they can easily be moved, redrawn or erased quickly.

    This is compound shape 1.
    '''
    # Just initiating a bunch of lists.
    tempList = []
    tempShapeList = []
    radList = []
    clipList = []
    faceList = []
    orderedFaceList = []
    '''
    For loop that draws a plane of the rocket pillar body. There is a lot of clipping handling here, to be honest I'm not entirely sure how some of it even functions anymore, 
    but in the famous words of Todd Howard, "It just works." The basics however funtion under the premise of testing radius in various ways. If I remember there are three different 
    clipping handlers functioning simultaneously here. One checks the radius between the average value of a plane and the camera position (0,0,0). It then draws objects further from 
    the camera first and lets them be overlapped by the other shapes. The other determines whether a point on the polygon would clip into the near clipping plane (z=0), if it does it 
    will set that value to z=1. The third clipping handler is external and handles clipping between different objects in th frame. Ie mountains and rockets. That was added in later but 
    basically is why we have those two if statements at the bottom.partticiularily the second one. It outputs the z coordinat of the shape specifically for this purpose.
    '''
    for count in range(sideCount):
        # These for if statements are part of the near clipping plane clipping handler.
        prePoint1 = rotatorator(*polyPoint2(sideCount,x,y-(1/2)*heightCyl,z,sideLengthBottom,0,yPointPreRotator,0,count),x,y,z,xRot,yRot,zRot)
        if prePoint1[2] <= 0:
            prePoint1 = rotatorator(*polyPoint2(sideCount,x,y-z+1,z,sideLengthBottom,0,yPointPreRotator,0,count),x,y,z,xRot,yRot,zRot)
        prePoint2 = rotatorator(*polyPoint2(sideCount,x,y+(1/2)*heightCyl,z,sideLengthBottom,0,yPointPreRotator,0,count),x,y,z,xRot,yRot,zRot)
        if prePoint2[2] <= 0:
            prePoint2 = rotatorator(*polyPoint2(sideCount,x,y+z-1,z,sideLengthBottom,0,yPointPreRotator,0,count),x,y,z,xRot,yRot,zRot)
        prePoint3 = rotatorator(*polyPoint2(sideCount,x,y+(1/2)*heightCyl,z,sideLengthBottom,0,yPointPreRotator,0,1+count),x,y,z,xRot,yRot,zRot)
        if prePoint3[2] <= 0:
            prePoint3 = rotatorator(*polyPoint2(sideCount,x,y+z-1,z,sideLengthBottom,0,yPointPreRotator,0,1+count),x,y,z,xRot,yRot,zRot)
        prePoint4 = rotatorator(*polyPoint2(sideCount,x,y-(1/2)*heightCyl,z,sideLengthBottom,0,yPointPreRotator,0,1+count),x,y,z,xRot,yRot,zRot)
        if prePoint4[2] <= 0:
            prePoint4 = rotatorator(*polyPoint2(sideCount,x,y-z+1,z,sideLengthBottom,0,yPointPreRotator,0,1+count),x,y,z,xRot,yRot,zRot)
        # This is part of the radial clipping handler to detemine drawing precedence. This does all the radius calculations and makes a list of all these values tied to the list of faces.
        # These are then sent down to the stuff at the bottom to handle drawing order.
        aveRad =  max([(m.sqrt(((prePoint1[0])**2)+((prePoint1[1])**2)+((prePoint1[2])**2))),(m.sqrt(((prePoint2[0])**2)+((prePoint2[1])**2)+((prePoint2[2])**2))),(m.sqrt(((prePoint3[0])**2)+((prePoint3[1])**2)+((prePoint3[2])**2))),(m.sqrt(((prePoint4[0])**2)+((prePoint4[1])**2)+((prePoint4[2])**2)))])
        radList.append(aveRad)
        pointList = [prePoint1,prePoint2,prePoint3,prePoint4]
        faceList.append(pointList)
        # Standard point-setting and perspective mapping.
        point1 = gr.Point(*perspectiveMap(*prePoint1,fov))
        point2 = gr.Point(*perspectiveMap(*prePoint2,fov))
        point3 = gr.Point(*perspectiveMap(*prePoint3,fov))
        point4 = gr.Point(*perspectiveMap(*prePoint4,fov))
        # Wow dynamically named variables epic.
        pillarNameFace = "pillarFace" + str(count+1)
        globals()[pillarNameFace] = gr.Polygon(point1,point2,point3,point4)
        # Wow coloring, I attempt to create artificial lighting by changine the color order for all of these functions. It's honestly hard to explain so I won't.
        globals()[pillarNameFace].setFill(color[count])
        tempList.append(globals()[pillarNameFace])
    # Same deal as above this handles pointsetting and clipping for the top/cone of the rocket. These if statements handle interactions with the near clipping plane.
    for count in range(sideCount):
        prePoint1 = rotatorator(*polyPoint2(sideCount,x,y+(1/2)*heightCyl,z,sideLengthBottom,0,yPointPreRotator,0,count),x,y,z,xRot,yRot,zRot)
        if prePoint1[2] <= 0:
            prePoint1 = rotatorator(*polyPoint2(sideCount,x,y+(1/2)*heightCyl,z,sideLengthBottom,0,yPointPreRotator,0,count),x,y,z,xRot,yRot,zRot)
        prePoint2 = rotatorator(*polyPoint2(sideCount,x,y+(1/2)*heightCyl+heightCon,z,sideLengthTop,0,yPointPreRotator,0,count),x,y,z,xRot,yRot,zRot)
        if prePoint2[2] <= 0:
            prePoint2 = rotatorator(*polyPoint2(sideCount,x,y+(1/2)*heightCyl+z-1,z,sideLengthTop,0,yPointPreRotator,0,count),x,y,z,xRot,yRot,zRot)
        prePoint3 = rotatorator(*polyPoint2(sideCount,x,y+(1/2)*heightCyl+heightCon,z,sideLengthTop,0,yPointPreRotator,0,1+count),x,y,z,xRot,yRot,zRot)
        if prePoint3[2] <= 0:
            prePoint3 = rotatorator(*polyPoint2(sideCount,x,y+(1/2)*heightCyl+z-1,z,sideLengthTop,0,yPointPreRotator,0,1+count),x,y,z,xRot,yRot,zRot)
        prePoint4 = rotatorator(*polyPoint2(sideCount,x,y+(1/2)*heightCyl,z,sideLengthBottom,0,yPointPreRotator,0,1+count),x,y,z,xRot,yRot,zRot)
        if prePoint4[2] <= 0:
            prePoint4 = rotatorator(*polyPoint2(sideCount,x,y+(1/2)*heightCyl,z,sideLengthBottom,0,yPointPreRotator,0,1+count),x,y,z,xRot,yRot,zRot)
        # Same radial clipping handling as above.
        aveRad =  max([(m.sqrt(((prePoint1[0])**2)+((prePoint1[1])**2)+((prePoint1[2])**2))),(m.sqrt(((prePoint2[0])**2)+((prePoint2[1])**2)+((prePoint2[2])**2))),(m.sqrt(((prePoint3[0])**2)+((prePoint3[1])**2)+((prePoint3[2])**2))),(m.sqrt(((prePoint4[0])**2)+((prePoint4[1])**2)+((prePoint4[2])**2)))])
        radList.append(aveRad)
        pointList = [prePoint1,prePoint2,prePoint3,prePoint4]
        faceList.append(pointList)
        # Again pretty standard stuff all things considered. Setting points and handling perspective mapping.
        point1 = gr.Point(*perspectiveMap(*prePoint1,fov))
        point2 = gr.Point(*perspectiveMap(*prePoint2,fov))
        point3 = gr.Point(*perspectiveMap(*prePoint3,fov))
        point4 = gr.Point(*perspectiveMap(*prePoint4,fov))
        # I don't even know what to say, even more dynamically named variables.
        pillarNameFace = "pillarFace" + str(count+1)
        globals()[pillarNameFace] = gr.Polygon(point1,point2,point3,point4)
        # Wow coloring.
        globals()[pillarNameFace].setFill(color[count-1])
        tempList.append(globals()[pillarNameFace])
    # WoOooOhOoo terrible clipping handling LEEETTTSSSS GOOOOOOO! Anyways, basically what we do here we zip a range equal in length to the radius list to the radius list.
    clipper = list(zip(range(len(radList)),radList))
    # Now here is the fun bit. We use the sort method. The sort method can kind of have a mapping function built in in the form of our key function, except that it doesn't actually change values.
    # In any case we sort by the second value in the list, in reverse order from greatest to least. Pretty handy.
    clipper.sort(key = lambda zippedVal: zippedVal[1], reverse = True)
    # Now here we go through our clipperlist and append the index of the faces we want to draw in the order they should be drawn to our clipList. Then we create a list of the faces in the order they should be drawn using this same list.
    # Finally, we also do the same trhing to our temp shapelist so it can be outputted as a list with a name for animation purposes.
    for order in range(len(clipper)):
        clipList.append((clipper[order])[0])
        orderedFaceList.append(faceList[clipList[order]])
        tempShapeList.append(tempList[clipList[order]])
    # What to outpus if varName is specified.
    if varName is not None and zVal is False:
        globals()[varName] = tempShapeList
        return globals()[varName]
    # What to output if varName is specified and z values are requested.
    if varName is not None and zVal is True:
        globals()[varName] = (tempShapeList,z)
        return globals()[varName]


def mountainBackground_init(color=0,y=0,z=600,roughness=0,displacement=0,iterations=0,varName=None):
    '''
    Woohoo, this was actually pretty fun. Difficult, but fun. Honestly I had to read a blogpost to get the idea for this algorithm. However, the implementation is my own.
    However, I doubt the implementation is too different from others because its a pretty unique idea. Basically a midpoint bisection algorithm.

    Also FYI this is compound shape 2.
    '''
    # This determines the x coordinates of the bounds of the mountain ranges depending on visible x coordinates in this screenspace dependant on z coordinates.
    x1 = (-770)/(fov/z)
    x2 = (770)/(fov/z)
    # Initiates our terrain array.
    pointList = [[x1,y],[x2,y]]
    grPointList = []
    # Splits our line however many times specified in iterations.
    for i in range(iterations):
        # Turns list to tuple because tuple values are better for this math.
        workablePoints = tuple(pointList)
        for j in range(len(workablePoints)-1):
            # Calculates midpoint x coordinate.
            midx = (workablePoints[j][0]+workablePoints[j+1][0])/2
            # Calculates midpoint y coordinate.
            midy = (workablePoints[j][1]+workablePoints[j+1][1])/2
            # Bundles these two values into a list like all other points.
            midpoint = list((midx,midy))
            # Changes the y value of the list.
            midpoint[1] += r.randrange(-1,1)*displacement
            # Prevents negative values.
            if midpoint[1] < 0:
                midpoint[1] = -midpoint[1]
            # Puts the list into the right place in the list of lists. (Sorts by x coordinate.)
            b.insort(pointList,midpoint)
        # Lowers displacement paramater each iteration.
        displacement *= 2**(roughness)
    # Dynamically names and converts points to gr.Points. Then adds to grPointList.
    for i in range(len(pointList)):
        points = "point" + str(i+1)
        globals()[points] = tuple(pointList[i])
        grPoints = "grPoint" + str(i+1)
        globals()[grPoints] = gr.Point(*globals()[points])
        grPointList.append(globals()[grPoints])
    # Creates our desired polygon.
    backShape = gr.Polygon(*tuple(grPointList),gr.Point(x2,-10),gr.Point(x1,-10))
    # Sets color.
    backShape.setFill(color)
    # Handles naming when requested.
    if varName is not None:
        globals()[varName] = backShape
        return globals()[varName]


def floor(color,z=800):
    '''
    Super basic just creates afloor with parameters being the exact dimensions of the vewing screen.
    '''
    # Calculates dimnensions.
    xFramingBackLeft = (-770)/(fov/z)
    xFramingBackRight = (770)/(fov/z)
    xFramingFrontLeft = (-770)/(fov/1)
    xFramingFrontRight = (770)/(fov/1)
    # Sets points.
    prePoint1 = (xFramingBackLeft,-10,z)
    prePoint2 = (xFramingBackRight,-10,z)
    prePoint3 = (xFramingFrontRight,-10,1)
    prePoint4 = (xFramingFrontLeft,-10,1)
    # Creates Graphics Points.
    point1 = gr.Point(*perspectiveMap(*prePoint1,fov))
    point2 = gr.Point(*perspectiveMap(*prePoint2,fov))
    point3 = gr.Point(*perspectiveMap(*prePoint3,fov))
    point4 = gr.Point(*perspectiveMap(*prePoint4,fov))
    # Creates Polygon.
    floor = gr.Polygon(point1,point2,point3,point4)
    floor.setFill(color)
    return floor


def cactiBillboards_init(x,z,y=-10):
    """
    Another procedurally generated mess. "Works as expected, 100% of the time, 50% of the time." 
    In all seriousness, the only issue this occasionaly fgaces is that their is occasional branch overlay which I can't be bothered to fix.
    Basically, there is a 50% chance this will be either a 2 or 3 branched cactus. The paramaters for cactus height, branch lengths and the like
    are randomly chosen from ranges i arbitrarily deemed reasonable. Points are then calculated from these parameters and a polygon is constructed.
    They are then randomly placed at a random x dependent on a random z value.

    I guess we can call this compound shape 3.
    """
    # Parameters.
    heightTot = r.randint(15,25)
    branch1Height = r.randint(5,8)
    branch2Height = r.randint(4,7)
    branch3Height = r.randint(2,5)
    branch1Offset = r.randint(7,10)
    branch2Offset = r.randint(6,9)
    branch3Offset = r.randint(3,4)
    heightOfBranch1 = (1/3)*heightTot+r.randint(0,5)
    heightOfBranch2 = (1/2.3)*heightTot+r.randint(0,3)
    heightOfBranch3 = (2/3)*heightTot+r.randint(0,2)
    branchCount = r.randint(2,3)
    directChoice = r.choice([-1,1])
    # Random choice.
    for i in range(branchCount):
        if branchCount == 2:
            # Points.
            point1 = gr.Point(*perspectiveMap(x-3,y,z,fov))
            point2 = gr.Point(*perspectiveMap(x-3,y+heightOfBranch1-2,z,fov))
            point3 = gr.Point(*perspectiveMap(x-branch1Offset-10,y+heightOfBranch1-2,z,fov))
            point4 = gr.Point(*perspectiveMap(x-branch1Offset-10,y+heightOfBranch1+branch1Height,z,fov))
            point5 = gr.Point(*perspectiveMap(x-branch1Offset-6,y+heightOfBranch1+branch1Height,z,fov))
            point6 = gr.Point(*perspectiveMap(x-branch1Offset-6,y+heightOfBranch1+2,z,fov))
            point7 = gr.Point(*perspectiveMap(x-3,y+heightOfBranch1+2,z,fov))
            point8 = gr.Point(*perspectiveMap(x-3,y+heightTot,z,fov))
            point9 = gr.Point(*perspectiveMap(x+3,y+heightTot,z,fov))
            point10 = gr.Point(*perspectiveMap(x+3,y+heightOfBranch2+2,z,fov))
            point11 = gr.Point(*perspectiveMap(x+branch2Offset+6,y+heightOfBranch2+2,z,fov))
            point12 = gr.Point(*perspectiveMap(x+branch2Offset+6,y+heightOfBranch2+branch2Height,z,fov))
            point13 = gr.Point(*perspectiveMap(x+branch2Offset+10,y+heightOfBranch2+branch2Height,z,fov))
            point14 = gr.Point(*perspectiveMap(x+branch2Offset+10,y+heightOfBranch2-2,z,fov))
            point15 = gr.Point(*perspectiveMap(x+3,y+heightOfBranch2-2,z,fov))
            point16 = gr.Point(*perspectiveMap(x+3,y,z,fov))
            cactus = gr.Polygon(point1,point2,point3,point4,point5,point6,point7,point8,point9,point10,point11,point12,point13,point14,point15,point16)
        else:
            # More points.
            point1 = gr.Point(*perspectiveMap(x-3,y,z,fov))
            point2 = gr.Point(*perspectiveMap(x-3,y+heightOfBranch1-2,z,fov))
            point3 = gr.Point(*perspectiveMap(x-branch1Offset-10,y+heightOfBranch1-2,z,fov))
            point4 = gr.Point(*perspectiveMap(x-branch1Offset-10,y+heightOfBranch1+branch1Height,z,fov))
            point5 = gr.Point(*perspectiveMap(x-branch1Offset-6,y+heightOfBranch1+branch1Height,z,fov))
            point6 = gr.Point(*perspectiveMap(x-branch1Offset-6,y+heightOfBranch1+2,z,fov))
            point7 = gr.Point(*perspectiveMap(x-3,y+heightOfBranch1+2,z,fov))
            point8 = gr.Point(*perspectiveMap(x-3,y+heightTot,z,fov))
            point9 = gr.Point(*perspectiveMap(x+3,y+heightTot,z,fov))
            point10 = gr.Point(*perspectiveMap(x+3,y+heightOfBranch3+1,z,fov))
            point11 = gr.Point(*perspectiveMap(x+branch3Offset+5,y+heightOfBranch3+1,z,fov))
            point12 = gr.Point(*perspectiveMap(x+branch3Offset+5,y+heightOfBranch3+branch3Height,z,fov))
            point13 = gr.Point(*perspectiveMap(x+branch3Offset+7,y+heightOfBranch3+branch3Height,z,fov))
            point14 = gr.Point(*perspectiveMap(x+branch3Offset+7,y+heightOfBranch3-1,z,fov))
            point15 = gr.Point(*perspectiveMap(x+3,y+heightOfBranch3-1,z,fov))
            point16 = gr.Point(*perspectiveMap(x+3,y+heightOfBranch2+2,z,fov))
            point17 = gr.Point(*perspectiveMap(x+branch2Offset+6,y+heightOfBranch2+2,z,fov))
            point18 = gr.Point(*perspectiveMap(x+branch2Offset+6,y+heightOfBranch2+branch2Height,z,fov))
            point19 = gr.Point(*perspectiveMap(x+branch2Offset+10,y+heightOfBranch2+branch2Height,z,fov))
            point20 = gr.Point(*perspectiveMap(x+branch2Offset+10,y+heightOfBranch2-2,z,fov))
            point21 = gr.Point(*perspectiveMap(x+3,y+heightOfBranch2-2,z,fov))
            point22 = gr.Point(*perspectiveMap(x+3,y,z,fov))
            cactus = gr.Polygon(point1,point2,point3,point4,point5,point6,point7,point8,point9,point10,point11,point12,point13,point14,point15,point16,point17,point18,point19,point20,point21,point22)
    # Color.
    cactus.setFill("#2C8515")
    cactusSet = (cactus,z)
    return cactusSet


def titleScreen(x,y,text="Default",scale=1):
    '''
    Basic Title function. Wish I coul've used some terrible font. Alas.
    '''
    center = gr.Point(x,y)
    text = gr.Text(center,text)
    text.setFace("times roman")
    text.setSize(int(scale*18))
    return text


def rocketTest():
    shapeList = []
    width = 1540
    height = 870
    logo = tk.PhotoImage(file="Project05\Daco_6135086.png")
    screen = gr.GraphWin("Yeah, We Doin' a Project.'", width=width, height=height, autoflush=False)
    screen.setCoords(-770,-435,770,435)
    screen.master.iconphoto(False, logo)
    screen.master.attributes("-fullscreen", False)
    color = ("#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C","#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C","#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C")    
    iRocket1 = rocket_init_(8,200,0,200,0,5,75,20,0,0,0,22.5,color,"rocket")
    jRocket1 = rocket_init_(8,-200,0,125,0,5,75,20,0,0,0,22.5,color,"rocket")
    kRocket1 = rocket_init_(8,0,0,50,0,5,75,20,0,0,0,22.5,color,"rocket")
    shapeList.extend(iRocket1)
    shapeList.extend(jRocket1)
    shapeList.extend(kRocket1)
    for i in range(len(shapeList)):
        shapeList[i].draw(screen)
    screen.getMouse()
    screen.close()


def mountainTest():
    shapeList = []
    width = 1540
    height = 870
    logo = tk.PhotoImage(file="Project05\Daco_6135086.png")
    screen = gr.GraphWin("Yeah, We Doin' a Project.'", width=width, height=height, autoflush=False)
    screen.setCoords(-770,-435,770,435)
    screen.master.iconphoto(False, logo)
    screen.master.attributes("-fullscreen", False)
    mount1 = mountainBackground_init("#406694",300,800,-.55,200,9,"mountBack")
    mount2 = mountainBackground_init("#204d83",150,700,-.70,100,9,"mountMid")
    mount3 = mountainBackground_init("#003371",50,600,-.85,50,9,"mountFront")
    shapeList.append(mount1)
    shapeList.append(mount2)
    shapeList.append(mount3)
    for i in range(len(shapeList)):
        shapeList[i].draw(screen)
    screen.getMouse()
    screen.close()