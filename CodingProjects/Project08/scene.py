import turtle
import lsystem
import turtle_interpreter as ti
import ctypes

def main():
    
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    lsys1 = lsystem.Lsystem(filename="myLSystem.txt")
    lsys2 = lsystem.Lsystem(filename="myLSystem2.txt")
    inter = ti.TurtleInterpreter(width=800, height=800, bgColor='#58A8FF')
    wreath = "F[-F][-<gL]<rB>[++gL>][-F[-F][-F[-<gL][++gL>]F][-F-F][-F-F][-F][+<gL][++gL>]<rB>[-F[-F][-F[-F][-F[-<gL][++gL>]F][-F-F][-F-F][-F][+<gL][++gL>]<rB>][-F[-F][-F[-F][-F[-<gL][++gL>]F][-F-F][-F-F][-F][+<gL][++gL>]<rB>[-F[-F][-F[-F][-F[-<gL][++gL>]F][-F-F][-F-F][-F][+<gL][++gL>]<rB>][-F[-F][-F[-F][-F[-<gL][++gL>]F][-F-F][-F-F][-F][+<gL][++gL>]<rB>[-<gL][++gL>]F[-F][-F[-F][-F[-<gL][++gL>]F][-F-F][-F-F][-F][+<gL][++gL>]<rB>][-F[-F][-F[-F][-F[-<gL][++gL>]F][-F-F][-F-F][-F][+<gL][++gL>]<rB>-F[-F][-F[-F][-F[-<gL][++gL>]F][-F-F][-F-F][-F][+<gL][++gL>]<rB>][-F[-F][-F[-F][-F[-<gL][++gL>]F][-F-F][-F-F][-F][+<gL][++gL>]<rB>-F[-F][-F[-F][-F[-<gL][++gL>]F][-F-F][-F-F][-F][+<gL][++gL>]<rB>][-F[-F][-F[-F][-F[-<gL][++gL>]F][-F-F][-F-F][-F][+<gL][++gL>]<rB>][+<gL][++gL>]<rB>"
    wreath2 = "F[-F][-<gl]<rB>[++gl>][-F[-F][-F[-<gl][++gl>]F][-F-F][-F-F][-F][+<gl][++gl>]<rB>[-F[-F][-F[-F][-F[-<gl][++gl>]F][-F-F][-F-F][-F][+<gl][++gl>]<rB>][-F[-F][-F[-F][-F[-<gl][++gl>]F][-F-F][-F-F][-F][+<gl][++gl>]<rB>[-F[-F][-F[-F][-F[-<gl][++gl>]F][-F-F][-F-F][-F][+<gl][++gl>]<rB>][-F[-F][-F[-F][-F[-<gl][++gl>]F][-F-F][-F-F][-F][+<gl][++gl>]<rB>[-<gl][++gl>]F[-F][-F[-F][-F[-<gl][++gl>]F][-F-F][-F-F][-F][+<gl][++gl>]<rB>][-F[-F][-F[-F][-F[-<gl][++gl>]F][-F-F][-F-F][-F][+<gl][++gl>]<rB>-F[-F][-F[-F][-F[-<gl][++gl>]F][-F-F][-F-F][-F][+<gl][++gl>]<rB>][-F[-F][-F[-F][-F[-<gl][++gl>]F][-F-F][-F-F][-F][+<gl][++gl>]<rB>-F[-F][-F[-F][-F[-<gl][++gl>]F][-F-F][-F-F][-F][+<gl][++gl>]<rB>][-F[-F][-F[-F][-F[-<gl][++gl>]F][-F-F][-F-F][-F][+<gl][++gl>]<rB>][+<gl][++gl>]<rB>"
    wreath = wreath[0:int(len(wreath)/2-90)]
    wreath2 = wreath2[0:int(len(wreath2)/2-90)]
    inter.setColor('#492A10')
    inter.goto(0,400,90)
    for i in range(8):
        inter.drawString(wreath, -20, 22)
        inter.turtle.setheading(90)
    inter.goto(0,400,-90)
    for i in range(8):
        inter.drawString(wreath2, 20, -22)
        inter.turtle.setheading(-90)
    size = 20
    inter.setWidth(5)
    for i in range(8):
        inter.goto(500-i*50,-200,90)
        inter.setColor('#492A10')
        inter.drawString(lsys2.buildString(2), size, -22)
        size -= 2
    size = 20
    for i in range(8):
        inter.goto(-500+i*50,-200,90)
        inter.setColor('#492A10')
        inter.drawString(lsys2.buildString(2), size, 22)
        size -= 2
    inter.goto(300,400,90)
    inter.setColor('#492A10')
    inter.drawString(lsys1.buildString(3), 20, 22)
    inter.goto(-400,400,90)
    inter.setColor('#492A10')
    inter.drawString(lsys1.buildString(3), 20, 22)
    inter.goto(-800,-200,0)
    inter.turtle.begin_fill()
    inter.setColor("white")
    inter.drawString("F-F-F-F", 1600, 90)
    inter.turtle.end_fill()
    inter.goto(200,100,0)
    inter.turtle.begin_fill()
    inter.setColor("yellow")
    inter.drawString("B", 400, 90)
    inter.turtle.end_fill()
    inter.hold()

main()