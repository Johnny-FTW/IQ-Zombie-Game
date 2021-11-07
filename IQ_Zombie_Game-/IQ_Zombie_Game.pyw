import tkinter as tk
import random
import time

class Game(tk.Tk):
    cc = 0
    def __init__(self):
        super().__init__()

        self.create_background()
        self.player = Player(self.canvas)
        self.food = self.add_food()
        self.bind_all_events()

        self.time = 10
        self.game_started = time.time()
        self.time_label = self.canvas.create_text(self.bg.width()-50,30,text="00", font="arial 30",fill="red")
        self.ca = self.score()

    def score(self):
        self.cc = self.cc +1
        self.canvas.after(1000,self.score)
        return self.cc

    def display_game_time(self):
        t = self.time - int(time.time() - self.game_started)
        seconds = t
        time_string ="{:02d}".format(seconds)
        self.canvas.itemconfig(self.time_label, text=time_string)
        self.canvas.create_text(self.bg.width()-125,30,text = "IQ:",font="arial 30",fill="red")
        return t

    def create_background(self):
        self.bg = tk.PhotoImage(file="background.png")
        self.canvas = tk.Canvas(width=self.bg.width(), height=self.bg.height())
        self.canvas.pack()
        self.canvas.create_image(self.bg.width() / 2, self.bg.height() / 2, image=self.bg)

    def bind_all_events(self):
        self.canvas.bind_all("<KeyPress-Right>", self.player.keypress_right)
        self.canvas.bind_all("<KeyRelease-Right>", self.player.keyrelease_right)
        self.canvas.bind_all("<KeyPress-Left>", self.player.keypress_left)
        self.canvas.bind_all("<KeyRelease-Left>", self.player.keyrelease_left)

    def add_food(self):
        food_list = [f1, f2, f0, f3, f4, f5, f6, f7]
        food_type = random.choice(food_list)
        food = food_type(self.canvas)
        return food

    def timer(self):
        self.player.tik()
        self.food.tik()

        if self.food.destroyed:
            self.food = self.add_food()
        if self.player.eat(self.food):
            self.time += self.food.value
            self.food= self.add_food()

        t = self.display_game_time()
        if t<= 0:
            self.game_over()
        else:
            self.canvas.after(40, self.timer)

    def game_over(self):
        self.player.destroy()
        self.food.destroy()

        self.canvas.create_text(self.bg.width()/2,100, text="GAME OVER", font="arial 60", fill="red")
        text = "SCORE: {}".format(self.cc)
        self.canvas.create_text(self.bg.width() / 2, 250, text=text, font="arial 30", fill="red")
        h0 = h1 = h2 = h3 = h4 = h5 = h6 = h7 =0
        for food in self.player.eaten_food:
            if isinstance(food, f0):
                h0 +=1
            elif isinstance(food, f1):
                h1 +=1
            elif isinstance(food, f2):
                h2 +=1
            elif isinstance(food, f3):
                h3 +=1
            elif isinstance(food, f4):
                h4 +=1
            elif isinstance(food, f5):
                h5 +=1
            elif isinstance(food, f6):
                h6 +=1
            elif isinstance(food, f7):
                h7 +=1

        self.f0 = self.display_food_stats("food/0.png",h0,300,"lime")
        self.f1 = self.display_food_stats("food/1.png", h1, 400,"lime")
        self.f2 = self.display_food_stats("food/2.png", h2, 500,"lime")
        self.f3 = self.display_food_stats("food/3.png", h3, 600,"lime")
        self.f4 = self.display_food_stats("food/4.png", h4, 700,"red")
        self.f5 = self.display_food_stats("food/5.png", h5, 800,"red")
        self.f6 = self.display_food_stats("food/6.png", h6, 950,"red")
        self.f7 = self.display_food_stats("food/7.png", h7, 1050,"red")

    def display_food_stats(self, file_path, count, position,color):
        img = tk.PhotoImage(file=file_path)
        self.canvas.create_image(position, self.bg.height()/2, image=img)
        self.canvas.create_text(position, self.bg.height()/2+50, text=str(count), font = "arial 20", fill=color)
        return img

class BaseSprite:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x, self.y = x, y
        self.id = self.canvas.create_image(x, y)
        self.destroyed = False

    def load_sprites(self, file_path, rows, cols):
        sprite_img = tk.PhotoImage(file=file_path)
        sprites=[]
        height = sprite_img.height()//rows
        width = sprite_img.width()//cols
        for row in range(rows):
            for col in range(cols):
                l = col*width
                t = row*height
                r = (col+1)*width
                b = (row+1)*height
                subimage = self.create_subimage(sprite_img, l, t, r, b)
                sprites.append(subimage)
        return sprites

    def create_subimage(self, img, left, top, right , bottom):
        subimage = tk.PhotoImage()
        subimage.tk.call(subimage, "copy", img, "-from", left, top, right, bottom, "-to", 0, 0)
        return subimage

    def tik(self):
        pass

    def destroy(self):
        self.destroyed = True
        self.canvas.delete(self.id)

class Food(BaseSprite):
    value = 0
    speed = 0

    def __init__(self, canvas):
        x = random.randrange(100, 1181)
        y = 0

        super().__init__(canvas, x, y)
        self.smer= random.randrange(-20,20)


    def move(self):
        y = self.y + self.speed


        if y <= self.canvas.winfo_height()-70:
            self.y = y

        else:
            self.smer = random.randrange(-20,20)
            self.destroy()

        self.x = self.x + self.smer

        if self.x >= self.canvas.winfo_width():
            self.smer = self.smer*-1
        elif self.x <= 0:
            self.smer = self.smer * -1

        self.canvas.coords(self.id, self.x, self.y)

    def tik(self):
        self.move()


class f0(Food):
    value = 3
    speed = 6
    def __init__(self, canvas):
        super().__init__(canvas)
        self.sprites = self.load_sprites("food/0.png",1,1)
        self.canvas.itemconfig(self.id, image= self.sprites[0])

class f1(Food):
    value = 8
    speed = 12
    def __init__(self, canvas):
        super().__init__(canvas)
        self.sprites = self.load_sprites("food/1.png",1,1)
        self.canvas.itemconfig(self.id, image= self.sprites[0])

class f2(Food):
    value = 6
    speed = 10
    def __init__(self, canvas):
        super().__init__(canvas)
        self.sprites = self.load_sprites("food/2.png",1,1)
        self.canvas.itemconfig(self.id, image= self.sprites[0])

class f3(Food):
    value = 15
    speed = 20
    def __init__(self, canvas):
        super().__init__(canvas)
        self.sprites = self.load_sprites("food/3.png",1,1)
        self.canvas.itemconfig(self.id, image= self.sprites[0])

class f4(Food):
    value = -20
    speed = 20
    def __init__(self, canvas):
        super().__init__(canvas)
        self.sprites = self.load_sprites("food/4.png",1,1)
        self.canvas.itemconfig(self.id, image= self.sprites[0])

class f5(Food):
    value = -20
    speed = 20
    def __init__(self, canvas):
        super().__init__(canvas)
        self.sprites = self.load_sprites("food/5.png",1,1)
        self.canvas.itemconfig(self.id, image= self.sprites[0])

class f6(Food):
    value = -20
    speed = 20
    def __init__(self, canvas):
        super().__init__(canvas)
        self.sprites = self.load_sprites("food/6.png",1,1)
        self.canvas.itemconfig(self.id, image= self.sprites[0])

class f7(Food):
    value = -20
    speed = 20
    def __init__(self, canvas):
        super().__init__(canvas)
        self.sprites = self.load_sprites("food/7.png",1,1)
        self.canvas.itemconfig(self.id, image= self.sprites[0])


class Player(BaseSprite):
    LEFT = "left"
    RIGHT = "right"
    IDLE = "idle"
    MOVE = "move"

    def __init__(self, canvas, x=600, y=590):
        super().__init__(canvas, x, y)
        self.sprite_sheet = self.load_all_sprites()
        self.movement = self.IDLE
        self.direction = self.LEFT
        self.sprite_idx = 0
        self.dx = self.dy = 0
        self.keys_pressed = 0
        self.eaten_food = []

    def eat(self, food):
        dst = ((self.x - food.x)**2 + (self.y - food.y)**2)**0.5
        if dst < 100:
            self.eaten_food.append(food)
            food.destroy()
            return True
        return False


    def load_all_sprites(self):
        sprite_sheet = {
            "idle" : {
                "left" : [],
                "right" : []
            },
            "move" : {
                "left" : [],
                "right" : []
            }
        }
        sprite_sheet["idle"]["left"] = self.load_sprites("player/left_idle.png",1,10)
        sprite_sheet["idle"]["right"] = self.load_sprites("player/right_idle.png",1,10)
        sprite_sheet["move"]["left"] = self.load_sprites("player/left_move.png", 1, 10)
        sprite_sheet["move"]["right"] = self.load_sprites("player/right_move.png", 1, 10)
        return sprite_sheet

    def next_animation_index(self, idx):
        idx +=1
        max_idx = len(self.sprite_sheet[self.movement][self.direction])
        idx = idx % max_idx
        return idx

    def tik(self):
        self.sprite_idx = self.next_animation_index(self.sprite_idx)
        img = self.sprite_sheet[self.movement][self.direction][self.sprite_idx]
        self.canvas.itemconfig(self.id, image=img)
        if self.movement == self.MOVE:
            self.move()

    def move(self):
        x = self.x + self.dx
        y = self.y + self.dy
        if x >= 100 and x <= self.canvas.winfo_width()-100:
            self.x = x
        if y >= 35 and y <= self.canvas.winfo_width()-35:
            self.y = y
        self.canvas.coords(self.id, x, y)

    def keypress_right(self, event):
        self.movement = self.MOVE
        self.direction = self.RIGHT
        self.keys_pressed += 1
        self.dx = 10

    def keyrelease_right(self, event):
        self.dx = 0
        self.keys_pressed -= 1
        if self.keys_pressed ==0:
            self.movement = self.IDLE

    def keypress_left(self, event):
        self.movement = self.MOVE
        self.direction = self.LEFT
        self.keys_pressed += 1
        self.dx = -10

    def keyrelease_left(self, event):
        self.dx = 0
        if self.keys_pressed == 0:
            self.movement = self.IDLE


game = Game()
game.resizable(width=False, height=False)
game.title("IQ Zombie Game")
game.iconbitmap('zb.ico')
game.timer()
game.mainloop()