import pygame
from pygame.locals import *

pygame.init()
fenetre = pygame.display.set_mode((650, 650))

app = 1
menu = "main"
menuhover = None
while app:
    if menu == "main":
        fenetre.blit(pygame.image.load("img/menu.png"), (0, 0))
        if menuhover == "play":
            fenetre.blit(pygame.image.load("img/play.png"), (218, 324))
        elif menuhover == "quit":
            fenetre.blit(pygame.image.load("img/quit.png"), (218, 431))
    elif menu == "game":
        pass
    pygame.display.flip()

    for evt in pygame.event.get():
        if evt.type == QUIT:
            app = 0
        elif evt.type == MOUSEMOTION:
            if menu == "main":
                menuhover = None
                if 218 <= evt.pos[0] <= 434 and 324 <= evt.pos[1] <= 430:
                    menuhover = "play"
                elif 218 <= evt.pos[0] <= 434 and 431 <= evt.pos[1] <= 541:
                    menuhover = "quit"
        elif evt.type == MOUSEBUTTONDOWN:
            if menu == "main":
                if 218 <= evt.pos[0] <= 434 and 324 <= evt.pos[1] <= 430:
                    menu = "game"
                elif 218 <= evt.pos[0] <= 434 and 431 <= evt.pos[1] <= 541:
                    app = 0
            elif menu == "game":
                pass


pygame.quit()
