import turtle as t
a = "What Shape would you like to draw?"
b = "Input how many sides you'd like your polygon to have: "
print(a)
print()
sides = input(b)
extAngle = ((int(sides) - 2) * 180) / int(sides)
angle = 180 - extAngle
for iter in range(int(sides)):
    t.right(angle)
    t.forward(100)
t.exitonclick()