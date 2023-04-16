from cmu_graphics import *
import random, time
from PIL import Image
import os, pathlib


class Fruit:
    def __init__(self):
        # Draw fruit images here
        self.x = random.randint(100, 1400)
        self.y = 1000 # Initial position 
        self.dy = 25 # Initial velocity 
        self.ddy = -0.8 # Acceleration 
        self.radius = 30
    
    def drawFruit(self):
        drawCircle(self.x, self.y, self.radius, fill = 'black')
    
    def fruitFlying(self):
        self.y -= self.dy 
        self.dy += 0.5 * self.ddy
            
    def offScreen(self):
        if self.y >= 1500 - self.radius:
            return True
        else:
            return False

class Blade:
    def __init__(self):
        pass

def onAppStart(app):
    app.width = 1500
    app.height = 1000
    app.rx = 200
    app.ry = 200
    app.score = 0
    app.lives = 3
    app.homescreen = True
    app.classicRectX = 476
    app.classicRectY = 522
    app.zenRectX = 876
    app.zenRectY = 522
    app.classic = False
    app.zen = False
    app.gameOver = False
    app.level = digitCount(app.score) - 1

    app.fruits = []
    app.lastFruitTime = time.time()

    # Title image
    app.titleURL = Image.open('title.png')
    app.titleWidth,app.titleHeight = app.titleURL.width,app.titleURL.height
    app.titleURL = CMUImage(app.titleURL)



def drawHomescreen(app):
    newTitleWidth, newTitleHeight = 800, 500
    drawImage(app.titleURL, app.width/2, 300, width = newTitleWidth,
              height= newTitleHeight, align = 'center')
    # drawLabel("Fruit Ninja", app.width/2, 300, size = 80, bold=True, align = "center")
    drawRect(app.classicRectX, app.classicRectY, 150, 60, fill = 'lightblue') # Classic button
    drawRect(app.zenRectX, app.zenRectY, 150, 60, fill = 'lightblue') # Zen button
    drawLabel("Classic", 550 , 550, size = 30, bold = True, fill="black")
    drawLabel("Zen", 950, 550, size = 30, bold = True, fill="black")

def drawClassicScreen(app):
    drawLabel(f'Score: {app.score}', 1400, 50, size = 30, bold = True, align = "right")
    drawLabel(f'Lives: {app.lives}', 1400, 100, size = 30, bold = True, align = 'right')
    drawRect(67, 20, 150, 60, fill = 'pink') # End game button
    drawLabel("End Game", 84, 50, size = 25, bold = True, align = "left")

def drawGameOver(app):
    if app.gameOver:
        pass

def gameOver(app):
    if app.lives <= 0:
        app.gameOver = True
        app.classic = False
        app.zen = False

def onMouseDrag(app, mouseX, mouseY):
    # This is called when the user moves the mouse
    # while it IS pressed:
    app.rx = mouseX
    app.ry = mouseY


def redrawAll(app):
    if app.homescreen:
        drawHomescreen(app)
    elif app.classic:
        drawClassicScreen(app)
        for fruit in app.fruits:
            fruit.drawFruit()
    elif app.zen:
        pass
    elif app.gameOver:
        pass


def onMousePress(app, mouseX, mouseY):
    if app.homescreen:
        # If mouse intersects with the classic button
        if ((app.classicRectX <= mouseX <= app.classicRectX + 150) and 
            (app.classicRectY <= mouseY <= app.classicRectY + 60)):
            app.homescreen = False
            app.classic = True
    
    if app.classic:
        # If mouse intersects with the End Game button:
        if (67 <= mouseX <= 217) and (20 <= mouseY <= 80):
            app.gameOver = True  


def onStep(app):
    if app.classic == True and not app.gameOver:
        i = 0
        while i < len(app.fruits):
            fruit = app.fruits[i]
            fruit.fruitFlying()
            if fruit.offScreen():
                app.fruits.pop(i)
                app.lives -= 1
            else:
                i += 1
    
        if (time.time() - app.lastFruitTime > 1) and (len(app.fruits) < app.level):
            app.fruits.append(Fruit())
            app.lastFruitTime = time.time()
        
def digitCount(n):
    n = abs(n)
    if (n == 0):
        return 2
    return math.floor(math.log10(n)) + 1





# def distance(x1,y1,x2,y2):
#     return ((x1-x2)**2 + (y1-y2)**2)**(0.5)

def main():
    runApp()

main()
