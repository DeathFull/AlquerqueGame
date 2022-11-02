import pygame
from pygame.locals import *

pygame.init()
fenetre = pygame.display.set_mode((650, 650))
pygame.display.set_caption("Alquerque")


class App:
    def __init__(self):
        self.brice = False


class Plateau:
    def __init__(self):
        self.tableau = []
        self.player = 1

    def getTableau(self):
        return self.tableau

    def setTableau(self, tab):
        self.tableau = tab

    def getCurrentPlayer(self):
        return self.player

    def switchPlayer(self):
        self.player = 2 if self.player == 1 else 2

    def drawGame(self, fen):
        fen.fill((125, 125, 125))
        plateau_img = pygame.transform.scale(pygame.image.load("img/plateau.png"), (450, 450))
        plateau_rect = plateau_img.get_rect(center=(325, 325))
        fen.blit(plateau_img, plateau_rect)

        for i in range(len(self.tableau)):
            for k in range(len(self.tableau[i])):
                self.tableau[i][k].updateImage()
                self.tableau[i][k].updateRect((100 + (k * 112.5), 100 + (i * 112.5)))
                if self.tableau[i][k].image is not None and self.tableau[i][k].player != 0:
                    fen.blit(self.tableau[i][k].image, self.tableau[i][k].rect)

    def selectPion(self, event: pygame.event.Event):
        for i in range(len(self.tableau)):
            for j in range(len(self.tableau[i])):
                if self.tableau[i][j].rect.collidepoint(event.pos[0], event.pos[1]) is True:
                    return i, j
        return None

    def hasPionInPlateau(self, player):
        for i in range(len(self.tableau)):
            for j in range(len(self.tableau[i])):
                if self.tableau[i][j].player == player:
                    return True

    def caseVoisins(self, pion: tuple):
        voisins = []
        if 0 <= pion[0] - 1 < len(self.tableau):
            voisins.append((pion[0] - 1, pion[1]))
        if 0 <= pion[0] + 1 < len(self.tableau):
            voisins.append((pion[0] + 1, pion[1]))
        if 0 <= pion[1] - 1 < len(self.tableau):
            voisins.append((pion[0], pion[1] - 1))
        if 0 <= pion[1] + 1 < len(self.tableau):
            voisins.append((pion[0], pion[1] + 1))
        if (pion[0] % 2 == 0 and pion[1] % 2 == 0) or (pion[0] % 2 != 0 and pion[1] % 2 != 0):
            if 0 <= pion[0] - 1 < len(self.tableau) and 0 <= pion[1] - 1 < len(self.tableau):
                voisins.append((pion[0] - 1, pion[1] - 1))
            if 0 <= pion[0] + 1 < len(self.tableau) and 0 <= pion[1] - 1 < len(self.tableau):
                voisins.append((pion[0] + 1, pion[1] - 1))
            if 0 <= pion[0] - 1 < len(self.tableau[pion[0]]) and 0 <= pion[1] + 1 < len(self.tableau):
                voisins.append((pion[0] - 1, pion[1] + 1))
            if 0 <= pion[0] + 1 < len(self.tableau[pion[0]]) and 0 <= pion[1] + 1 < len(self.tableau):
                voisins.append((pion[0] + 1, pion[1] + 1))
        return voisins

    def caseVoisinsCanCapture(self, pion: tuple):
        voisins = []
        if 0 <= pion[0] - 2 < len(self.tableau):
            voisins.append((pion[0] - 2, pion[1]))
        if 0 <= pion[0] + 2 < len(self.tableau):
            voisins.append((pion[0] + 2, pion[1]))
        if 0 <= pion[1] - 2 < len(self.tableau):
            voisins.append((pion[0], pion[1] - 2))
        if 0 <= pion[1] + 2 < len(self.tableau):
            voisins.append((pion[0], pion[1] + 2))
        if (pion[0] % 2 == 0 and pion[1] % 2 == 0) or (pion[0] % 2 != 0 and pion[1] % 2 != 0):
            if 0 <= pion[0] - 2 < len(self.tableau) and 0 <= pion[1] - 2 < len(self.tableau):
                voisins.append((pion[0] - 2, pion[1] - 2))
            if 0 <= pion[0] + 2 < len(self.tableau) and 0 <= pion[1] - 2 < len(self.tableau):
                voisins.append((pion[0] + 2, pion[1] - 2))
            if 0 <= pion[0] - 2 < len(self.tableau[pion[0]]) and 0 <= pion[1] + 2 < len(self.tableau):
                voisins.append((pion[0] - 2, pion[1] + 2))
            if 0 <= pion[0] + 2 < len(self.tableau[pion[0]]) and 0 <= pion[1] + 2 < len(self.tableau):
                voisins.append((pion[0] + 2, pion[1] + 2))
        return voisins

    def capturePion(self, pion1: tuple, pion2: tuple):
        for items in self.caseVoisins(pion1):
            if items in self.caseVoisins(pion2) and (
                    self.tableau[items[0]][items[1]].getPlayer() != (self.player and 0)) and (
                    (((pion1[0] + pion2[0]) / 2, (pion1[1] + pion2[1]) / 2) == items) or (
                    pion1[0] == pion2[0] == items[0] or pion1[1] == pion2[1] == items[1])):
                return items
        return None

    def verifCanCapturePion(self, pion1: tuple, pion2: tuple):
        for items in self.caseVoisins(pion1):
            if self.tableau[pion2[0]][pion2[1]].getPlayer() == 0 and items in self.caseVoisins(pion2) and (
                    self.tableau[items[0]][items[1]].getPlayer() != self.player and self.tableau[items[0]][
                items[1]].getPlayer() != 0) and ((((pion1[0] + pion2[0]) / 2, (pion1[1] + pion2[1]) / 2) == items) or (
                    pion1[0] == pion2[0] == items[0] or pion1[1] == pion2[1] == items[1])):
                return items
        return None

    def canCapturePion(self):
        for i in range(len(self.tableau)):
            for j in range(len(self.tableau[i])):
                if self.tableau[i][j].getPlayer() == self.player:
                    for item in self.caseVoisinsCanCapture((i, j)):
                        if self.verifCanCapturePion((i, j), item) is not None:
                            return True
        return False

    def canMove(self):
        for i in range(len(self.tableau)):
            for j in range(len(self.tableau[i])):
                if self.tableau[i][j].getPlayer() == self.player:
                    for item in self.caseVoisins((i, j)):
                        if self.tableau[item[0]][item[1]].getPlayer() == 0:
                            return True
        return False

    def movePion(self, pion1: tuple, pion2: tuple):
        if pion2 in self.caseVoisins(pion1) and self.tableau[pion2[0]][pion2[1]].getPlayer() == 0:
            if self.canCapturePion() is False:
                self.tableau[pion2[0]][pion2[1]].setPlayer(self.player)
            self.tableau[pion1[0]][pion1[1]].setPlayer(0)
            self.switchPlayer()
            return True
        elif self.capturePion(pion1, pion2) is not None:
            pioncap = self.capturePion(pion1, pion2)
            self.tableau[pioncap[0]][pioncap[1]].setPlayer(0)
            self.tableau[pion1[0]][pion1[1]].setPlayer(0)
            self.tableau[pion2[0]][pion2[1]].setPlayer(self.player)
            if self.canCapturePion() is False:
                self.switchPlayer()
            return True
        else:
            return False

    def isPossibleToPlay(self, player: int):
        if self.canMove() and self.hasPionInPlateau(player):
            return True
        return False

    def resetPlateau(self, case, secondcase):
        self.player = 1
        case = None
        secondcase = None
        tab.setTableau([[Pion(2), Pion(2), Pion(2), Pion(2), Pion(2)],
                        [Pion(2), Pion(2), Pion(2), Pion(2), Pion(2)],
                        [Pion(2), Pion(2), Pion(0), Pion(1), Pion(1)],
                        [Pion(1), Pion(1), Pion(1), Pion(1), Pion(1)],
                        [Pion(1), Pion(1), Pion(1), Pion(1), Pion(1)]])
        return case, secondcase


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


tab = Plateau()

tab.setTableau([[Pion(2), Pion(2), Pion(2), Pion(2), Pion(2)],
                [Pion(2), Pion(2), Pion(2), Pion(2), Pion(2)],
                [Pion(2), Pion(2), Pion(0), Pion(1), Pion(1)],
                [Pion(1), Pion(1), Pion(1), Pion(1), Pion(1)],
                [Pion(1), Pion(1), Pion(1), Pion(1), Pion(1)]])




app = 1
menu = "main"
menuhover = None
game_case, second_game_case = None, None
while app:
    if menu == "main":
        fenetre.blit(pygame.image.load("img/menu.png"), (0, 0))
        if menuhover == "play":
            fenetre.blit(pygame.image.load("img/play.png"), (218, 324))
        elif menuhover == "quit":
            fenetre.blit(pygame.image.load("img/quit.png"), (218, 431))
    elif menu == "game":
        tab.drawGame(fenetre)
    elif menu == "end":
        fenetre.blit(pygame.image.load("img/end.png"), (0, 0))
        if menuhover == "replay":
            fenetre.blit(pygame.image.load("img/replay.png"), (105, 324))
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
                click = tab.selectPion(evt)
                if click is None:
                    break

                if game_case is None and tab.getTableau()[click[0]][click[1]].getPlayer() == tab.getCurrentPlayer():
                    game_case = click
                elif game_case is not None and second_game_case is None and \
                        tab.getTableau()[click[0]][click[1]].getPlayer() == 0 and game_case is not click:
                    second_game_case = click
                if game_case is None or second_game_case is None:
                    break
                if tab.movePion(game_case, second_game_case) is True:
                    game_case, second_game_case = None, None
                    if tab.canCapturePion():
                        break

                if tab.isPossibleToPlay(1) is False and tab.isPossibleToPlay(2) is False:
                    game_case, second_game_case = tab.resetPlateau(game_case, second_game_case)
                    menu = "end"
pygame.quit()
