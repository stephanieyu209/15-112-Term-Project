from cmu_graphics import *
import random, time, math
from PIL import Image
import os, pathlib

#-------------------------------------------------------------------------------
# Stephanie Yu's Term Project- Fruit Ninja
# 
# Sources
# Fruit Ninja title image from:
# https://www.cleanpng.com/png-fruit-ninja-puss-in-boots-kinect-xbox-360-android-1010522/download-png.html
#-------------------------------------------------------------------------------

class Fruit:
    def __init__(self):
        # Draw fruit images here
        self.initialX = random.randint(100, 1400)
        self.x = self.initialX
        self.y = 1000 # Initial position 
        self.dy = 25 # Initial velocity 
        self.ddy = -0.8 # Acceleration 
        self.radius = 30
    
    def drawFruit(self):
        drawCircle(self.x, self.y, self.radius, fill = 'black')
   
    def fruitFlying(self):
        self.y -= self.dy 
        self.dy += 0.5 * self.ddy
        
    def updateX(self):
        if self.initialX <= 1500 // 2:
            self.x += 3
        if self.initialX > 1500 // 2:
            self.x -= 3

    def offScreen(self):
        if self.y >= 1500 - self.radius:
            return True
        else:
            return False

class Blade:
    def __init__(self):
        self.x = -100
        self.y = -100
    
    def drawCircle(self):
        drawCircle(self.x, self.y, 10, fill = 'gray')

class HalfFruit1(Fruit):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = 210
        self.dy = 0 # Initial velocity
    
    def drawSelf(self):
        drawArc(self.x - 10, self.y, self.radius*2, self.radius*2, 0, 180, 
                rotateAngle = self.angle)
    
    def halfFlying(self):
        self.y -= self.dy 
        self.dy += self.ddy
    
    def offScreen(self):
        if self.y >= 1500 - self.radius*2:
            return True
        else:
            return False

class HalfFruit2(Fruit):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = -330
        self.dy = 0 # Initial velocity
    
    def drawSelf(self):
        drawArc(self.x + 10, self.y, self.radius*2, self.radius*2, 0, 180, 
                rotateAngle = self.angle)
    
    def halfFlying(self):
        self.y -= self.dy
        self.dy += self.ddy
    
    def offScreen(self):
        if self.y >= 1500 - self.radius*2:
            return True
        else:
            return False

def onAppStart(app):
    app.width = 1500
    app.height = 1000
    app.rx = 200
    app.ry = 200
   
    app.homescreen = True
    app.classicRectX = 476
    app.classicRectY = 522
    app.zenRectX = 876
    app.zenRectY = 522

    # Keeps track of highest score
    app.classicHighScore = 0
   
    restart(app)

    # Title image
    app.titleURL = Image.open('title.png')
    app.titleWidth,app.titleHeight = app.titleURL.width,app.titleURL.height
    app.titleURL = CMUImage(app.titleURL)

def restart(app):
    app.score = 0
    app.lives = 3
    app.level = 1
    app.classic = False
    app.zen = False
    app.collision = False
    app.gameOver = False

    # Initialize list of all fruit objects 
    app.fruits = []
    app.lastFruitTime = time.time()

    # Initialize lists of half fruits 
    app.halfFruit1 = []
    app.halfFruit2 = []

    # Initialize Blade 
    app.blade = Blade()

def drawHomescreen(app):
    newTitleWidth, newTitleHeight = 800, 500
    drawImage(app.titleURL, app.width/2, 300, width = newTitleWidth,
              height= newTitleHeight, align = 'center')
    drawRect(app.classicRectX, app.classicRectY, 150, 60, fill = 'lightblue') # Classic button
    drawRect(app.zenRectX, app.zenRectY, 150, 60, fill = 'lightblue') # Zen button
    drawLabel("Classic", 550 , 550, size = 30, bold = True, fill="black")
    drawLabel("Zen", 950, 550, size = 30, bold = True, fill="black")

def drawClassicScreen(app):
    drawLabel(f'Score: {app.score}', 1400, 50, size = 30, bold = True, 
              align = "right")
    drawLabel(f'Lives: {app.lives}', 1400, 100, size = 30, bold = True, 
              align = 'right')
    drawRect(67, 20, 150, 60, fill = 'pink') # End game button
    drawLabel("End Game", 84, 50, size = 25, bold = True, align = "left")

def drawGameOverScreen(app):
    width = 400
    height = 500
    left = app.width//2 - width//2
    top = app.height//2 - height//2
    drawRect(0, 0, app.width, app.height, fill = 'lightblue')
    drawRect(left, top, width, height, fill = 'black')
    drawLabel("GAME OVER", app.width//2, top + 50, size = 40, 
              bold = True, fill = 'white')
    drawLabel(f'Your Score: {app.score}', app.width//2, top + 150, size = 25,
               fill = 'white')
    drawLabel(f'Your Highest Score: {app.classicHighScore}', app.width//2,
              top + 200, size = 25, fill = 'white')
    drawRect(584, 536, 300, 60, fill = 'green')
    drawLabel("Return to Home Screen", app.width//2, top + 400, size = 25,
              fill = 'white')


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
        app.blade.drawCircle()
        for fruit in app.fruits:
            fruit.drawFruit()
        for halfFruit1 in app.halfFruit1:
            halfFruit1.drawSelf()
        for halfFruit2 in app.halfFruit2:
            halfFruit2.drawSelf()

    elif app.zen:
        pass
    elif app.gameOver:
        drawGameOverScreen(app)

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
            app.homescreen = True
            app.classic = False
            restart(app)
    
    if app.gameOver:
        # If mouse intersects with the Return to Homescreen button:
        if (584 <= mouseX <= 884) and (536 <= mouseY <= 596):
            app.homescreen = True
            app.gameOver = False
            restart(app)

def onMouseMove(app, mouseX, mouseY):
    if app.classic:
        app.blade.x = mouseX
        app.blade.y = mouseY

def onStep(app):
    if digitCount(app.score) == 3:
        if app.score <= 500:
            app.level = 2
        elif 500 < app.score < 1000:
            app.level = 3
    elif digitCount(app.score) == 4:
        if app.score <= 1500:
            app.level = 4
        else:
            app.score = 5
    else:
        app.level = digitCount(app.score) - 1

    for fruit in app.fruits:
        if checkCollision(app, fruit):
            thisFruit = app.fruits.index(fruit)
            fruitx = fruit.x
            fruity = fruit.y
            app.fruits.pop(thisFruit)
            app.halfFruit1.append(HalfFruit1(fruitx, fruity))
            app.halfFruit2.append(HalfFruit2(fruitx, fruity))
            app.score += 10
            
    if app.classic and not app.gameOver:
        i = 0
        while i < len(app.fruits):
            fruit = app.fruits[i]
            fruit.fruitFlying()
            fruit.updateX()
            # Checks if fruit flies off screen, if it does loses 1 life 
            if fruit.offScreen():
                app.fruits.pop(i)
                if app.lives == 1:
                    app.lives -= 1
                    app.gameOver = True # Game over if lives = 0
                    app.classic = False
                    if app.score > app.classicHighScore:
                        app.classicHighScore = app.score

                else:
                    app.lives -= 1
            else:
                i += 1
            
        n = 0
        while n < len(app.halfFruit1):
            half1 = app.halfFruit1[n]
            half2 = app.halfFruit2[n]
            half1.halfFlying()
            half1.angle -= 10
            half1.x -= 3
            half2.halfFlying()
            half2.angle += 10
            half2.x += 3
            # Checks if half flies off screen, pop it
            if half1.offScreen() or half2.offScreen():
                app.halfFruit1.pop(n)
                app.halfFruit2.pop(n)
            else:
                n += 1

        # Code from lecture 
        if (time.time()-app.lastFruitTime > 1) and (len(app.fruits) < app.level):
            app.fruits.append(Fruit())
            app.lastFruitTime = time.time()
    
# Checks for collision between blade and passed in fruit object
def checkCollision(app, fruit):
    if distance(app.blade.x, app.blade.y, fruit.x, fruit.y) <= fruit.radius:
        return True

def digitCount(n):
    n = abs(n)
    if (n == 0):
        return 2
    return math.floor(math.log10(n)) + 1

def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5

def main():
    runApp()

main()
