'''
compound_shapes.py
Roman Schiffino 151B Fall Semester
This is my project file for project number 4. 
It kind of tries its best to generate a 3d ball in which the camera is located. It's honestly a tiny bit
jank near the top because of my clipmask, but, its barely notable.
'''

import graphics as gr
import numpy as np
import math as m
import tkinter as tk
import inspect as ins

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
    # Clipping is handled well by default here so we just append our templist as is to the main shapelist.
    shapeList.extend(tempList)


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
    shapeList.extend(tempList)


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
    shapeList.extend(tempList)


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
    shapeList.extend(tempList)


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
    shapeList.extend(tempList)


def polyWindowPoints(polyX,polyY,polyZ,degCurrent,windowVerticalOffset,windowHorizontalOffset,sideCount,windowWidth,windowHeight,rowCount,columnCount,winDn,winSide):
    '''
    This worked so badly that I just abandoned it. However, I honestly worked a lot on it so I didn't want to delete it. Check it out if you'd like.
    '''
    point_pre = (polyX,polyY,polyZ)
    point = np.array([point_pre]) - np.array([((windowHorizontalOffset+windowHorizontalOffset*columnCount+windowWidth*columnCount+windowWidth*winSide)*m.cos(degCurrent+m.radians(90/sideCount)),-windowVerticalOffset-windowVerticalOffset*rowCount-windowHeight*rowCount-windowHeight*winDn,(windowHorizontalOffset+windowHorizontalOffset*columnCount+windowWidth*columnCount+windowWidth*winSide)*m.sin(degCurrent+m.radians(90/sideCount)))])
    #Convert to tuple.
    point=np.reshape(point,3)
    point=tuple(point)
    return point


def defunctPolyFrustrizedWindow(sideCount,x,y,z,sideLengthTop,sideLengthBottom,height,xRot,yRot,zRot,color):
    '''
    This worked so badly that I just abandoned it. However, I honestly worked a lot on it so I didn't want to delete it. Check it out if you'd like.
    '''
    # I refuse to comment this its just a non functioning mess lol.
    tempList = []
    winVert = int(height/30)
    winVertOff = (height%30)/(winVert+1)
    winHor = int(sideLengthTop/70)
    winHorOff = (sideLengthTop%70)/(winHor+1)
    for count in range(1,sideCount+1):
        for winColCount in range(winHor):
            for winRowCount in range(winVert): 
                point1 = gr.Point(*perspectiveMap(*polyWindowPoints(*polyPoint3(sideCount,x,y,z,sideLengthTop,xRot,yRot,zRot,count),winVertOff,winHorOff,sideCount,winHor,winVert,winRowCount,winColCount,0,0),fov))
                point2 = gr.Point(*perspectiveMap(*polyWindowPoints(*polyPoint3(sideCount,x,y,z,sideLengthTop,xRot,yRot,zRot,count),winVertOff,winHorOff,sideCount,winHor,winVert,winRowCount,winColCount,0,1),fov))
                point3 = gr.Point(*perspectiveMap(*polyWindowPoints(*polyPoint3(sideCount,x,y,z,sideLengthTop,xRot,yRot,zRot,count),winVertOff,winHorOff,sideCount,winHor,winVert,winRowCount,winColCount,1,1),fov))
                point4 = gr.Point(*perspectiveMap(*polyWindowPoints(*polyPoint3(sideCount,x,y,z,sideLengthTop,xRot,yRot,zRot,count),winVertOff,winHorOff,sideCount,winHor,winVert,winRowCount,winColCount,1,0),fov))
                pillarNameFace = "pillarFace" + str(count+1)
                globals()[pillarNameFace] = gr.Polygon(point1,point2,point3,point4)
                globals()[pillarNameFace].setFill(color[count-1])
                if polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,count)[2] >= 0 and polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,count)[2] >= 0 and polyPoint2(sideCount,x,y+height,z,sideLengthTop,xRot,yRot,zRot,1+count)[2] >= 0 and polyPoint2(sideCount,x,y,z,sideLengthBottom,xRot,yRot,zRot,1+count)[2] >= 0: 
                    tempList.append(globals()[pillarNameFace])
                print(globals()[pillarNameFace])
    shapeList.extend(tempList)


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
    shapeList.extend(tempList)


def moarWindows_init_(sideCount,x,y,z,sideLength,height,xRot,yRot,zRot,color,winWidth,winHeight):
    '''
    This would have been the framework to generate more windows. However, I dont need to make this harder than it already was. 
    Here's a quick explanation. Basically this along with polyPoint4 provides the framework for generating points on a pillar plane
    While not necessarily having the shapes begin being drawn on the face itself if that makes sense. That is the soltion to this 
    code was though of whie I was eating breakfast. Thus no time to implement.
    '''
    # Again refuse to commentate this as I don't use it.
    for count in range(1,sideCount+1):
        centerPoint = gr.Point(*perspectiveMap(*polyPoint4(sideCount,x,y,z,sideLength,xRot,yRot,zRot,count),fov))
        point_pre = (x,y,z)
    point = np.array([point_pre]) - np.array([])
    #Convert to tuple.
    point=np.reshape(point,3)
    point=tuple(point)


def testPillar():
    '''
    Compound Shape #1
    '''
    color = ("#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C","#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C","#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C")
    pillar_init(8,0,-150,200,20,300,0,22.5,0,color)
    pillar_init(6,-300,-100,200,30,300,0,-60,0,color)
    pillar_init(20,300,-200,200,10,300,0,90-27,0,color)
    # Wow... Draws everything.
    for drawer in range(len(shapeList)):
        shapeList[drawer].draw(screen)
    # Makes the screen close on click.
    screen.getMouse()
    screen.close()


def testFrustrum():
    '''
    Compound Shape #3
    '''
    color = ("#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C","#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C","#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C")
    polyFrustrum(8,0,-150,200,20,30,300,0,67.5,0,color)
    polyFrustrum(6,-300,-100,200,30,40,300,0,0,0,color)
    polyFrustrum(20,300,-200,200,10,20,300,0,90-27,0,color)
    # Wow... Draws everything.
    for drawer in range(len(shapeList)):
        shapeList[drawer].draw(screen)
    # Makes the screen close on click.
    screen.getMouse()
    screen.close()


def testSidePillar():
    '''
    Compound Shape #2
    '''
    color = ("#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C","#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C","#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C")
    sidePillar_init(8,0,0,200,20,300,0,0,0,color)
    sidePillar_init(6,-300,-100,200,30,300,0,0,0,color)
    sidePillar_init(20,300,100,200,10,300,0,0,0,color)
    # Wow... Draws everything.
    for drawer in range(len(shapeList)):
        shapeList[drawer].draw(screen)
    # Makes the screen close on click.
    screen.getMouse()
    screen.close()


def main():
    screen.bind_all("<F11>", screenFull)
    screen.bind_all("<Escape>", screenEsc)
    # Ha ha ha... My color list. Nothing too exciting here basically lists all my colors (4 total) in order of lightest to darkest then darkest to lightest.
    # Basically allows me to get away with not making a lighting system and instead just iterating through preordained values. 
    # This honestly in my opinion produces a pretty good illusion of lighting. I honestly expected it to not work as well right off the bat.
    # But it just worked kind of plug and pay so I let it rock. Also should have used a block comment.
    color = ("#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C")
    colors = ("#FFC300","#DFAB00","#BF9200","#9F7A00","#9F7A00","#BF9200","#DFAB00","#FFC300")
    # Just calls everything in proper order so that everything clips properly.
    polyFrustrum(8,0,-150,200,80,20,-50,0,22.5,0,color)
    polyFrustrum(8,0,150,200,80,20,25,0,22.5,0,color)
    polyFrustrum(8,0,-200,200,150,80,-10,0,22.5,0,color)
    polyFrustrum(8,0,175,200,150,80,10,0,22.5,0,color)
    polyFrustrumClipMask(8,0,185,200,300,150,10,0,22.5,0,color)
    polyFrustrumClipMask(8,0,-210,200,300,150,-10,0,22.5,0,color)
    polyFrustrumClipMask(8,0,195,200,330,300,-105,0,22.5,0,color)
    polyFrustrumWindowClipMask(8,0,-100,200,350,330,95,0,22.5,0,colors,color)
    polyFrustrumClipMask(8,0,-220,200,330,300,120,0,22.5,0,color)
    polyFrustrumClipMask(8,0,90,200,350,330,-95,0,22.5,0,color)
    sidePillar_init(4,getRelRad(8,20),100,200,20,300,45,0,0,color)
    sidePillar_init(4,-getRelRad(8,20),100,200,20,-300,45,0,0,color)
    pillar_init(8,0,-150,200,20,300,0,22.5,0,color)
    frontPillar_init(4,0,100,200-getRelRad(8,20),20,199-getRelRad(8,20),0,0,45,color)
    # Wow... Draws everything.
    for drawer in range(len(shapeList)):
        shapeList[drawer].draw(screen)
    # Makes the screen close on click.
    screen.getMouse()
    screen.close()


# This runs the whole thing.
if __name__ == '__main__':
    main()
