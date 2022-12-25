import pygame
from pygame.locals import *

pygame.init()
fenetre = pygame.display.set_mode((650, 650))
pygame.display.set_caption("Alquerque")


class App:
    def __init__(self, plateau):
        self.app = 1
        self.menu = "main"
        self.menuhover = None
        self.plateau: Plateau = plateau

    def getStatus(self):
        return self.app

    def setStatus(self, status):
        self.app = status

    def getMenu(self):
        return self.menu

    def setMenu(self, menu):
        self.menu = menu

    def getMenuHover(self):
        return self.menuhover

    def setMenuHover(self, mhover):
        self.menuhover = mhover

    def getPlateau(self):
        return self.plateau


class Plateau:
    def __init__(self):
        self.tableau = [[Pion(2), Pion(2), Pion(2), Pion(2), Pion(2)],
                        [Pion(2), Pion(2), Pion(2), Pion(2), Pion(2)],
                        [Pion(2), Pion(2), Pion(0), Pion(1), Pion(1)],
                        [Pion(1), Pion(1), Pion(1), Pion(1), Pion(1)],
                        [Pion(1), Pion(1), Pion(1), Pion(1), Pion(1)]]
        self.player = 1
        self.game_case, self.second_game_case = None, None

    def getGameCase(self):
        return self.game_case

    def setGameCase(self, gamecase):
        self.game_case = gamecase

    def getSecondGameCase(self):
        return self.second_game_case

    def setSecondGameCase(self, sgamecase):
        self.second_game_case = sgamecase

    def getTableau(self):
        return self.tableau

    def setTableau(self, tab):
        self.tableau = tab

    def getCurrentPlayer(self):
        return self.player

    def switchPlayer(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

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

    def listNeighbours(self, pion: tuple):
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

    def listCaptureTargets(self, pion: tuple):
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
        for items in self.listNeighbours(pion1):
            if items in self.listNeighbours(pion2) and (
                    self.tableau[items[0]][items[1]].getPlayer() != (self.player and 0)) and (
                    (((pion1[0] + pion2[0]) / 2, (pion1[1] + pion2[1]) / 2) == items) or (
                    pion1[0] == pion2[0] == items[0] or pion1[1] == pion2[1] == items[1])):
                return items
        return None

    def isActualCapture(self, pion1: tuple, pion2: tuple):
        for items in self.listNeighbours(pion1):
            if self.tableau[pion2[0]][pion2[1]].getPlayer() == 0 and items in self.listNeighbours(pion2) and (
                    self.tableau[items[0]][items[1]].getPlayer() != self.player and self.tableau[items[0]][
                items[1]].getPlayer() != 0) and ((((pion1[0] + pion2[0]) / 2, (pion1[1] + pion2[1]) / 2) == items) or (
                    pion1[0] == pion2[0] == items[0] or pion1[1] == pion2[1] == items[1])):
                return items
        return None

    def canCapturePion(self):
        for i in range(len(self.tableau)):
            for j in range(len(self.tableau[i])):
                if self.tableau[i][j].getPlayer() == self.player:
                    for item in self.listCaptureTargets((i, j)):
                        if self.isActualCapture((i, j), item) is not None:
                            return True
        return False

    def canMove(self):
        for i in range(len(self.tableau)):
            for j in range(len(self.tableau[i])):
                if self.tableau[i][j].getPlayer() == self.player:
                    for item in self.listNeighbours((i, j)):
                        if self.tableau[item[0]][item[1]].getPlayer() == 0:
                            return True
        return False

    def movePion(self, pion1: tuple, pion2: tuple):
        if pion2 in self.listNeighbours(pion1) and self.tableau[pion2[0]][pion2[1]].getPlayer() == 0:
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
            print(self.canCapturePion())
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
        self.setTableau([[Pion(2), Pion(2), Pion(2), Pion(2), Pion(2)],
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


app = App(Plateau())

while app.getStatus():
    if app.getMenu() == "main":
        fenetre.blit(pygame.image.load("img/menu.png"), (0, 0))
        if app.getMenuHover() == "play":
            fenetre.blit(pygame.image.load("img/play.png"), (218, 324))
        elif app.getMenuHover() == "quit":
            fenetre.blit(pygame.image.load("img/quit.png"), (218, 431))
    elif app.getMenu() == "game":
        app.getPlateau().drawGame(fenetre)
    elif app.getMenu() == "end":
        fenetre.blit(pygame.image.load("img/end.png"), (0, 0))
        if app.getMenuHover() == "replay":
            fenetre.blit(pygame.image.load("img/replay.png"), (105, 324))
    pygame.display.flip()

    for evt in pygame.event.get():
        if evt.type == QUIT:
            app = 0
        elif evt.type == MOUSEMOTION:
            if app.getMenu() == "main":
                app.setMenuHover(None)
                if 218 <= evt.pos[0] <= 434 and 324 <= evt.pos[1] <= 430:
                    app.setMenuHover("play")
                elif 218 <= evt.pos[0] <= 434 and 431 <= evt.pos[1] <= 541:
                    app.setMenuHover("quit")
            if app.getMenu() == "end":
                app.setMenuHover(None)
                if 105 <= evt.pos[0] <= 541 and 324 <= evt.pos[1] <= 541:
                    app.setMenuHover("replay")
        elif evt.type == MOUSEBUTTONDOWN:
            if app.getMenu() == "main":
                if 218 <= evt.pos[0] <= 434 and 324 <= evt.pos[1] <= 430:
                    app.setMenu("game")
                elif 218 <= evt.pos[0] <= 434 and 431 <= evt.pos[1] <= 541:
                    app = 0
            elif app.getMenu() == "end":
                if 105 <= evt.pos[0] <= 541 and 324 <= evt.pos[1] <= 541:
                    app.setMenu("game")
            elif app.getMenu() == "game":
                click = app.getPlateau().selectPion(evt)
                if click is None:
                    break

                if app.getPlateau().getGameCase() is None and app.getPlateau().getTableau()[click[0]][
                    click[1]].getPlayer() == app.getPlateau().getCurrentPlayer():
                    print("first")
                    app.getPlateau().setGameCase(click)
                elif app.getPlateau().getGameCase() is not None and app.getPlateau().getSecondGameCase() is None and \
                        app.getPlateau().getTableau()[click[0]][
                            click[1]].getPlayer() == 0 and app.getPlateau().getGameCase() is not click:
                    print("second")
                    app.getPlateau().setSecondGameCase(click)
                if app.getPlateau().getGameCase() is None or app.getPlateau().getSecondGameCase() is None:
                    break
                if app.getPlateau().movePion(app.getPlateau().getGameCase(),
                                             app.getPlateau().getSecondGameCase()) is True:
                    print(app.getPlateau().getCurrentPlayer())
                    app.getPlateau().setGameCase(None)
                    app.getPlateau().setSecondGameCase(None)
                    if app.getPlateau().canCapturePion():
                        break
                else:
                    app.getPlateau().setGameCase(None)
                    app.getPlateau().setSecondGameCase(None)

                if app.getPlateau().isPossibleToPlay(1) is False and app.getPlateau().isPossibleToPlay(2) is False:
                    game_case, second_game_case = app.getPlateau().resetPlateau(app.getPlateau().getGameCase(),
                                                                                app.getPlateau().getSecondGameCase())
                    app.getPlateau().setGameCase(game_case)
                    app.getPlateau().setSecondGameCase(second_game_case)
                    menu = "end"
pygame.quit()
