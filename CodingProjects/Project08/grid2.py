import lsystem
import turtle_interpreter as ti
import ctypes

def main():
    
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    lsys = lsystem.Lsystem(filename="myLSystem2.txt")
    inter = ti.TurtleInterpreter(width=800, height=800, bgColor='white')
    inter.setWidth(2)
    angles = [22,46,60]
    
    for x in range(3):
        for y in range(3):
            lsysString = lsys.buildString(x+1)
            inter.setColor('brown')
            inter.goto(-400+400*x,200-400*y,90)
            inter.drawString(lsysString, 20, angles[y])
    
    inter.hold()

main()