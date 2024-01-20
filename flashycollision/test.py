import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((400, 400), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.SCALED)
font = pygame.font.SysFont("timesnewroman", 14)
text = font.render("text", False, (255, 255, 255), (0,0,0))
rect = text.get_rect(topleft = (100, 100))

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(text, rect)


    pygame.display.update()

