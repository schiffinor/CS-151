import graphicsPlus as gr
import math as m
from matrix import *
import json as js


width =1920
height=1080
screen = gr.GraphWin("Yeah, We Doin' a Project.'", width=width, height=height, autoflush=False)
screen.setCoords(-width/2,-height/2,width/2,height/2)
floorMap = gr.Image(gr.Point(4320,0),"Project11\Resources\Background\FloorData\Artboard2.ppm")
lowestFloor = []
for column in range(0,10560):
    row = 1079
    pixel =  floorMap.getPixel(column,row)
    while pixel != [0,0,0]:
        row -= 1
        pixel = floorMap.getPixel(column,row)
    lowestFloor.append([column,row])

with open("Project11\FloorData.txt","w") as outputFile:
    js.dump(lowestFloor,outputFile)