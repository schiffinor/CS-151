'''
ascii_art_image.py
Roman Schiffino 151B Fall Semester
This turns our images into ascii art using that handy dandy matrix class I made.
'''
import graphics as gr
import tkinter as tk
import sys as s
from matrix import *


def hexColor(tupColor):
    '''
    Converts (R,G,B) to Hex.
    '''
    hexColor = '#{:02x}{:02x}{:02x}'.format(*tupColor)
    return hexColor


def tupColor(hexColor):
    '''
    Converts Hex to (R,G,B).
    '''
    modif =hexColor.lstrip("#")
    tupColor = (int(modif[0:2], 16), int(modif[2:4], 16), int(modif[0:2], 16))
    return tupColor


def twoCharAscii(img):
    '''
    Makes an ascii art using 2 characters.
    '''
    # Dimensions
    width = img.getWidth()
    height = img.getHeight()
    # Init matrix
    asciiMatrix = matData(width,height)
    # Characters
    choices = ['▓','░']
    for i in range(width):
        for j in range(height):
            # Intensity calculation.
            intensity = int(sum(map(lambda x: img.getPixel(i,j)[x],[0,1,2])))/3
            # Sets matrix values.
            asciiMatrix.set(i,j,choices[0 if (intensity<128) else 1])
    return asciiMatrix


def multiCharAscii(img):
    '''
    Makes an ascii art using 4 characters.
    '''
    # Dimensions
    width = img.getWidth()
    height = img.getHeight()
    # Init matrix
    asciiMatrix = matData(width,height)
    # Characters
    choices = ['█','▓','▒','░']
    for i in range(width):
        for j in range(height):
            # Intensity calculation.
            intensity = int(sum(map(lambda x: img.getPixel(i,j)[x],[0,1,2])))/3
            # Sets matrix values.
            asciiMatrix.set(i,j,choices[0 if (0<=intensity and intensity<64) else 1 if (64<=intensity and intensity<128) else 2 if (128<=intensity and intensity<192) else 3])
    return asciiMatrix



def test(fileName):
    '''
    just applies twoCharAscii filter
    '''
    image = "Project07\Project07Folder\ ".rstrip(" ")+str(fileName)
    myImage = gr.Image(gr.Point(0,0),image)
    asciiArt = twoCharAscii(myImage)
    print(asciiArt)
    # Allows me to use these utf characters.
    with open(file="Project07\Project07Folder\TwoCharAscii.txt", mode="w", encoding="utf-16") as outFile:
        outFile.write(str(asciiArt))
    outFile.close()


def test2(fileName):
    '''
    just applies multiCharAscii filter
    '''
    image = "Project07\Project07Folder\ ".rstrip(" ")+str(fileName)
    myImage = gr.Image(gr.Point(0,0),image)
    asciiArt = multiCharAscii(myImage)
    print(asciiArt)
    # Allows me to use these utf characters.
    with open(file="Project07\Project07Folder\MultiCharAscii.txt", mode="w", encoding="utf-16") as outFile:
        outFile.write(str(asciiArt))
    outFile.close()


def main():
    '''
    main function just runs both tests.
    '''
    test("exotic.ppm")
    test2("exotic.ppm")


if __name__ == '__main__':
    main()