import shapes_lib as sl
import turtle as t
import math as m
'''
main.py Roman Schiffino 151B Fall Semester
This is my project file late as it may be. 
It basically is a basic 3d renderer/3d point modeler.
'''


def main():
    '''
    This is the main function that initiates the drawing and ajusts a couple turtle settings.
    '''
    #Disables tracer. If you want to see it trace do recognize it is slow. If you want to not wait over 3 minutes along ith tracer comment out sl.floor().
    t.speed(0)
    #Sky color.
    t.bgcolor("#3274be")
    sl.floor()
    sl.leftWingLeft()
    sl.lefttWingRoofleft()
    sl.rightWingRight()
    sl.rightWingRoofRight()
    sl.mainBodyBack()
    sl.mainBodyRoof()
    sl.mainBodyFront()
    sl.leftWingRight()
    sl.leftWingFront()
    sl.rightWingLeft()
    sl.rightWingFront()
    sl.rightWingRoofLeft()
    sl.leftWingRoofRight()
    sl.mainBodyTopRoof()
    sl.towerLevel5()
    sl.towerLevel4()
    sl.towerLevel3()
    sl.towerLevel2Trim()
    sl.towerLevel2()
    sl.towerLevel1()
    sl.towerLevel1Trim()
    sl.front()
    #Remove cursor.
    t.hideturtle()
    #Update canvas.
    t.update()
    #Exit.
    t.exitonclick()
    

main()