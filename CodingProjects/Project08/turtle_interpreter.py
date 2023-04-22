import turtle as t

class TurtleInterpreter:
    
    def __init__(self, width=800, height=800, bgColor='white'):
        '''TurtleInterpreter constructor.
        Creates instance variables for a Turtle object and a Screen object with a particular window
        `width`, `height`, and background color `bgColor`.
        '''
        # Create a Turtle object, set it as an instance variable

        # Create a Screen object, set it as an instance variable.
        # Set the screen's height, width, and color based on the parameters

        # Turn the screen's tracer off.
        self.turtle = t.Turtle()
        self.screen = t.Screen()
        self.height = height
        self.width = width
        self.bgColor = bgColor
        self.screen.screensize(self.width,self.height,bgColor)
        self.screen.tracer(False)

    def setColor(self,color):
        self.turtle.color(color)

    def setWidth(self,width):
        self.turtle.pensize(width)

    def goto(self,x,y,heading=None):
        self.turtle.up()
        self.turtle.goto(x,y)
        self.turtle.down()
        if heading != None:
            self.turtle.setheading(heading)
    
    def getScreenWidth(self):
        return self.screen.screensize()[0]

    def getScreenHeight(self):
        return self.screen.screensize()[1]

    def hold(self):
        '''Holds the screen open until user clicks or presses 'q' key'''

        # Hide the turtle cursor and update the screen
        self.turtle.hideturtle()
        self.screen.update()

        # Close the window when users presses the 'q' key
        self.screen.onkey(t.bye, 'q')

        # Listen for the q button press event
        self.screen.listen()

        # Have the turtle listen for a click
        self.screen.exitonclick()

    def drawString(self, lsysString, distance, angle):
        '''Interpret each character in an L-system string as a turtle command.

        Here is the starting L-system alphabet:
            F is forward by a certain distance
            + is left by an angle
            - is right by an angle

        Parameters:
        -----------
        lsysString: str. The L-system string with characters that will be interpreted as drawing
            commands.
        distance: distance to travel with F command.
        angle: turning angle (in deg) for each right/left command.
        '''

        # Walk through the lsysString character-by-character and
        # have the turtle object (instance variable) carry out the
        # appropriate commands

        # Call the update method on the screen object to make sure
        # everything drawn shows up at the very end of the method
        # (remember: you turned off animations in the constructor)
        positionTracker = []
        headingTracker = []
        colorTracker = []
        widthTracker = []
        '''
            elif character == "text":
                self.turtle.FUNC
            '''
        for character in lsysString:
            if character == "F":
                self.turtle.forward(distance)
            elif character == "+":
                self.turtle.left(angle)
            elif character == "-":
                self.turtle.right(angle)
            elif character == "[":
                positionTracker.append(self.turtle.pos())
                headingTracker.append(self.turtle.heading())
            elif character == "]":
                position = positionTracker.pop()
                heading = headingTracker.pop()
                self.goto(*position,heading)
            elif character == "<":
                colorTracker.append(self.turtle.color()[0])
            elif character == ">":
                color = colorTracker.pop()
                self.setColor(color)
            elif character == "g":
                self.setColor((0.15, 0.5, 0.2))
            elif character == "y":
                self.setColor((0.8, 0.8, 0.3))
            elif character == "r":
                self.setColor((0.7, 0.2, 0.3))
            elif character == "L":
                self.turtle.begin_fill()
                self.turtle.circle(distance/2,-180)
                self.turtle.end_fill()
            elif character == "l":
                self.turtle.begin_fill()
                self.turtle.circle(distance/2,180)
                self.turtle.end_fill()
            elif character == "B":
                self.turtle.begin_fill()
                self.turtle.circle(distance/4,)
                self.turtle.end_fill()

        self.screen.update()