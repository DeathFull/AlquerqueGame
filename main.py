import pygame
from pygame.locals import *

pygame.init()
fenetre = pygame.display.set_mode((650, 650))


class Pion(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.image = None
        if player == 2:
            self.image = pygame.transform.scale(pygame.image.load("img/noir.png"), (60, 60))
        else:
            self.image = pygame.transform.scale(pygame.image.load("img/blanc.png"), (60, 60))
        self.rect = self.image.get_rect()

    def updateRect(self, xy):
        self.rect = self.image.get_rect(center=xy)

    def updateImage(self):
        if self.player == 2:
            self.image = pygame.transform.scale(pygame.image.load("img/noir.png"), (60, 60))
        else:
            self.image = pygame.transform.scale(pygame.image.load("img/blanc.png"), (60, 60))

    def getPlayer(self):
        return self.player

    def setPlayer(self, player):
        self.player = player


tableau = [[Pion(2), Pion(2), Pion(2), Pion(2), Pion(2)],
           [Pion(2), Pion(2), Pion(2), Pion(2), Pion(2)],
           [Pion(2), Pion(2), Pion(0), Pion(1), Pion(1)],
           [Pion(1), Pion(1), Pion(1), Pion(1), Pion(1)],
           [Pion(1), Pion(1), Pion(1), Pion(1), Pion(1)]]


def drawGame():
    fenetre.fill((125, 125, 125))
    plateau_img = pygame.transform.scale(pygame.image.load("img/plateau.png"), (450, 450))
    plateau_rect = plateau_img.get_rect(center=(325, 325))
    fenetre.blit(plateau_img, plateau_rect)

    for i in range(len(tableau)):
        for k in range(len(tableau[i])):
            tableau[i][k].updateImage()
            tableau[i][k].updateRect((100 + (k * 112.5), 100 + (i * 112.5)))
            if tableau[i][k].image is not None and tableau[i][k].player != 0:
                fenetre.blit(tableau[i][k].image, tableau[i][k].rect)


def selectPion(event: pygame.event.Event):
    for i in range(len(tableau)):
        for j in range(len(tableau[i])):
            if tableau[i][j].rect.collidepoint(event.pos[0], event.pos[1]) is True:
                return i, j
    return None


def caseVoisins(pion: tuple):
    voisins = []
    if 0 <= pion[0] - 1 < len(tableau):
        voisins.append((pion[0] - 1, pion[1]))
    if 0 <= pion[0] + 1 < len(tableau):
        voisins.append((pion[0] + 1, pion[1]))
    if 0 <= pion[1] - 1 < len(tableau):
        voisins.append((pion[0], pion[1] - 1))
    if 0 <= pion[1] + 1 < len(tableau):
        voisins.append((pion[0], pion[1] + 1))
    if (pion[0] % 2 == 0 and pion[1] % 2 == 0) or (pion[0] % 2 != 0 and pion[1] % 2 != 0):
        if 0 <= pion[0] - 1 < len(tableau) and 0 <= pion[1] - 1 < len(tableau):
            voisins.append((pion[0] - 1, pion[1] - 1))
        if 0 <= pion[0] + 1 < len(tableau) and 0 <= pion[1] - 1 < len(tableau):
            voisins.append((pion[0] + 1, pion[1] - 1))
        if 0 <= pion[0] - 1 < len(tableau[pion[0]]) and 0 <= pion[1] + 1 < len(tableau):
            voisins.append((pion[0] - 1, pion[1] + 1))
        if 0 <= pion[0] + 1 < len(tableau[pion[0]]) and 0 <= pion[1] + 1 < len(tableau):
            voisins.append((pion[0] + 1, pion[1] + 1))
    return voisins


def caseVoisinsCanCapture(pion: tuple):
    voisins = []
    if 0 <= pion[0] - 2 < len(tableau):
        voisins.append((pion[0] - 2, pion[1]))
    if 0 <= pion[0] + 2 < len(tableau):
        voisins.append((pion[0] + 2, pion[1]))
    if 0 <= pion[1] - 2 < len(tableau):
        voisins.append((pion[0], pion[1] - 2))
    if 0 <= pion[1] + 2 < len(tableau):
        voisins.append((pion[0], pion[1] + 2))
    if (pion[0] % 2 == 0 and pion[1] % 2 == 0) or (pion[0] % 2 != 0 and pion[1] % 2 != 0):
        if 0 <= pion[0] - 2 < len(tableau) and 0 <= pion[1] - 2 < len(tableau):
            voisins.append((pion[0] - 2, pion[1] - 2))
        if 0 <= pion[0] + 2 < len(tableau) and 0 <= pion[1] - 2 < len(tableau):
            voisins.append((pion[0] + 2, pion[1] - 2))
        if 0 <= pion[0] - 2 < len(tableau[pion[0]]) and 0 <= pion[1] + 2 < len(tableau):
            voisins.append((pion[0] - 2, pion[1] + 2))
        if 0 <= pion[0] + 2 < len(tableau[pion[0]]) and 0 <= pion[1] + 2 < len(tableau):
            voisins.append((pion[0] + 2, pion[1] + 2))
    return voisins


def capturePion(pion1: tuple, pion2: tuple):
    for items in caseVoisins(pion1):
        if items in caseVoisins(pion2) and (
                tableau[items[0]][items[1]].getPlayer() != (game_player and 0)) and (
                (((pion1[0] + pion2[0]) / 2, (pion1[1] + pion2[1]) / 2) == items) or (
                pion1[0] == pion2[0] == items[0] or pion1[1] == pion2[1] == items[1])):
            return items
    return None


def verifCanCapturePion(pion1: tuple, pion2: tuple):
    for items in caseVoisins(pion1):
        if tableau[pion2[0]][pion2[1]].getPlayer() == 0 and items in caseVoisins(pion2) and (
                tableau[items[0]][items[1]].getPlayer() != game_player and tableau[items[0]][
            items[1]].getPlayer() != 0) and ((((pion1[0] + pion2[0]) / 2, (pion1[1] + pion2[1]) / 2) == items) or (
                pion1[0] == pion2[0] == items[0] or pion1[1] == pion2[1] == items[1])):
            return items
    return None


def canCapturePion():
    for i in range(len(tableau)):
        for j in range(len(tableau[i])):
            if tableau[i][j].getPlayer() == game_player:
                for item in caseVoisinsCanCapture((i, j)):
                    if verifCanCapturePion((i, j), item) is not None:
                        return True
    return False


def movePion(pion1: tuple, pion2: tuple):
    global game_player, menu
    if pion2 in caseVoisins(pion1) and tableau[pion2[0]][pion2[1]].getPlayer() == 0:
        if canCapturePion() is False:
            tableau[pion2[0]][pion2[1]].setPlayer(game_player)
        tableau[pion1[0]][pion1[1]].setPlayer(0)
        game_player = 1 if game_player == 2 else 2
        return True
    elif capturePion(pion1, pion2) is not None:
        pioncap = capturePion(pion1, pion2)
        tableau[pioncap[0]][pioncap[1]].setPlayer(0)
        tableau[pion1[0]][pion1[1]].setPlayer(0)
        tableau[pion2[0]][pion2[1]].setPlayer(game_player)
        if canCapturePion() is False:
            game_player = 1 if game_player == 2 else 2
        return True
    else:
        return False


def hasPionInPlateau(player: int):
    for i in range(len(tableau)):
        for j in range(len(tableau[i])):
            if tableau[i][j].player == player:
                return True


def canMove():
    for i in range(len(tableau)):
        for j in range(len(tableau[i])):
            if tableau[i][j].getPlayer() == game_player:
                for item in caseVoisins((i, j)):
                    if tableau[item[0]][item[1]].getPlayer() == 0:
                        return True
    return False


def isPossibleToPlay(player: int):
    if canMove() and hasPionInPlateau(player):
        return True
    return False


def resetGame():
    global game_player, game_case, second_game_case, tableau
    game_player = 1
    game_case = None
    second_game_case = None
    tableau = [[Pion(2), Pion(2), Pion(2), Pion(2), Pion(2)],
               [Pion(2), Pion(2), Pion(2), Pion(2), Pion(2)],
               [Pion(2), Pion(2), Pion(0), Pion(1), Pion(1)],
               [Pion(1), Pion(1), Pion(1), Pion(1), Pion(1)],
               [Pion(1), Pion(1), Pion(1), Pion(1), Pion(1)]]


app = 1
menu = "main"
menuhover = None
game_player = 1
game_case, second_game_case = None, None
while app:
    if menu == "main":
        fenetre.blit(pygame.image.load("img/menu.png"), (0, 0))
        if menuhover == "play":
            fenetre.blit(pygame.image.load("img/play.png"), (218, 324))
        elif menuhover == "quit":
            fenetre.blit(pygame.image.load("img/quit.png"), (218, 431))
    elif menu == "game":
        drawGame()
    elif menu == "end":
        fenetre.blit(pygame.image.load("img/end.png"), (0, 0))
        if menuhover == "replay":
            fenetre.blit(pygame.image.load("img/replay.png"), (105, 324))
    pygame.display.flip()

    for evt in pygame.event.get():
        if evt.type == QUIT:
            app = 0
        elif evt.type == KEYDOWN and evt.key == K_SPACE:
            print(game_player)
        elif evt.type == MOUSEMOTION:
            if menu == "main":
                menuhover = None
                if 218 <= evt.pos[0] <= 434 and 324 <= evt.pos[1] <= 430:
                    menuhover = "play"
                elif 218 <= evt.pos[0] <= 434 and 431 <= evt.pos[1] <= 541:
                    menuhover = "quit"
            if menu == "end":
                menuhover = None
                if 105 <= evt.pos[0] <= 541 and 324 <= evt.pos[1] <= 541:
                    menuhover = "replay"
        elif evt.type == MOUSEBUTTONDOWN:
            if menu == "main":
                if 218 <= evt.pos[0] <= 434 and 324 <= evt.pos[1] <= 430:
                    menu = "game"
                elif 218 <= evt.pos[0] <= 434 and 431 <= evt.pos[1] <= 541:
                    app = 0
            elif menu == "end":
                if 105 <= evt.pos[0] <= 541 and 324 <= evt.pos[1] <= 541:
                    menu = "game"
            elif menu == "game":
                click = selectPion(evt)
                if click is None:
                    break

                if game_case is None and tableau[click[0]][click[1]].getPlayer() == game_player:
                    game_case = click
                elif game_case is not None and second_game_case is None and \
                        tableau[click[0]][click[1]].getPlayer() == 0 and game_case is not click:
                    second_game_case = click
                if game_case is None or second_game_case is None:
                    break
                if movePion(game_case, second_game_case) is True:
                    game_case, second_game_case = None, None
                    if canCapturePion():
                        break

                if isPossibleToPlay(1) is False and isPossibleToPlay(2) is False:
                    resetGame()
                    menu = "end"
pygame.quit()
