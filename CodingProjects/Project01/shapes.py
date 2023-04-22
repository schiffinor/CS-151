import turtle as t
import math as m

# this is the composition just calls and gives parameters.
# All shape constructions are more comprehensibly explained in their respective files.
def composition():
    t.hideturtle()
    t.speed(1000)
    heart(1,0,0)
    cross(1,0,0)
    cross(.35,280,365)
    cross(.35,-280,365)
    cross(.55,275,-280)
    cross(.55,-275,-280)
    t.bgcolor("black")
    t.exitonclick()
 
# hopefully interesting and creative design
def shapeThree():
# all parameters
    xOffsetHearts = 0
    xOffsetCrosses = 0
    xOffsetStars = 330
    yOffsetHearts = 0
    yOffsetCrosses = 0
    yOffsetStars = 250
    scaleHearts = 1
    scaleCrosses = .75
    scaleStars = .5
    t.hideturtle()
    t.speed(1000)
    heart(scaleHearts,xOffsetHearts,yOffsetHearts)
    cross(scaleCrosses,xOffsetCrosses,yOffsetCrosses)
    t.bgcolor("black")
    t.exitonclick()

def heart(scaleHeart,xOffsetHeart,yOffsetHeart):
# polar defined function converted to cartesian coordinates
    t.fillcolor("red")
    t.begin_fill()
    for deg in range(0,360):
# unit conversion because radians.
        theta = m.radians(deg)
# polar function converted to cartesian coordinates
        x = scaleHeart*(320*((m.sin(theta))**3))
        y = scaleHeart*((260*(m.cos(theta)))-(100*(m.cos(2*theta)))-(40*(m.cos(3*theta)))-(20*(m.cos(4*theta))))
# removes initial origin line
        if deg == 0:
            t.up()
            t.goto(x+xOffsetHeart,y+yOffsetHeart)
            t.down()
# calls function        
        else:
            t.goto(x,y)
    t.end_fill()

def cross(scaleCross,xOffsetCross,yOffsetCross):
# angles for seth command
    d = (90,120,30,-30,-120,-90,0,30,-60,-120,-210,-180,-90,-60,-150,-210,-300,90,180,210,120,60,-30,0)
# distances for fd command
    e = (200,25,25,25,25,200,200,25,25,25,25,200,300,25,25,25,25,300,200,25,25,25,25,200)
    t.up()
# account for of..fsetting to center 
    t.setpos(scaleCross*(xOffsetCross-9.1506),scaleCross*yOffsetCross)
    t.down()
    t.fillcolor("white")
    t.begin_fill()
    for iter in range(24):
        t.seth(d[iter])
        t.fd(scaleCross*e[iter])
    t.end_fill()
# Star function
def star(scaleStar,xOffsetStar,yOffsetStar):
# x coordinates of outer vertices
    d = (0,-122,-222.9,-285.3,-298.4,-259.8,-176.3,-62.4,62.4,176.3,259.8,298.4,285.3,222.9,122)
# y coordinates of outer vertices
    e = (300,274.1,200.7,92.7,-31.4,-150,-242.7,-293.4,-293.4,-242.7,-150,-31.4,92.7,200.7,274.1)
#vector angles
    f = (90,114,138,162,186,210,234,258,282,306,330,354,378,402,426)
    t.up()
    t.setpos((0*scaleStar)+xOffsetStar,(300*scaleStar)+yOffsetStar)
    t.down()
    t.fillcolor("white")
    t.begin_fill()
# for loops to iterate through lists of positions    
    for iter in range(15):
        t.goto((scaleStar*d[iter])+xOffsetStar,(scaleStar*e[iter])+yOffsetStar)
        t.seth((f[iter] - 180) - 1.1)
        t.fd(scaleStar*275.549)
    t.end_fill()
    t.begin_fill()
    for iter in range(15):
        t.goto((scaleStar*d[iter])+xOffsetStar,(scaleStar*e[iter])+yOffsetStar)
        t.seth((f[iter] - 180) + 1.1)
        t.fd(scaleStar*275.549)
    t.setpos((0*scaleStar)+xOffsetStar,(300*scaleStar)+yOffsetStar)
    t.end_fill()

composition()