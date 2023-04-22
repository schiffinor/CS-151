'''lab4_zelle_demo.py
A basic program with a shape in the Zelle Graphics Module
Oliver W. Layton
CS 151: Computational Thinking: Visual Media
Fall 2021
'''
import graphics as gr


# Create the screen
w = 600
h = 600
screen = gr.GraphWin('My Oval', width=w, height=h)

# Create an oval shape
oval = gr.Oval(gr.Point(300, 300), gr.Point(480, 400))

# Set the fill color, outline width, and outline color (as RGB color)
oval.setFill('blue')
oval.setOutline(gr.color_rgb(255, 0, 0))  # red
oval.setWidth(5)

# Draw the oval to the screen
oval.draw(screen)

# Pause until we click
screen.getMouse()

# After we click, remove the oval from the screen, pausing again to see the blank screen
oval.undraw()
screen.getMouse()

# Close the window after the 2nd click
screen.close()
