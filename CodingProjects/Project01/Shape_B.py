import turtle as t
a = "We will draw a shape!"
b = "Press Enter to begin shape drawing."
# These are the x positions for each vertex in the star.
d = (0,-122,-222.9,-285.3,-298.4,-259.8,-176.3,-62.4,62.4,176.3,259.8,298.4,285.3,222.9,122)
# These are the y positions for each vertex in the star.
e = (300,274.1,200.7,92.7,-31.4,-150,-242.7,-293.4,-293.4,-242.7,-150,-31.4,92.7,200.7,274.1)
# These are the angles at which each star vertex is from the origin.
f = (90,114,138,162,186,210,234,258,282,306,330,354,378,402,426)
print(a)
print()
start = input(b)
t.hideturtle()
# This prevents there from being a line between the orign and the first vertex.
t.up()
t.setpos(0,300)
t.down()
# These are the lines in the first dierection.
for iter in range(15):
    t.goto(d[iter],e[iter])
    t.seth((f[iter] - 180) + 1.1)
    t.fd(275.549)
# These are the lines in the other direction.
for iter in range(15):
    t.goto(d[iter],e[iter])
    t.seth((f[iter] - 180) - 1.1)
    t.fd(275.549)
# This completes the shape.
t.goto(0,300)
t.exitonclick()