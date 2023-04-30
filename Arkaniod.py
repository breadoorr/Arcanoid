from tkinter import *
#declaring and initializing variables that will be used throughout the game
WIDTH = 800  
HEIGHT = 600
DELAY = 20
colors = (['red', 'orange',  'yellow', 'green', 'blue', 'aqua', 'cyan', 'pink'])
bricks = []
balls = []
string = 5
column = 20
point = 0
level1 = 1

#creating a window with a game
#reference: CO1417, week01-drawing-colored-shapes, step0102, WelcomeGraphics.py
win = Tk()
win.title('Arkanoid')
win.geometry(str(WIDTH)+ "x"+ str(HEIGHT))
canvas = Canvas(win, width=WIDTH, height=HEIGHT)
#importing an image for the background of the window
#Reference: https://www.geeksforgeeks.org/how-to-use-images-as-backgrounds-in-tkinter/ , Method 2.
bg = PhotoImage(file = "D:\PycharmProjects\CO1417\week04-capstone-arkanoid\\file.png")
canvas.create_image( 0, 0, image = bg, anchor= 'nw')
canvas.pack()

#creating classes for craft, bricks, ball and score
class Craft:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.canvas_object = canvas.create_rectangle(self.x - self.width, self.y - self.height-5, self.x + self.width, self.y-5, fill=self.color)
    #reference for movement: CO1417, week02-event-driven-programming, xtras, bottomRec0201.py
    def move(self, event):
        if event.x <= WIDTH-self.width - 5 and event.x >= self.width + 5:
            self.x = event.x


class Brick:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.canvas_object = canvas.create_rectangle(self.x+3, self.y+3, self.x + self.width-2, self.y + self.height-2, fill=self.color)

#reference for a ball class: CO1417, weeek 3-animation, step0306, COllisions.py
class Ball:
    def __init__(self, x, y, radius, speed_x, speed_y, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color
        self.canvas_object = canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius, fill=self.color)

    def move(self):
        self.x += self.speed_x
        if self.x >= WIDTH - self.radius:
            self.speed_x = -abs(self.speed_x)
        if self.x <= self.radius:
            self.speed_x = abs(self.speed_x)
        self.y += self.speed_y
        if self.y <= self.radius:
            self.speed_y = abs(self.speed_y)
        if self.y >= craft.y - craft.height-5 - self.radius and self.x >= craft.x - craft.width  and self.x <= craft.x + craft.width:
            self.speed_y = -abs(self.speed_y)
            if self.x +self.radius== craft.x - craft.width:
                self.speed_x = -abs(self.speed_x)
            elif self.x -self.radius== craft.x + craft.width:
                self.speed_x = abs(self.speed_x)
        #if ball touches the bottom of the window 
        #"GAME OVER" is being printed and ball is being deleted from the canvas
        if self.y >= HEIGHT:
            loose = Score(
            WIDTH//2, HEIGHT//2, 'GAME\nOVER', 'Tahoma', 50, 'red'
            )
            canvas.delete(ball.canvas_object)

        
class Score:
    def __init__(self, x, y, text, font, size, color):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.canvas_object = canvas.create_text(self.x, self.y, text=self.text, font= (self.font, self.size), fill = self.color)

#initializing instances for the classes above
#craft as an instance for a craft class
craft = Craft (
    x = WIDTH//2,
    y = HEIGHT,
    width = 35,
    height = 10,
    color = 'cyan'
)
# ball as an instance for a ball class
ball = Ball(
    x = WIDTH//2, 
    y = HEIGHT//2, 
    radius= 10,
    speed_x= 5,
    speed_y= 5, 
    color='red'
)
#score as instance for a score class
score = Score(
    30, HEIGHT-10, point, 'Tahoma', 15, 'white'
)

#function that creates bricks in the window
def create_brick():
    for i in range(string):
        for j in range(column):
            brick = Brick(
                j*WIDTH//column, i * HEIGHT//string*0.2, WIDTH//column, 
                HEIGHT//string*0.2, colors[i])
            bricks.append(brick)

#function that detectes collision between bricks and a ball
# and deletes a brick that was collided
# also adds 10 points for each collided brick
# reference: CO1417, week 3-animation, xtras, Exercise0302     
def crash():
    global bricks, point, level1, Brick, ball
    for brick in bricks:
        if ball.y <= brick.y + brick.height-2 + ball.radius and ball.x >= brick.x +3  and ball.x <= brick.x + brick.width-2:
            ball.speed_y = abs(ball.speed_y)
            canvas.delete(brick.canvas_object)
            bricks.pop(bricks.index(brick))
            point = point + 10  
            # if there are no more bricks and level is less than 3 new level is created
            if len(bricks)==0:
                if level1<3:
                    level1+=1
                    level()
                    #else prints "YOU WON" 
                else:
                    winn = Score(
                WIDTH//2, HEIGHT//2, 'YOU\nWON', 'Tahoma', 50, 'red')
                    canvas.delete(ball.canvas_object)

#function that allows canvas objects to move in canvas space
# Reference: CO1417 course, week 3-animation, step0304, BallAsAClass.py        
def animation():
    crash() #
    ball.move()
    win.bind('<Motion>', craft.move)
    for brick in bricks:
        canvas.coords(brick.canvas_object, brick.x+3, brick.y+3, brick.x + brick.width-2, brick.y + brick.height-2)
    canvas.coords(craft.canvas_object, craft.x-craft.width, craft.y - craft.height -5, craft.x + craft.width, craft.y-5)
    canvas.coords(ball.canvas_object, ball.x - ball.radius, ball.y - ball.radius, ball.x + ball.radius, ball.y+ ball.radius)
    canvas.itemconfig(score.canvas_object, text = point, font=(score.font, score.size), fill=score.color)
    canvas.after(DELAY, animation)

#function that changes the speed of the ball depending on level
# and also creates a new set of bricks for each new level
def level():
    global level1
    if level1 == 2:
        create_brick()
        ball.speed_y+=1
        ball.speed_x+= 1
    if level1 == 3:
        create_brick()
        ball.speed_x+=1
        ball.speed_y+=1
        


#function calls for creating bricks and movements of ball and craft
create_brick()
animation()
win.mainloop()