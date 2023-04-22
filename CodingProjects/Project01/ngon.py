import turtle as t
a = "What Shape would you like to draw?"
b = "Input how many sides you'd like your polygon to have: "
c = "Input how long you'd like each side of the polyon to be: "
print(a)
print()
# This takes an input from the user on how many sides the polygon will have.
sides = input(b)
# This uses the amount of sides calculated and algorithm i made up to caclulate the extrior angle of whatever polygon is inputted.
# This could be returned as a value if we did so please. However it is just an intermediary. Overall the system could be simplified though.
extAngle = ((int(sides) - 2) * 180) / int(sides)
# This calculates what angle to et the turtle to.
angle = 180 - extAngle
# This takes what length to make each side of the polygon.
length = input(c)
# This iterates trhough the amount of sides and draws 'em.
for iter in range(int(sides)):
    t.right(angle)
    t.forward(int(length))
t.exitonclick()