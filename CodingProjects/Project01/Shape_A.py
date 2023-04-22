import turtle as t
a = "We will draw a shape!"
b = "Press Enter to begin shape drawing."
# I forgot about the range command, buth these are the lists that the for loop iterates through. First is just my replacement for the range command.
# The second line is the angles for the turtle to go in. The third line is the distances the turtle will travel.
c = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23)
d = (90,120,30,-30,-120,-90,0,30,-60,-120,-210,-180,-90,-60,-150,-210,-300,90,180,210,120,60,-30,0)
e = (200,25,25,25,25,200,200,25,25,25,25,200,300,25,25,25,25,300,200,25,25,25,25,200)
# This just prints the statements and gets a user input to initiate the drawing.
print(a)
print()
start = input(b)
# This just does all the drawing.
t.hideturtle()
for iter in c:
    t.seth(d[iter])
    t.fd(e[iter])
t.exitonclick()