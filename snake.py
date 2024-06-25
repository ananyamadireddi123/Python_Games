from tkinter import *
import random

HEIGHT=800
WIDTH=800

# speed of the snake = lower the number and faster the game
SPEED=200

SPACE=25  # size of the snake and food
BODY_PARTS=2 # number of body parts with which it starts
COLOR_SNAKE = "#FFFFFF"
COLOR_FOOD = "#00FF00"
BACKGROUND="#000000"


# snake object

class Snake:
    
    def __init__(self):
        self.body=BODY_PARTS
        self.coordinates=[]
        self.ovals = []
        
        for i in range(BODY_PARTS):
            self.coordinates.append([WIDTH/2,HEIGHT/2])
            
        for x,y in self.coordinates:
            oval = canvas.create_oval(x,y,x+SPACE,y+SPACE,fill=COLOR_SNAKE,tag="snake")
            self.ovals.append(oval)


# food object

class Food:

    def __init__(self):
        
        x=random.randint(0,(WIDTH-100)/SPACE) * SPACE
        y=random.randint(0,(HEIGHT-100)/SPACE) * SPACE
        
        self.coordinates=[x,y]
        
        canvas.create_oval(x,y,x+SPACE,y+SPACE,fill=COLOR_FOOD,tag="food")
        
        

# functions required

def next_length(snake,food):
    x,y=snake.coordinates[0]
    
    if direction == "up":
        y=y-SPACE
    elif direction == "down":
        y=y+SPACE
    elif direction == "left":
        x=x-SPACE
    elif direction == "right":
        x=x+SPACE
        
        
    if x<0:
        x=WIDTH-SPACE
    if x>WIDTH:
        x=0
    if y<0:
        y=HEIGHT-SPACE
    if y>HEIGHT:
        y=0               
        
    snake.coordinates.insert(0,(x,y))
    
    oval = canvas.create_oval(x,y,x+SPACE,y+SPACE,fill=COLOR_SNAKE)
    snake.ovals.insert(0,oval)
    
    global score
    global SPEED
    
    
    
    if x==food.coordinates[0] and y==food.coordinates[1]:
        
        # since we are supposed to add a body part to the snake
        # we keep deleting the last part always when it is roaming and add one when food is met 
        
        score+=1
        label.config(text="Score : {}".format(score))
        canvas.delete("food")
        
        food= Food()
    
    else:  
        del snake.coordinates[-1]
        canvas.delete(snake.ovals[-1])  
        del snake.ovals[-1]  
    
    
    if collision(snake):
        end_game()
    else:   
        window.after(SPEED, next_length , snake, food)                

def change_direction(new_direction):
    
    global direction
    
    if new_direction=="left":
        if (direction!="right"):
            direction=new_direction
    if new_direction=="right":
        if (direction!="left"):
            direction=new_direction
    if new_direction=="up":
        if (direction!="down"):
            direction=new_direction
    if new_direction=="down":
        if (direction!="up"):
            direction=new_direction                
        

def collision(snake):
    
    x,y=snake.coordinates[0]
    
    if (x<0 or x> WIDTH):
        next_length(snake,food)
        return False
    elif (y<0 or y> HEIGHT):
        next_length(snake,food)
        return False
    
    for coord in snake.coordinates[1:]:
        if x==coord[0] and y==coord[1]:
            print("GAME OVER")
            return True
    
    return False
    

def end_game():
    
    canvas.delete(all)
    canvas.create_text(window.winfo_width()/2,window.winfo_height()/2-50,font=("Intalic",20),text="GAME OVER",fill="red",tag="gameover")
    


window = Tk()

window.title("Nokia Snake Game")

# resizable function allows to resize the window
window.resizable(False,False)


score=0
direction="up"

label=Label(window,text="Score : {}".format(score),font=("Italic",25))  # to display score
label.pack()

canvas= Canvas(window, bg=BACKGROUND, height=HEIGHT, width=WIDTH)   # make the board where actual game is played
canvas.pack()

window.update()

ww=window.winfo_width()
wh=window.winfo_height()
sw=window.winfo_screenwidth()
sh=window.winfo_screenheight()

centrex=int((sw/2)-(ww/2))
centrey=int((sh/2)-(wh/2))

window.geometry(f"{ww}x{wh}+{centrex}+{centrey}")

window.bind('<Left>', lambda event : change_direction("left"))
window.bind('<Right>', lambda event : change_direction("right"))
window.bind('<Up>', lambda event : change_direction("up"))
window.bind('<Down>', lambda event : change_direction("down"))


snake=Snake()
food=Food()

next_length(snake,food)
 
#keeps the window running 
window.mainloop()
