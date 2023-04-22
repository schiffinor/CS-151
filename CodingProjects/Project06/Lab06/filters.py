'''
filters.py
Roman Schiffino 151B Fall Semester
This is the lab version of the pilters.py file. It does exactly what the lab asks no more no less.
'''
import graphics as gr
import display as d
import tkinter as tk
import sys as s


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
    for i in range(img.getWidth()):
        for j in range(img.getHeight()):
            img.setPixel(i,j,hexColor(tuple(map(lambda x: img.getPixel(i,j)[x],[0,2,1]))))
    return img


def test(fileName):
    '''
    just applies out filter.
    '''
    image = "Project06\Lab06\ ".rstrip(" ")+str(fileName)
    myImage = gr.Image(gr.Point(0,0),image)
    moddedImage = swapGreenBlue(myImage)
    moddedImage.save("Project06\Lab06\modded"+str(fileName))
    screen = d.displayImage(moddedImage,"Dabba Doo, Dabba Dee")
    # Honestly this logo is barely viible but I made the effort so here it is.
    logo = tk.PhotoImage(file="Project06\Lab06\Daco_6135086.png")
    # Sets Icon.
    screen.master.iconphoto(False, logo)
    screen.getMouse()
    screen.close()


def main(length,file=" ",filter=0):
    global screen
    if length == 1:
        print("Usage Example: python3 Project06/Lab06/filters.py <filename of image> <0/1>")
        print("When you would like the filter to go into affect please add the 1.")
    elif length == 2:
        image = "Project06\Lab06\ ".rstrip(" ")+str(file)
        myImage = gr.Image(gr.Point(0,0),image)
        screen = d.displayImage(myImage,"Dabba Doo, Dabba Dee")
        # Honestly this logo is barely viible but I made the effort so here it is.
        logo = tk.PhotoImage(file="Project06\Lab06\Daco_6135086.png")
        # Sets Icon.
        screen.master.iconphoto(False, logo)
        # Sets inital screenstate as not fullscreen.
        screen.master.attributes("-fullscreen", False)
        screen.getMouse()
        screen.close()
    elif length == 3 and filter == 1:
        test(file)
    else: 
        print("Please check for any typos, or refer to documentation.")


if __name__ == '__main__':
    lengthOf = len(s.argv[0:])
    if lengthOf == 1:
        main(lengthOf)
    elif lengthOf == 2:
        filer = s.argv[1]
        main(lengthOf,filer)
    else:
        filer = s.argv[1]
        filterState = int(s.argv[2])
        main(lengthOf,filer,filterState)