'''
warhol.py
Roman Schiffino 151B Fall Semester
This is one of the main project files. It does what the lab asks it to do. 
I made a bunch of filters because I was just testing all the options. I finally 
settled on three of these for the final warholl image. I use the matrix class to 
keep track of the color at each pixel on the canvas. I then make an image from this data and save it as warhol.ppm.
'''
import graphics as gr
import display as d
import tkinter as tk
import sys as s
import math as m
import filters as f
from matrix import *


def main():
    '''
    This just iniates our function it handles everything fo this program.
    '''
    imageList = []
    matrixList = []
    # Image source.
    imageName = "Project06\Project06Folder\ ".rstrip(" ")+"borgar.ppm"
    # Creates an image from the source.
    image = gr.Image(gr.Point(0,0),imageName)
    # Image list that contains all our data thats passed to the functions.
    imList = [[0, 0, 0, image], [image.getWidth(), 0, 2, image], [0, image.getHeight(), 3, image], [image.getWidth(), image.getHeight(), 4, image]]
    # Creates new screen based on source dimensions. 
    mainCanvas = gr.GraphWin("Warhol",2*image.getWidth(),2*image.getHeight(),False)
    for iter in range(len(imList)):
        # Extracts data on what filter to use.
        filterName = imList[iter][2]
        # Creates a dynamically named variableby which to refer to the image being currently modified.
        imageName = "image" + str(iter+1)
        globals()[imageName] = imList[iter][3]
        globals()[imageName] = globals()[imageName].clone()
        # No filter.
        if filterName == 0:
            colorMatrix = matData(globals()[imageName].getHeight(),globals()[imageName].getWidth())
            # This is just data to get our matrix values. This goes through every pixel and saves it to a matrix point.
            for i in range(globals()[imageName].getWidth()):
                for j in range(globals()[imageName].getHeight()):
                    color = f.hexColor(globals()[imageName].getPixel(i,j))
                    colorMatrix.set(j,i,color)
            # Appends matrix to list of matrices.
            imageList.append(colorMatrix)
            globals()[imageName] = f.placeImageInCanvas(mainCanvas, globals()[imageName], imList[iter][0], imList[iter][1])
        # Green Blue Swap.
        elif filterName == 1:
            imageDataSet = f.swapGreenBlue(globals()[imageName])
            # Appends matrix to list of matrices.
            imageList.append(imageDataSet[1])
            globals()[imageName] = imageDataSet[0]
            globals()[imageName] = f.placeImageInCanvas(mainCanvas, globals()[imageName], imList[iter][0], imList[iter][1])
        # Chroma Red Lum filter.
        elif filterName == 2:
            imageDataSet = f.chromaRedLum(globals()[imageName])
            # Appends matrix to list of matrices.
            imageList.append(imageDataSet[1])
            globals()[imageName] = imageDataSet[0]
            globals()[imageName] = f.placeImageInCanvas(mainCanvas, globals()[imageName], imList[iter][0], imList[iter][1])
        # Chroma Green Lum filter.
        elif filterName == 3:
            imageDataSet = f.chromaGreenLum(globals()[imageName])
            # Appends matrix to list of matrices.
            imageList.append(imageDataSet[1])
            globals()[imageName] = imageDataSet[0]
            globals()[imageName] = f.placeImageInCanvas(mainCanvas, globals()[imageName], imList[iter][0], imList[iter][1])
        # Chroma Blue Lum filter.
        elif filterName == 4:
            imageDataSet = f.chromaBlueLum(globals()[imageName])
            # Appends matrix to list of matrices.
            imageList.append(imageDataSet[1])
            globals()[imageName] = imageDataSet[0]
            globals()[imageName] = f.placeImageInCanvas(mainCanvas, globals()[imageName], imList[iter][0], imList[iter][1])
        # Chroma Red Lum Alt filter.
        elif filterName == 5:
            imageDataSet = f.chromaRedLumAlt(globals()[imageName])
            # Appends matrix to list of matrices.
            imageList.append(imageDataSet[1])
            globals()[imageName] = imageDataSet[0]
            globals()[imageName] = f.placeImageInCanvas(mainCanvas, globals()[imageName], imList[iter][0], imList[iter][1])
        # Chroma Green Lum Alt filter.
        elif filterName == 6:
            imageDataSet = f.chromaGreenLumAlt(globals()[imageName])
            # Appends matrix to list of matrices.
            imageList.append(imageDataSet[1])
            globals()[imageName] = imageDataSet[0]
            globals()[imageName] = f.placeImageInCanvas(mainCanvas, globals()[imageName], imList[iter][0], imList[iter][1])
        # Chroma Blue Lum Alt filter.
        elif filterName ==7:
            imageDataSet = f.chromaBlueLumAlt(globals()[imageName])
            # Appends matrix to list of matrices.
            imageList.append(imageDataSet[1])
            globals()[imageName] = imageDataSet[0]
            globals()[imageName] = f.placeImageInCanvas(mainCanvas, globals()[imageName], imList[iter][0], imList[iter][1])
        # Chroma Red Lum Swap filter.
        elif filterName == 8:
            imageDataSet = f.chromaRedLumSwap(globals()[imageName])
            # Appends matrix to list of matrices.
            imageList.append(imageDataSet[1])
            globals()[imageName] = imageDataSet[0]
            globals()[imageName] = f.placeImageInCanvas(mainCanvas, globals()[imageName], imList[iter][0], imList[iter][1])
        # Chroma Green Lum Swap filter.
        elif filterName == 9:
            imageDataSet = f.chromaGreenLumSwap(globals()[imageName])
            # Appends matrix to list of matrices.
            imageList.append(imageDataSet[1])
            globals()[imageName] = imageDataSet[0]
            globals()[imageName] = f.placeImageInCanvas(mainCanvas, globals()[imageName], imList[iter][0], imList[iter][1])
        # Chroma Blue Lum Swap filter.
        else:
            imageDataSet = f.chromaBlueLumSwap(globals()[imageName])
            # Appends matrix to list of matrices.
            imageList.append(imageDataSet[1])
            globals()[imageName] = imageDataSet[0]
            globals()[imageName] = f.placeImageInCanvas(mainCanvas, globals()[imageName], imList[iter][0], imList[iter][1])
        globals()[imageName].draw(mainCanvas)
    # Defines and recombines matrices so that we compile all the info for our image compilation.
    topLeftMatrix = imageList[0]
    topRightMatrix = imageList[1]
    bottomLeftMatrix = imageList[2]
    bottomRightMatrix = imageList[3]
    topMatrix = topLeftMatrix.rAppend(topRightMatrix)
    bottomMatrix = bottomLeftMatrix.rAppend(bottomRightMatrix)
    fullColorMatrix = topMatrix.dAppend(bottomMatrix)
    # Presents combined image.
    mainCanvas.update()
    mainCanvas.getMouse()
    mainCanvas.close()
    # Creates empty image with dimensions of canvas.
    output = gr.Image(gr.Point(0,0),2*image.getWidth(),2*image.getHeight())
    # Sets every pixel in the output image to its corresponding color as defined by the matrix.
    for i in range(fullColorMatrix.rows):
        for j in range(fullColorMatrix.columns):
            output.setPixel(i,j,fullColorMatrix.get(j,i))
    output.save("Project06\Project06Folder\warhol.ppm")


if __name__ == '__main__':
    main()