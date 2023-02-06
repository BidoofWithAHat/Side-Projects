import pygame
import random
import math
import numpy as np

pygame.init()

GAME_EVENT = pygame.event.custom_type()

""" SETTING DISPLAY SURFACES """
spriteSize = 1 #pixel(s) squared per square
rowsCount = 40 #Height of game grid
columnsCount = 40 #Width of game grid
drawSurfaceWidth = spriteSize*columnsCount #Stretch of game grid (horizontally)
drawSurfaceHeight = spriteSize*rowsCount   #                     (vertically)
drawSurface = pygame.surface.Surface((drawSurfaceWidth, drawSurfaceHeight)) #The surface where all active game objects are painted onto

windowDimensions = (950, 950) #Actual size of display
window = pygame.display.set_mode(windowDimensions) #The surface where "drawSurface" is scaled to the size of this surface then painted onto

""" SETTING VARIABLES """
poss = [] #List of all positions on the game board
for x in range(columnsCount):
    for y in range(rowsCount):
        poss.append((x, y))

snakeOccupiedPoss = [] #Will contain occupied positions of all snake segments, ordered from head to tail
fruitCount = 1 #Number of fruits on the game surface at any given time ##NUMBERS > 1 ARE NOT FULLY SUPPORTED YET (missing occupied spaces of all fruits) (lvl - easy)
growthRate = 1 #Number of segments the snake will grow after consuming a fruit ##NUMBER > 1 ARE NOT SUPPORTED YET
snakeStartPos = (columnsCount//2, rowsCount//2)
fruits = []
lastKeyPressed = "NONE"
pause = False

""" SETTING CLASSES """
class SnakeHead():
    def __init__(self, lengthIn, colourIn, posIn, moveSpeedIn, *argsIn, **flagsIn):
        #self.flags = flagsIn
        #self.args = argsIn
        self.length = lengthIn
        self.colour = colourIn
        self.pos = posIn
        self.image = pygame.Surface((spriteSize, spriteSize))
        pygame.draw.rect(self.image, self.colour, self.image.get_rect())
        self.moveSpeed = moveSpeedIn
        self.nextMoveTime = pygame.time.get_ticks() + self.moveSpeed
        self.lastDirection = "NONE"
        
    def move(self): #Every update cycle, snake will move the direction of the latest inputted direction
        if pygame.time.get_ticks() >= self.nextMoveTime:
            self.nextMoveTime += self.moveSpeed
            if lastKeyPressed == "Up":
                self.pos[1] += -1
                self.lastDirection = "Up"
            if lastKeyPressed == "Right":
                self.pos[0] += 1
                self.lastDirection = "Right"
            if lastKeyPressed == "Down":
                self.pos[1] += 1
                self.lastDirection = "Down"
            if lastKeyPressed == "Left":
                self.pos[0] += -1
                self.lastDirection = "Left"
            if lastKeyPressed != "NONE":
                snakeOccupiedPoss.insert(0, tuple(self.pos))
                
    def grow(self):
        if columnsCount*rowsCount > self.length:
            self.length += 1
    
    def checkCollision(self):
        if pygame.Rect.colliderect(pygame.Rect(*self.pos, spriteSize, spriteSize), drawSurface.get_rect()) != True: #If snake head is not inside game board, 
            pygame.event.post(pygame.event.Event(GAME_EVENT, active="GAMEOVER")) #trigger event "GAMEOVER"
        if tuple(self.pos) in snakeOccupiedPoss[1:len(snakeOccupiedPoss)]: #If snake head is in the position another segment is in, 
            pygame.event.post(pygame.event.Event(GAME_EVENT, active="GAMEOVER")) #trigger event "GAMEOVER"
        
class Fruit():
    def __init__(self, colourIn, posIn):
        self.colour = colourIn
        self.pos = posIn
        self.image = pygame.Surface((spriteSize, spriteSize))
        pygame.draw.rect(self.image, self.colour, self.image.get_rect())
    
    def collideCheck(self, snakePos):
        if (self.pos[0] == snakePos[0]) and (self.pos[1] == snakePos[1]): #If snake head is in this fruit's position,
            return True
        
def addFruit(): #Add a fruit with given [COLOR (R/G/B), POSITION (in array form)], the position being a random pick from all available positions
    fruits.append(Fruit((255, 0, 0), np.array(random.choice(list(set(poss) - set(snakeOccupiedPoss))))))
    
def reverseBool(boolIn):
    if boolIn:
        return False
    else:
        return True
    
""" INITIALIZE GAME """
def main():
    
    global lastKeyPressed
    global fruits
    global snakeOccupiedPoss
    global pause
    
    clock = pygame.time.Clock() #Setting up clock
    running = True
    
    snake = SnakeHead(1, (0, 255, 0), np.array([*snakeStartPos]), 70) #Create snake (player) with given [LENGTH, COLOR (R/G/B), STARTING POSITION (in array form), MOVESPEED (=ticks until next movement)]
    snakeOccupiedPoss = [snakeStartPos]
    fruits = []
    for i in range(fruitCount): #Create fruit(s)
        addFruit()
    
    """ GAME START """
    while running:
        
        """ UPDATE """
        if not pause:
            snake.move()
            
            snake.checkCollision()
            
            endLoop = len(fruits)
            i = 0
            fruitEaten = 0 #Number of fruits eaten this cycle (just in case somehow more than 1 is eaten)
            while (i < endLoop):
                if fruits[i].collideCheck(snake.pos): #If {statement} is True,
                    pygame.event.post(pygame.event.Event(GAME_EVENT, active="FRUITCOLLECTED")) #trigger event "FRUITCOLLECTED"
                    fruitEaten += 1
                    fruits.remove(fruits[i]) #delete fruit[i]
                endLoop -= 1
            if (fruitEaten == 0) and (lastKeyPressed != "NONE") and (len(snakeOccupiedPoss) > snake.length): #This code may seem weird
                snakeOccupiedPoss.pop(-1) #Forget the oldest recorded snake position / Get rid of the last segment of the snake
        
            for i in range(fruitEaten):
                addFruit()
            
        """ EVENTS """
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: 
                pygame.quit()
            if ev.type == pygame.KEYDOWN:
                if (ev.key == pygame.K_SPACE or ev.key == pygame.K_p):
                    pause = reverseBool(pause)
                if not pause:
                    if (ev.key == pygame.K_UP or ev.key == pygame.K_w) and (snake.lastDirection != "Down"):
                        lastKeyPressed = "Up"
                    if (ev.key == pygame.K_RIGHT or ev.key == pygame.K_d) and (snake.lastDirection != "Left"):
                        lastKeyPressed = "Right"
                    if (ev.key == pygame.K_DOWN or ev.key == pygame.K_s) and (snake.lastDirection != "Up"):
                        lastKeyPressed = "Down"
                    if (ev.key == pygame.K_LEFT or ev.key == pygame.K_a) and (snake.lastDirection != "Right"):
                        lastKeyPressed = "Left"
            if ev.type == GAME_EVENT:
                if ev.active == "FRUITCOLLECTED":
                    snake.grow()
                    print("Length:", snake.length)
                if ev.active == "GAMEOVER":
                    running = False
                    print("Game Over")
        
        """ RENDER """
        drawSurface.fill((0, 0, 0)) #Fill background with color
        for sprite in fruits:
            drawSurface.blit(sprite.image, sprite.pos)
        for i in range(len(snakeOccupiedPoss)):
            drawSurface.blit(snake.image, snakeOccupiedPoss[i])
        window.blit(pygame.transform.scale(drawSurface, window.get_rect().size), (0, 0)) #Scale the game surface to, then print onto, the window display
        pygame.display.flip()
        
        clock.tick(100) #I believe this is how many ticks per second
        
while True:
    main()