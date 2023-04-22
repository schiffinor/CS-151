'''
filters.py
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


def swapGreenBlue(img):
    '''
    Swaps the green and blue values of every pixel of a Zelle image `img`
    '''
    # Initiates matrix for color storage.
    colorMatrix = matData(img.getHeight(),img.getWidth())
    for i in range(img.getWidth()):
        for j in range(img.getHeight()):
            # Color transformation using map and lambda is very efficient.
            color = hexColor(tuple(map(lambda x: img.getPixel(i,j)[x],[0,2,1])))
            img.setPixel(i,j,color)
            # Add data to color matrix.
            colorMatrix.set(j,i,color)
    return (img,colorMatrix)


def chromaRedLum(img):
    '''
    Sets the green and blue values of every pixel of a Zelle image `img` to grayscale values defined by luma.
    It also boosts the red value.
    '''
    # Initiates matrix for color storage.
    colorMatrix = matData(img.getHeight(),img.getWidth())
    for i in range(img.getWidth()):
        for j in range(img.getHeight()):
            # Luma is a brightness type value determined by the formula below. It basicaly only used for grayscale.
            Luma = int(0.2126*(img.getPixel(i,j)[0]) + 0.7152*(img.getPixel(i,j)[1]) + 0.0722*(img.getPixel(i,j)[2]))
            # Color transformation using map and lambda is very efficient.
            color = hexColor(tuple(map(lambda x: int(img.getPixel(i,j)[0]+m.sqrt((255-(img.getPixel(i,j)[0])))) if (x==0) else Luma,[0,1,2])))
            img.setPixel(i,j,color)
            # Add data to color matrix.
            colorMatrix.set(j,i,color)
    return (img,colorMatrix)


def chromaGreenLum(img):
    '''
    Sets the red and blue values of every pixel of a Zelle image `img` to grayscale values defined by luma.
    It also boosts the green value.
    '''
    # Initiates matrix for color storage.
    colorMatrix = matData(img.getHeight(),img.getWidth())
    for i in range(img.getWidth()):
        for j in range(img.getHeight()):
            # Luma is a brightness type value determined by the formula below. It basicaly only used for grayscale.
            Luma = int(0.2126*(img.getPixel(i,j)[0]) + 0.7152*(img.getPixel(i,j)[1]) + 0.0722*(img.getPixel(i,j)[2]))
            # Color transformation using map and lambda is very efficient.
            color = hexColor(tuple(map(lambda x: int(img.getPixel(i,j)[1]+m.sqrt((255-(img.getPixel(i,j)[1])))) if (x==1) else Luma,[0,1,2])))
            img.setPixel(i,j,color)
            # Add data to color matrix.
            colorMatrix.set(j,i,color)
    return (img,colorMatrix)


def chromaBlueLum(img):
    '''
    Sets the red and green values of every pixel of a Zelle image `img` to grayscale values defined by luma.
    It also boosts the blue value.
    '''
    # Initiates matrix for color storage.
    colorMatrix = matData(img.getHeight(),img.getWidth())
    for i in range(img.getWidth()):
        for j in range(img.getHeight()):
            # Luma is a brightness type value determined by the formula below. It basicaly only used for grayscale.
            Luma = int(0.2126*(img.getPixel(i,j)[0]) + 0.7152*(img.getPixel(i,j)[1]) + 0.0722*(img.getPixel(i,j)[2]))
            # Color transformation using map and lambda is very efficient.
            color = hexColor(tuple(map(lambda x: int(img.getPixel(i,j)[2]+m.sqrt((255-(img.getPixel(i,j)[2])))) if (x==2) else Luma,[0,1,2])))
            img.setPixel(i,j,color)
            # Add data to color matrix.
            colorMatrix.set(j,i,color)
    return (img,colorMatrix)


def chromaRedLumAlt(img):
    '''
    Sets the red and green values of every pixel of a Zelle image `img` to grayscale values defined by luma.
    It also boosts the blue value.
    '''
    # Initiates matrix for color storage.
    colorMatrix = matData(img.getHeight(),img.getWidth())
    for i in range(img.getWidth()):
        for j in range(img.getHeight()):
            # Luma is a brightness type value determined by the formula below. It basicaly only used for grayscale.
            Luma = int(0.2126*(img.getPixel(i,j)[0]) + 0.7152*(img.getPixel(i,j)[1]) + 0.0722*(img.getPixel(i,j)[2]))
            # Color transformation using map and lambda is very efficient.
            color = hexColor(tuple(map(lambda x: int(img.getPixel(i,j)[0]+(1/2)*((255-(img.getPixel(i,j)[0])))) if (x==0) else Luma,[0,1,2])))
            img.setPixel(i,j,color)
            # Add data to color matrix.
            colorMatrix.set(j,i,color)
    return (img,colorMatrix)


def chromaGreenLumAlt(img):
    '''
    Sets the red and blue values of every pixel of a Zelle image `img` to grayscale values defined by luma.
    It also boosts the green value.
    '''
    # Initiates matrix for color storage.
    colorMatrix = matData(img.getHeight(),img.getWidth())
    for i in range(img.getWidth()):
        for j in range(img.getHeight()):
            # Luma is a brightness type value determined by the formula below. It basicaly only used for grayscale.
            Luma = int(0.2126*(img.getPixel(i,j)[0]) + 0.7152*(img.getPixel(i,j)[1]) + 0.0722*(img.getPixel(i,j)[2]))
            # Color transformation using map and lambda is very efficient.
            color = hexColor(tuple(map(lambda x: int(img.getPixel(i,j)[1]+(1/2)*((255-(img.getPixel(i,j)[1])))) if (x==1) else Luma,[0,1,2])))
            img.setPixel(i,j,color)
            # Add data to color matrix.
            colorMatrix.set(j,i,color)
    return (img,colorMatrix)


def chromaBlueLumAlt(img):
    '''
    Sets the red and green values of every pixel of a Zelle image `img` to grayscale values defined by luma.
    It also boosts the blue value.
    '''
   # Initiates matrix for color storage.
    colorMatrix = matData(img.getHeight(),img.getWidth())
    for i in range(img.getWidth()):
        for j in range(img.getHeight()):
            # Luma is a brightness type value determined by the formula below. It basicaly only used for grayscale.
            Luma = int(0.2126*(img.getPixel(i,j)[0]) + 0.7152*(img.getPixel(i,j)[1]) + 0.0722*(img.getPixel(i,j)[2]))
            # Color transformation using map and lambda is very efficient.
            color = hexColor(tuple(map(lambda x: int(img.getPixel(i,j)[2]+(1/2)*((255-(img.getPixel(i,j)[2])))) if (x==2) else Luma,[0,1,2])))
            img.setPixel(i,j,color)
            # Add data to color matrix.
            colorMatrix.set(j,i,color)
    return (img,colorMatrix)


def chromaRedLumSwap(img):
    '''
    Boosts red, than mutes green and blue, and swaps them.
    '''
    # Initiates matrix for color storage.
    colorMatrix = matData(img.getHeight(),img.getWidth())
    for i in range(img.getWidth()):
        for j in range(img.getHeight()):
            # Luma is a brightness type value determined by the formula below. It basicaly only used for grayscale.
            Luma = int(0.2126*(img.getPixel(i,j)[0]) + 0.7152*(img.getPixel(i,j)[1]) + 0.0722*(img.getPixel(i,j)[2]))
            # Color transformation using map and lambda is very efficient.
            color = hexColor(tuple(map(lambda x: int(img.getPixel(i,j)[0]+m.sqrt((255-(img.getPixel(i,j)[0])))) if (x==0) else (int(Luma+m.sqrt((255-(img.getPixel(i,j)[2])))) if (x==1) else (int(Luma+m.sqrt((255-(img.getPixel(i,j)[1])))))),[0,1,2])))
            img.setPixel(i,j,color)
            # Add data to color matrix.
            colorMatrix.set(j,i,color)
    return (img,colorMatrix)


def chromaGreenLumSwap(img):
    '''
    Boosts green, than mutes red and blue, and swaps them.
    '''
    # Initiates matrix for color storage.
    colorMatrix = matData(img.getHeight(),img.getWidth())
    for i in range(img.getWidth()):
        for j in range(img.getHeight()):
            # Luma is a brightness type value determined by the formula below. It basicaly only used for grayscale.
            Luma = int(0.2126*(img.getPixel(i,j)[0]) + 0.7152*(img.getPixel(i,j)[1]) + 0.0722*(img.getPixel(i,j)[2]))
            # Color transformation using map and lambda is very efficient.
            color = hexColor(tuple(map(lambda x: int(img.getPixel(i,j)[1]+m.sqrt((255-(img.getPixel(i,j)[1])))) if (x==1) else (int(Luma+m.sqrt((255-(img.getPixel(i,j)[0])))) if (x==2) else (int(Luma+m.sqrt((255-(img.getPixel(i,j)[2])))))),[0,1,2])))
            img.setPixel(i,j,color)
            # Add data to color matrix.
            colorMatrix.set(j,i,color)
    return (img,colorMatrix)


def chromaBlueLumSwap(img):
    '''
    Boosts blue, than mutes red and green, and swaps them.
    '''
    # Initiates matrix for color storage.
    colorMatrix = matData(img.getHeight(),img.getWidth())
    for i in range(img.getWidth()):
        for j in range(img.getHeight()):
            # Luma is a brightness type value determined by the formula below. It basicaly only used for grayscale.
            Luma = int(0.2126*(img.getPixel(i,j)[0]) + 0.7152*(img.getPixel(i,j)[1]) + 0.0722*(img.getPixel(i,j)[2]))
            # Color transformation using map and lambda is very efficient.
            color = hexColor(tuple(map(lambda x: int(img.getPixel(i,j)[2]+m.sqrt((255-(img.getPixel(i,j)[2])))) if (x==2) else (int(Luma+m.sqrt((255-(img.getPixel(i,j)[1])))) if (x==0) else (int(Luma+m.sqrt((255-(img.getPixel(i,j)[0])))))),[0,1,2])))
            img.setPixel(i,j,color)
            # Add data to color matrix.
            colorMatrix.set(j,i,color)
    return (img,colorMatrix)


def greenScreen(greenImg, otherImg):
    '''
    If a pixel in `greenImg` is very green, replace it with the corresponding pixel in `otherImg`.
    A reasonable test for 'very green' is if the green pixel is 1.5 times the blue channel and also bigger than the red pixel.
    Play around with the 1.5 number to see if you can get better results.
    Ahahaha, I was having trouble with zoom so I may have made a custom version of the greenscreen image which I made in photoshop
    it actually used a G value of exactly 225. It is also manually cut so its 100% Green or it's not.
    Haha the bold statemnts made her ended up not being true because I forgot to disable feathering, and antialiasing. So yeah haha its just much harsher.
    '''
    for i in range(greenImg.getWidth()):
        for j in range(greenImg.getHeight()):
            if greenImg.getPixel(i,j)[1] >= 2.35*greenImg.getPixel(i,j)[2] and greenImg.getPixel(i,j)[0] <= 1.2*greenImg.getPixel(i,j)[1]:
                greenImg.setPixel(i,j,hexColor(tuple(map(lambda x: otherImg.getPixel(i,j)[x],[0,1,2]))))
    return greenImg


def placeImageInCanvas(canvas, img , topleft_x,topleft_y):

    '''
    Place the image `img` into the larger canvas `canvas`. The image `img` should be positioned
    so that its top-left corner appears at (row , col) = (topleft_row, topleft_col) in the large canvas.
    NOTE: (0, 0) is the top-left corner.

    Parameters:
    -----------
    canvas: Image. Larger canvas to place the image on.
    img: Image. Image to be placed on the canvas.
    topleft_x: int. x pixel position (column) in `canvas` where the top-left corner of `img` should go
    topleft_y: int. y pixel position (row) in `canvas` where the top-left corner of `img` should go
    '''
    # Pretty simple to how the display code works.
    anchor_x = (img.getWidth())/2 + topleft_x
    anchor_y = (img.getHeight())/2 + topleft_y
    img.move(anchor_x,anchor_y)
    return img


def test(fileName,filterName,fileReplacer=None):
    '''
    Basically our main logic handler. What we do here is basically just take all the impactful
    arguments and go through them to display whatever image is asked. It's values are defined 
    by the main function which recieves terminal side user input.
    '''
    # Makes any definition of screen in this function a global definition throughout the file.
    global screen
    # Checks to see whether a file for greenscreening is defined.
    if fileReplacer is None:
        # Determines if the filter identifier is one of the accepted values.
        if filterName == 0 or filterName == 1 or filterName == 2 or filterName == 3 or filterName == 4 or filterName == 5 or filterName == 6 or filterName == 7 or filterName == 8 or filterName == 9 or filterName == 10:
            # Defines image.
            image = "Project06\Project06Folder\ ".rstrip(" ")+str(fileName)
            myImage = gr.Image(gr.Point(0,0),image)
            if filterName == 0:
                myImage = gr.Image(gr.Point(0,0),image)
            elif filterName == 1:
                image = "Project06\Project06Folder\ ".rstrip(" ")+str(fileName)
                myImage = gr.Image(gr.Point(0,0),image)
                myImage = swapGreenBlue(myImage)[0]
                myImage.save("Project06\Project06Folder\greenBlueSwapped"+str(fileName))
            elif filterName == 2:
                image = "Project06\Project06Folder\ ".rstrip(" ")+str(fileName)
                myImage = gr.Image(gr.Point(0,0),image)
                myImage = chromaRedLum(myImage)[0]
                myImage.save("Project06\Project06Folder\chromaRed"+str(fileName))
            elif filterName == 3:
                image = "Project06\Project06Folder\ ".rstrip(" ")+str(fileName)
                myImage = gr.Image(gr.Point(0,0),image)
                myImage = chromaGreenLum(myImage)[0]
                myImage.save("Project06\Project06Folder\chromaGreen"+str(fileName))
            elif filterName == 4:
                image = "Project06\Project06Folder\ ".rstrip(" ")+str(fileName)
                myImage = gr.Image(gr.Point(0,0),image)
                myImage = chromaBlueLum(myImage)[0]
                myImage.save("Project06\Project06Folder\chromaBlue"+str(fileName))
            elif filterName == 5:
                image = "Project06\Project06Folder\ ".rstrip(" ")+str(fileName)
                myImage = gr.Image(gr.Point(0,0),image)
                myImage = chromaRedLumAlt(myImage)[0]
                myImage.save("Project06\Project06Folder\chromaRedAlt"+str(fileName))
            elif filterName == 6:
                image = "Project06\Project06Folder\ ".rstrip(" ")+str(fileName)
                myImage = gr.Image(gr.Point(0,0),image)
                myImage = chromaGreenLumAlt(myImage)[0]
                myImage.save("Project06\Project06Folder\chromaGreenAlt"+str(fileName))
            elif filterName ==7:
                image = "Project06\Project06Folder\ ".rstrip(" ")+str(fileName)
                myImage = gr.Image(gr.Point(0,0),image)
                myImage = chromaBlueLumAlt(myImage)[0]
                myImage.save("Project06\Project06Folder\chromaBlueAlt"+str(fileName))
            elif filterName == 8:
                image = "Project06\Project06Folder\ ".rstrip(" ")+str(fileName)
                myImage = gr.Image(gr.Point(0,0),image)
                myImage = chromaRedLumSwap(myImage)[0]
                myImage.save("Project06\Project06Folder\chromaRedSwap"+str(fileName))
            elif filterName == 9:
                image = "Project06\Project06Folder\ ".rstrip(" ")+str(fileName)
                myImage = gr.Image(gr.Point(0,0),image)
                myImage = chromaGreenLumSwap(myImage)[0]
                myImage.save("Project06\Project06Folder\chromaGreenSwap"+str(fileName))
            elif filterName == 10:
                image = "Project06\Project06Folder\ ".rstrip(" ")+str(fileName)
                myImage = gr.Image(gr.Point(0,0),image)
                myImage = chromaBlueLumSwap(myImage)[0]
                myImage.save("Project06\Project06Folder\chromaBlueSwap"+str(fileName))
            screen = d.displayImage(myImage,"Dabba Doo, Dabba Dee")
            # Honestly this logo is barely viible but I made the effort so here it is.
            logo = tk.PhotoImage(file="Project06\Project06Folder\Daco_6135086.png")
            # Sets Icon.
            screen.master.iconphoto(False, logo)
            # Sets inital screenstate as not fullscreen.
            screen.master.attributes("-fullscreen", False)
            screen.getMouse()
            screen.close()
        else: 
            print("Please check for any typos, or refer to documentation.")
    elif fileReplacer is not None:
        # Just a quick check to make sure usage is correct.
        if filterName == "g":
            # Define both images.
            srcImg = "Project06\Project06Folder\ ".rstrip(" ")+str(fileName)
            replacerImg = "Project06\Project06Folder\ ".rstrip(" ")+str(fileReplacer)
            Source = gr.Image(gr.Point(0,0),srcImg)
            Replacer = gr.Image(gr.Point(0,0),replacerImg)
            # Makes sure that the two images have the same dimensions, otherwise raises an error. 
            # Also IK that you wanted us to not throw errors; however, this is a specific error and one that is defined by me, so I hope it flies.
            if Source.getWidth()!=Replacer.getWidth() or Source.getHeight()!=Replacer.getHeight():
                raise ValueError("Dimension mismatch, please submit images with the same dimensions in the case of greenscreen.ppm those are 640x480.")
            Souce = greenScreen(Source,Replacer)
            Source.save("Project06\Project06Folder\greenScreened"+str(fileName))
            screen = d.displayImage(Source,"Dabba Doo, Dabba Dee")
            # Honestly this logo is barely viible but I made the effort so here it is.
            logo = tk.PhotoImage(file="Project06\Project06Folder\Daco_6135086.png")
            # Sets Icon.
            screen.master.iconphoto(False, logo)
            # Sets inital screenstate as not fullscreen.
            screen.master.attributes("-fullscreen", False)
            screen.getMouse()
            screen.close()
        else: 
            print("Please check for any typos, or refer to documentation.")
    else:
        # Pretty much what it says on the tin.
        print("I have no clue what could possibly result in this outcome, but I just wanted to add it in.")
        print("If you manage to get this message congrats, I'm baffled.")


def main(length,file="flowers.ppm",filter=0,fileReplacer=None):
    '''
    main function honestly just here to initiate things and to detail usage instructions for all the programs.
    '''
    # All the usage instructions depending on the arguments provided.
    print("Please run this code from a folder containing the outer most folder I've submitted.")
    print("That is the folder from where the terminal is run from should contain the \Project06 folder.")
    if length == 1 or length == 2:
        print("Usage Example: python3 Project06/Project06Folder/filters.py <filename of image> <0/1/2/3/4/5/6/7/8/9/10>")
        print("When you would like the original image please use 0.")
        print("For the filter swapGreenBlue use 1.")
        print("For the filter chromaRedLum use 2.")
        print("For the filter chromaGreenLum use 3.")
        print("For the filter chromaBlueLum use 4.")
        print("For the filter chromaRedLumAlt use 5.")
        print("For the filter chromaGreenLumAlt use 6.")
        print("For the filter chromaBlueLumAlt use 7.")
        print("For the filter chromaRedLumSwap use 8.")
        print("For the filter chromaGreenLumSwap use 9.")
        print("For the filter chromaBlueLumSwap use 10.")
        print("If you would like to use the greenscreen filter:")
        print("Usage Example: python3 Project06/Project06Folder/filters.py <filename of src image> g <filename of replacer image>")
    elif length == 3:
        test(file,filter)
    elif length == 4:
        test(file,filter,fileReplacer)
    else: 
        print("Please check for any typos, or refer to documentation.")


if __name__ == '__main__':
    # Interpreting provided arguments.
    lengthOf = len(s.argv[0:])
    if lengthOf == 1:
        main(lengthOf)
    elif lengthOf == 2:
        main(lengthOf)
    elif lengthOf == 3:
        filer = s.argv[1]
        filterState = int(s.argv[2])
        main(lengthOf,filer,filterState)
    else:
        filer = s.argv[1]
        fileReplacer = s.argv[3]
        filterState = s.argv[2]
        main(lengthOf,filer,filterState,fileReplacer)