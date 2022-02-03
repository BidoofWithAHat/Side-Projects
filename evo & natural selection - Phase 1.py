import pygame
import random
import math
 
pygame.init()

spriteSize = 1
rowsCount = 100
columnsCount = 100

drawSurfaceWidth = spriteSize*columnsCount
drawSurfaceHeight = spriteSize*rowsCount
windowDimensions = (1000, 1000)
window = pygame.display.set_mode(windowDimensions)
drawSurface = pygame.surface.Surface((drawSurfaceWidth, drawSurfaceHeight))

generation = 1
turn = 1
creaturesCount = 100

spritesGroup = pygame.sprite.Group()
creaturesGroup = pygame.sprite.Group()

class Creature(pygame.sprite.Sprite):
    def __init__(self, posIn, spriteIn, neuralNetworkIn, colorIn, *args, **flags):
        pygame.sprite.Sprite.__init__(self)
        self.flags = flags
        self.args = args
        self.image = pygame.Surface((spriteSize, spriteSize))
        self.rect = self.image.get_rect()
        self.pos = posIn
        self.rect.x = self.pos[0]*spriteSize
        self.rect.y = self.pos[1]*spriteSize
        self.color = colorIn
        self.sprite = spriteIn
        if spriteIn == "Square":
            self.image.fill(self.color)
        
    def move(self, **directions):
        xPlus = directions.get("x")
        yPlus = directions.get("y")
        if type(xPlus) != int:
            xPlus = 0
        if type(yPlus) != int:
            yPlus = 0
        xNew = self.rect.x+xPlus
        yNew = self.rect.y+yPlus
        if (xNew in range(0, drawSurfaceWidth)) and (yNew in range(0, drawSurfaceHeight)) and ((xNew, yNew) not in occupiedSpaces()):
            self.setPos(xNew, yNew)
    
    def setPos(self, xIn, yIn):
        self.rect.x = xIn
        self.rect.y = yIn
        
    def update(self):
        pygame.sprite.Sprite.update(self)
        if self.flags['movement'] == "random":
            self.move(x=random.randrange(-1, 2), y=random.randrange(-1, 2))
        
def addCreature(quantity, posIn):
    creature = Creature(posIn, "Square", '', (70, 180, 90), 50, 30, movement="random")
    creaturesGroup.add(creature)
    spritesGroup.add(creature)
    
def summonByCreaturesCount():
    for i in range(creaturesCount):
        posIn = (random.randrange(0, columnsCount), random.randrange(0, rowsCount))
        searching = True
        while searching:
            if (posIn[0], posIn[1]) in occupiedSpaces():
                if posIn[0]+2 > columnsCount:
                    if posIn[1]+2 > rowsCount:
                        posIn = (0, 0)
                    else:
                        posIn = (0, posIn[1]+1)
                else:
                    posIn = (posIn[0]+1, posIn[1])
            else:
                addCreature(1, posIn)
                searching = False
        
def occupiedSpaces():
    occupiedSpacesList = []
    for creature in creaturesGroup.sprites():
        occupiedSpacesList.append((creature.rect.x, creature.rect.y))
    return occupiedSpacesList

def newGeneration():
    generation += 1
        
def main():
    
    clock = pygame.time.Clock()
    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: 
                running = False
            if ev.type == pygame.KEYDOWN:  
                if ev.key == pygame.K_w:
                    addCreature(1, (random.randrange(0, columnsCount), random.randrange(0, rowsCount)))
                if ev.key == pygame.K_d:
                    summonByCreaturesCount()
                if ev.key == pygame.K_s:
                    print(len(set(occupiedSpaces())))
                if ev.key == pygame.K_f:
                    outsideSpacesList = []
                    for creature in creaturesGroup.sprites():
                        if (creature.rect.x > columnsCount-1) or (creature.rect.x < 0) or (creature.rect.y > rowsCount-1) or (creature.rect.y < 0):
                            print(f'({creature.rect.x}, {creature.rect.y})')
                            outsideSpacesList.append((creature.rect.x, creature.rect.y))
                    print(outsideSpacesList)
                    print(len(outsideSpacesList))
                if ev.key == pygame.K_UP:
                    creaturesGroup.sprites()[0].move(y=-1)
                if ev.key == pygame.K_LEFT:
                    creaturesGroup.sprites()[0].move(x=-1)
                if ev.key == pygame.K_RIGHT:
                    creaturesGroup.sprites()[0].move(x=1)
                if ev.key == pygame.K_DOWN:
                    creaturesGroup.sprites()[0].move(y=1)
        
        creaturesGroup.update()
                
        drawSurface.fill((255, 255, 255))
        spritesGroup.draw(drawSurface)
        window.blit(pygame.transform.scale(drawSurface, window.get_rect().size), (0, 0))
        pygame.display.flip()
        
        clock.tick(50) 
    pygame.quit()    

main()