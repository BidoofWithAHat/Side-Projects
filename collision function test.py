import pygame
import random
import math

pygame.init()

spriteSize = 1
rowsCount = 30
columnsCount = 30

rect = (17, 14, 8, 8)
otherRect = (12, 8, 8, 8)

drawSurfaceWidth = spriteSize*columnsCount
drawSurfaceHeight = spriteSize*rowsCount
windowDimensions = (1000, 1000) #size of "window display"
window = pygame.display.set_mode(windowDimensions)
drawSurface = pygame.surface.Surface((drawSurfaceWidth, drawSurfaceHeight)) #main surface #will be stretched to fit the "window display"

def main():
        
    clock = pygame.time.Clock()
    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: 
                running = False
        if (rect[0] < otherRect[0]+otherRect[2] and otherRect[0] < rect[0]+20 and
        rect[1] < otherRect[1]+otherRect[3] and otherRect[1] < rect[1]+20):
            print("true")
            
        drawSurface.fill((255, 255, 255))
        pygame.draw.rect(drawSurface, (255, 0, 0), rect)
        pygame.draw.rect(drawSurface, (0, 255, 0), otherRect)
        window.blit(pygame.transform.scale(drawSurface, window.get_rect().size), (0, 0))
        pygame.display.flip()
        
        clock.tick(50) 
    pygame.quit()    

main()