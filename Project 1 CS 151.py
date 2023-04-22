from turtle import *
a = "What Shape would you like to draw?"
b = "Input how many sides you'd like your polygon to have: "
print(a)
print()
sides = input(b)
extAngle = 180 + 360 / int(sides) 
print(extAngle)
