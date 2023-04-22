'''
scene2.py
Roman Schiffino 151B Fall Semester
This is my project file for project number 5. 
This is an extremely, and i mean extremely slow program. 
This program may take several minutes to boot aon slower computers. 
IE it will draw a couple of the static shapes first then compute all points for the rockets along their path
and then draw the rest of the animation. So I guess just give it some time. Regardless 
the intended effect is of a nuclear missle strike in a desert. Mountain ranges and cacti are random/procedurally generated. 
So if you'd like to see the randomness run it a couple times. Oh also fyi, I had to make an edit to the graphicPlus library
to make it more workable with my code. I prefer to work with hex so I changed getFill() to output in hex.

P.S. I was doing some slight editing while commenting and I found some inefficiencies. I fixed them and it now runs very quickly on my Desktop so yeah not quite as slow. 
It seems I accidentally indented some code and was running through like a couple hundred thousand iterations. Also, was unnecesarily frequently updating the screen.
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
from compund_shapes import *


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


def flash():
    '''
    This function creates a "flash of light" effect that rapidly grows from the center of the screen
    and then disapears.
    '''
    # Initiates output list.
    tempList = []
    # Parameters for initial circle.
    center = gr.Point(0,0)
    radius = 1
    # Draw initial circle.
    flash = gr.Circle(center,radius)
    flash.setFill("white")
    tempList.append(flash)
    tempList[0].draw(screen)
    screen.update()
    radius = 0
    # Animation Loop.
    for i in range(100):
        # Updates radius and creates circle.
        radius += 10
        flash = gr.Circle(center,radius)
        flash.setFill("white")
        tempList.append(flash)
    for i in range(100):
        # Draws circle.
        tempList[i+1].draw(screen)
        screen.update()
    for i in range(101):
        # Removes all circles.
        tempList[i].undraw()
    screen.update()


def main():
    '''
    Main function executes everything and makes everything work.
    '''
    screen.setBackground("#FF863A")
    # All of the empty lists that must be initiated to get everything else to work properly.
    delListi = []
    delListj = []
    delListk = []
    drawListi = []
    drawListj = []
    drawListk = []
    zVali = []
    zValj = []
    zValk = []
    billboardsList = []
    orderedBillboardsList = []
    # Just key-binding.
    screen.bind_all("<F11>", screenFull)
    screen.bind_all("<Escape>", screenEsc)
    # This is just the color list for the rockets to handle their colors and faux-shading.
    color = ("#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C","#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C","#37004C","#300043","#290039","#220030","#220030","#290039","#300043","#37004C")
    # Initiates first three rockets.
    iRocket1 = rocket_init_(8,200,0,600,0,5,75,20,0,0,90,22.5,color,"rocket",True)
    jRocket1 = rocket_init_(8,-200,0,800,0,5,75,20,0,0,90,22.5,color,"rocket",True)
    kRocket1 = rocket_init_(8,0,0,600,0,5,75,20,0,0,90,22.5,color,"rocket",True)
    # Adds floor static to shapeList.
    shapeList.append(floor("#FFEA81",800))
    # Creates mountain static backgrounds.
    mountBackStatic = mountainBackground_init("#406694",300,800,-.55,200,9,"mountBack")
    mountMidStatic = mountainBackground_init("#204d83",150,700,-.70,100,9,"mountMid")
    mountFrontStatic = mountainBackground_init("#003371",50,600,-.85,50,9,"mountFront")
    # Adds them to shapeList.
    shapeList.extend([mountBackStatic,mountMidStatic,mountFrontStatic])
    # Saves statics to second variable for use as dynamic (refreshable) background.
    mountBack = mountBackStatic
    mountMid = mountMidStatic
    mountFront = mountFrontStatic
    # Creates cactus billboards. Gets random Z, calculates visible x range based on said z and then draws cactus at random (x,z) dependent on said points.
    for i in range(10):
        z = r.randint(50,350)
        billboardsList.append(cactiBillboards_init(r.randint(int((-770)/(fov/z)),int((770)/(fov/z))),z))
    # Sorts billboards by reverze z order.
    billboardsList.sort(key = lambda billboardsList: billboardsList[1], reverse = True)
    # Extracts only billboard data from billboard z-pos tuple.
    for i in range(10):
        orderedBillboardsList.append(billboardsList[i][0])
    # Adds bilboards to shapeList.
    shapeList.extend(orderedBillboardsList)
    # Draws all shapes in shapeList.
    for drawer in range(len(shapeList)):
        shapeList[drawer].draw(screen)
        screen.update()
    # Slight break.
    t.sleep(.25)
    # The beginning of the relatively efficient, but extremely math intensive, and slow code.
    # Also for reference zip from python 3 is equivalent to izip from itertools in python 2, so yeah.
    for i,j,k in zip(range(275),range(250),range(275)):
        # Stores previous rocket object, such that it can be deleted once the new rocket is drawn.
        iRocket0 = iRocket1
        # Adds previous object to deletion list.
        delListi.append(iRocket0[0])
        # Calculates magnitude of tangent vector so that we can calculate the angle of the tangent vector relative the coordinate axes.
        iMagnitude1 = m.sqrt(((-20)**2)+((200-(1/25)*40*i)**2)+((-40)**2))
        # Uses a parametrized path function and the aforementioned angles to draw a rocket at a specific point and facing the direction specified by the angles above.
        iRocket1 = rocket_init_(8,200-(1/25)*20*i,(1/25)*200*i-(1/625)*20*(i**2),800-(1/25)*40*i,0,5,75,20,m.degrees(m.acos((-20)/iMagnitude1)),90+m.degrees(m.acos((200-(1/25)*40*i)/iMagnitude1)),m.degrees(m.acos((-40)/iMagnitude1)),22.5,color,"rocket",True)
        # Appends the new rocket to drawList.
        drawListi.append(iRocket1[0])
        # Appends the current zvalue of the rocket to the list of zvals for rocket i.
        zVali.append(iRocket1[1])
        # Stores previous rocket object, such that it can be deleted once the new rocket is drawn.
        jRocket0 = jRocket1
        # Adds previous object to deletion list.
        delListj.append(jRocket0[0])
        # Calculates magnitude of tangent vector so that we can calculate the angle of the tangent vector relative the coordinate axes.
        jMagnitude1 = m.sqrt(((20-20*(m.sin((1/25)*j)))**2)+((200-(1/25)*40*j+20*m.cos((1/25)*j))**2)+((-40)**2))
        # Uses a parametrized path function and the aforementioned angles to draw a rocket at a specific point and facing the direction specified by the angles above.
        jRocket1 = rocket_init_(8,(-200+(1/25)*20*j+20*m.cos((1/25)*j)),((1/25)*200*j-(1/625)*20*(j**2)+20*m.sin((1/25)*j)),(800-(1/25)*40*j),0,5,75,20,m.degrees(m.acos((20-20*m.sin((1/25)*j))/jMagnitude1)),90+m.degrees(m.acos(((200 - (1/25)*40*j+20*m.cos((1/25)*j))/jMagnitude1))),(m.degrees(m.acos((-40)/jMagnitude1))),22.5,color,"rocket",True)
        # Appends the new rocket to drawList.
        drawListj.append(jRocket1[0])
        # Appends the current zvalue of the rocket to the list of zvals for rocket j.
        zValj.append(jRocket1[1])
        # Stores previous rocket object, such that it can be deleted once the new rocket is drawn.
        kRocket0 = kRocket1
        # Adds previous object to deletion list.
        delListk.append(kRocket0[0])
        # Calculates magnitude of tangent vector so that we can calculate the angle of the tangent vector relative the coordinate axes.
        kMagnitude1 = m.sqrt(((30*(m.sin((1/25)*k)))**2)+((200-(1/25)*40*k-60*m.cos((1/25)*k))**2)+((-40)**2))
        # Uses a parametrized path function and the aforementioned angles to draw a rocket at a specific point and facing the direction specified by the angles above.
        kRocket1 = rocket_init_(8,(-30*m.cos((1/25)*k)),((1/25)*200*k-(1/625)*20*(k**2)-60*m.sin((1/25)*k)),(800-(1/25)*40*k),0,5,75,20,m.degrees(m.acos((30*m.sin((1/25)*k))/kMagnitude1)),90+m.degrees(m.acos(((200 - (1/25)*40*k-60*m.cos((1/25)*k))/kMagnitude1))),(m.degrees(m.acos((-40)/kMagnitude1))),22.5,color,"rocket",True)
        # Appends the new rocket to drawList.
        drawListk.append(kRocket1[0])
        # Appends the current zvalue of the rocket to the list of zvals for rocket k.
        zValk.append(kRocket1[1])
    # I'll just explain what these 3 next for loop blocks do. It basically just functions to check if the current rocket is in front or behind the mountains. If it is behind it will then redraw that mountain range infront of the rockets.
    # Also FYI thius is the area with the glitches that I fixed up.
    for i,j,k in zip(range(275),range(250),range(275)): 
        # Draws Rocket.
        for face in range(len(drawListi[i])):
            drawListi[i][face].draw(screen)
        # Draws furthest mountain range.
        if zVali[i] >800:
            mountBack.undraw()
            mountBack.draw(screen)
        # Draws middle mountain range.
        if zVali[i] > 700:
            mountMid.undraw()
            mountMid.draw(screen)
        # Draws front mountain range.
        if zVali[i] > 600:
            mountFront.undraw()
            mountFront.draw(screen)
        # Draws Cacti.
        if zVali[i] > 400:
            for n in range(10):
                orderedBillboardsList[n].undraw()
                orderedBillboardsList[n].draw(screen)
        # Deletes last Rocket.
        for face in range(len(delListi[i])):
            delListi[i][face].undraw()
        # Draws Rocket.
        for face in range(len(drawListj[j])):
            drawListj[j][face].draw(screen)
        # Draws furthest mountain range.
        if zValj[j] > 800:
            mountBack.undraw()
            mountBack.draw(screen)
        # Draws middle mountain range.
        if zValj[j] > 700:
            mountMid.undraw()
            mountMid.draw(screen)
        # Draws front mountain range.
        if zValj[j] > 600:
            mountFront.undraw()
            mountFront.draw(screen)
        # Draws Cacti.
        if zValj[j] > 400:
            for n in range(10):
                orderedBillboardsList[n].undraw()
                orderedBillboardsList[n].draw(screen)
        # Deletes last Rocket.
        for face in range(len(delListj[j])):
            delListj[j][face].undraw()
        # Draws Rocket.
        for face in range(len(drawListk[k])):
            drawListk[k][face].draw(screen)
        # Draws furthest mountain range.
        if zValk[k] > 800:
            mountBack.undraw()
            mountBack.draw(screen)
        # Draws middle mountain range.
        if zValk[k] > 700:
            mountMid.undraw()
            mountMid.draw(screen)
        # Draws front mountain range.
        if zValk[k] > 600:
            mountFront.undraw()
            mountFront.draw(screen)
        # Draws Cacti.
        if zValk[k] > 400:
            for n in range(10):
                orderedBillboardsList[n].undraw()
                orderedBillboardsList[n].draw(screen)
        # Deletes last Rocket.
        for face in range(len(delListk[k])):
            delListk[k][face].undraw()
        if screen.checkMouse() is not None:
            break 
        # Updates Screen.
        screen.update()
    # Self Explanatory, calls flash.
    flash()
    # Animation 2.
    # Haha, my second animation. Literally just gets every static object in the image, gets its fill color, using my modified version of the getFill() function, and appends said color to a list.
    # Then gets said color list, iterates through it getting the complement to each color, and sets that shapes color to be that of the its complement, and redraws everything.
    # This makes it have the effect of being like a negative of an image. 
    colorList = []
    # Gets the fill to each color of statics.
    for i in range(len(shapeList)):
        colorFill = shapeList[i].getFill()
        colorList.append(colorFill)
    # Undraws every shape in image.
    for i in screen.items[:]:
        i.undraw()
    # Sets Bg-color to complement of initial color.
    screen.setBackground(compColor("#FF863A"))
    screen.update()
    # Sets shape fill to complement and redraws every static shape.
    for i in range(len(shapeList)):
        shapeList[i].setFill(compColor(colorList[i]))
        shapeList[i].draw(screen)
        screen.update()
    # Short code to create and draw title off screen before animating.
    titleTempList = []
    title = titleScreen(0,450,"My title can't be this bad!",1.5)
    titleTempList.append(title)
    titleTempList[0].draw(screen)
    screen.update()
    delY = 0
    # Animates the title to zoom in from top.
    for i in range(1,31):
        t.sleep(.01)
        delY -= 8
        title = titleScreen(0,450+delY,"My title can't be this bad!",1.5)
        titleTempList.append(title)
        titleTempList[i-1].undraw()
        titleTempList[i].draw(screen)
        screen.update()
    # Close le'program.
    screen.getMouse()
    screen.close()


if __name__ == '__main__':
    fov = 360
    shapeList = []
    width = 1540
    height = 870
    # Honestly this logo is barely viible but I made the effort so here it is.
    logo = tk.PhotoImage(file="Project05\Daco_6135086.png")
    # We disable autoflush to decrease inefficiency, to prevent foreground flashing, and because it is bad.
    screen = gr.GraphWin("Yeah, We Doin' a Project.'", width=width, height=height, autoflush=False)
    # Unfortunately because of tkinters scaling, which I only found out about too late. I have to use not 1080p, and I got around that by creating a fullscreen function.
    #Regardless lead to not as clean an ouput as I had hoped.
    screen.setCoords(-770,-435,770,435)
    # Sets Icon.
    screen.master.iconphoto(False, logo)
    # Sets inital screenstate as not fullscreen.
    screen.master.attributes("-fullscreen", False)
    main()