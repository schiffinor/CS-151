import graphics as gr
import display as d
import tkinter as tk
import sys as s


def main(length,file=" "):
    if length == 1:
        print("Usage Example: python3 Project06/Lab06/show.py winter.ppm")
    if length == 2:
        global screen
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


if __name__ == '__main__':
    lengthOf = len(s.argv[0:])
    if lengthOf == 1:
        main(lengthOf)
    else:
        filed = s.argv[1]
        main(lengthOf,filed)