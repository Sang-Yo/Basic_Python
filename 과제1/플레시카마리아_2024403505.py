import turtle
t1 = turtle.Turtle('turtle')
t1.speed(0)

def square():
    t1.forward(20)
    t1.right(120)
    t1.forward(20)
    t1.right(60)
    t1.forward(20)
    t1.right(120)
    t1.forward(20)
    t1.right(60)
    t1.forward(20)

def drawSide1():
     t1.forward(100)
     t1.right(60)
     t1.forward(100)
     t1.right(120)
     t1.forward(100)
     t1.right(60)
     t1.forward(100)

def goingBack():
     t1.right(120)
     t1.forward(20)
     t1.right(60)
     t1.forward(100)
     t1.right(180)
     
t1.left(120)

for i in range(3):
     drawSide1()

t1.left(60)
for i in range(3):
     drawSide1()

for i in range(3):
    t1.forward(100)
    t1.right(60)

for i in range (6):
    t1.forward(200)
    t1.right(60)

def drawSquares():
    for i in range (5):
       for j in range(5):
           square()
       goingBack()

drawSquares()

t1.right(60)
t1.forward(100)
t1.right(180)

drawSquares()

for i in range(5):
    t1.forward(100)
    t1.right(60)
    drawSquares()

t1.forward(100)
t1.left(60)
drawSquares()

for i in range(2):
    t1.forward(100)
    t1.left(60)
    t1.forward(200)
    t1.left(180)
    drawSquares()
    
    t1.right(60)
    t1.forward(100)
    t1.right(60)
    drawSquares()

t1.hideturtle()
turtle.done()

