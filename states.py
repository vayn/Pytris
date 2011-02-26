#!/usr/bin/env python
# vim:fileencoding=utf-8
# @Author: Vayn a.k.a. VT <vayn@vayn.de>
# @Name: states.py
# @Date: 2011年02月26日 星期六 15时56分14秒

import sys
import os
import pygame
import time
import random
from pygame.locals import *
from tetrominoes import *

__metaclass__ = type

def loadData(filename, filetype):
    path = os.path.split(os.path.abspath(__file__))[0]
    return os.path.join(path, 'asset', filetype, filename)

pygame.font.init()

FONT = loadData('04b03.ttf', 'font')
BASICFONT = pygame.font.Font(FONT, 24)

class State:
    def handle(self, event):
        if event.type == QUIT:
            self.terminate()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.terminate()

    def firstDisplay(self, screen):
        screen.fill(DARKGRAY)
        pygame.display.flip()

    def display(self, screen):
        pass

    def terminate(self):
        pygame.quit()
        sys.exit()

class Play(State):
    """
    This is where the main part of the game.
    """
    lastMoveDownTime     = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime         = time.time()

    movingDown  = False
    movingLeft  = False
    movingRight = False

    def __init__(self, score=0):
        self.board = self.getNewBoard()
        self.score = score
        self.level = self.calculateLevel(self.score)
        self.fallFreq = self.calculateFallFreq(self.level)
        self.curPiece = self.getNewPiece()
        self.nextPiece = self.getNewPiece()
        self.playMusic()

    def handle(self, event):
        State.handle(self, event)
        if self.curPiece is None: return
        if event.type == KEYUP:
            if event.key == K_p:
                # pausing the game
                pause = Paused()
                pause.firstDisplay(self.screen, text='Paused')
                Play.lastFallTime = time.time()
                Play.lastMoveDownTime = time.time()
                Play.lastMoveSidewaysTime = time.time()
                while True:
                    event = pygame.event.wait()
                    if event is not None and event.type == KEYDOWN:
                        if event.key != K_p:
                            break

            if event.key == K_LEFT or event.key == K_a or event.key == K_h:
                Play.movingLeft = False
            if event.key == K_RIGHT or event.key == K_d or event.key == K_l:
                Play.movingRight = False
            if event.key == K_DOWN or event.key == K_s or event.key == K_j:
                Play.movingDown = False

        elif event.type == KEYDOWN:
            # moving the block sideways
            if (event.key == K_LEFT or event.key == K_a or event.key == K_h) and \
               self.isValidPosition(self.board, self.curPiece, adjX=-1):
                self.curPiece['x'] -= 1
                Play.movingLeft = True
                Play.movingRight = False
                Play.lastMoveSidewaysTime = time.time()
            if (event.key == K_RIGHT or event.key == K_d or event.key == K_l) and \
               self.isValidPosition(self.board, self.curPiece, adjX=1):
                self.curPiece['x'] += 1
                Play.movingRight = True
                Play.movingLeft = False
                Play.lastMoveSidewaysTime = time.time()

            # rotate the block (if allowed), then check if its new position is a
            # valid one, and if not, then rotate it back.
            if event.key == K_UP or event.key == K_w or event.key == K_k:
                self.curPiece['rotation'] = (self.curPiece['rotation'] + 1) % \
                        len(SHAPES[self.curPiece['shape']])
                if not self.isValidPosition(self.board, self.curPiece):
                    self.curPiece['rotation'] = (self.curPiece['rotation'] - 1) % \
                            len(SHAPES[self.curPiece['shape']])
            if event.key == K_q or event.key == K_i:
                self.curPiece['rotation'] = (self.curPiece['rotation'] - 1) % \
                        len(SHAPES[self.curPiece['shape']])
                if not self.isValidPosition(self.board, self.curPiece):
                    self.curPiece['rotation'] = (self.curPiece['rotation'] + 1) % \
                            len(SHAPES['shape'])

            # making the block fall faster
            if event.key == K_DOWN or event.key == K_s or event.key == K_j:
                Play.movingDown = True
                if self.isValidPosition(self.board, self.curPiece, adjY=1):
                    self.curPiece['y'] += 1
                Play.lastMoveDownTime = time.time()
            if event.key == K_SPACE:
                # move the current block all the way down
                Play.movingDown = False
                Play.movingLeft = False
                Play.movingRight = False
                #for i in range(1, BOARDHEIGHT):
                while self.curPiece['y'] < BOARDHEIGHT:
                    # Floating
                    #if not self.isValidPosition(self.board, self.curPiece, adjY=i):
                    #    break
                    #self.curPiece['y'] += (i-1)
                    if not self.isValidPosition(self.board, self.curPiece, adjY=1):
                        break
                    self.curPiece['y'] += 1

    def firstDisplay(self, screen):
        self.screen = screen
        screen.fill(BGCOLOR)
        self.drawBoard(self.board)
        self.drawStatus(self.score, self.level)
        self.drawNextPiece(self.nextPiece)
        self.drawPiece(self.curPiece)
        pygame.display.update()

    def update(self, game):
        if self.curPiece is not None:
            if (Play.movingLeft or Play.movingRight) and \
               (time.time() - Play.lastMoveSidewaysTime > MOVESIDEWAYSFREQ):
                if Play.movingLeft and self.isValidPosition(self.board, self.curPiece, adjX=-1):
                    self.curPiece['x'] -= 1
                if Play.movingRight and self.isValidPosition(self.board, self.curPiece, adjX=1):
                    self.curPiece['x'] += 1
                Play.lastMoveSidewaysTime = time.time()

            if Play.movingDown and time.time() - Play.lastMoveDownTime > MOVEDOWNFREQ and \
               self.isValidPosition(self.board, self.curPiece, adjY=1):
                self.curPiece['y'] += 1
                Play.lastMoveDownTime = time.time()

            # let the piece fall down if it is time to
            if time.time() - Play.lastFallTime > self.fallFreq:
                # see if the piece hit the bottom
                if self.hasHitBottom(self.board, self.curPiece):
                    self.addToBoard(self.board, self.curPiece)
                    self.score += self.deleteCompleteLines(self.board)
                    self.level = self.calculateLevel(self.score)
                    self.fallFreq = self.calculateFallFreq(self.level)
                    self.curPiece = None
                    Play.lastFallTime = time.time()
                else:
                    # just move the block down
                    self.curPiece['y'] += 1
                    Play.lastFallTime = time.time()
        else:
            self.curPiece = self.nextPiece
            self.nextPiece = self.getNewPiece()
            Play.lastFallTime = time.time()
            if not self.isValidPosition(self.board, self.curPiece):
                self.stopMusic()
                game.nextState = GameOver()

    def display(self, screen):
        screen.fill(BGCOLOR)
        self.drawBoard(self.board)
        self.drawStatus(self.score, self.level)
        self.drawNextPiece(self.nextPiece)
        if self.curPiece is not None:
            self.drawPiece(self.curPiece)
        pygame.display.update()

    def calculateLevel(self, score):
        return int(score / 10) + 1

    def calculateFallFreq(self, level):
        return 0.27 - (level * 0.02)

    def getNewBoard(self):
        board = []
        for i in range(BOARDWIDTH):
            board.append([BLANK] * BOARDHEIGHT)
        return board

    def getNewPiece(self):
        # return a random new piece in a random rotation and color
        shape = random.choice(list(SHAPES.keys()))
        newPiece = {'shape': shape,
                    'rotation': random.randint(0, len(SHAPES[shape]) - 1),
                    'x': int(BOARDWIDTH / 2) - 2,
                    'y': -2,
                    'color': random.randint(0, len(COLORS) - 1)}
        return newPiece

    def addToBoard(self, board, piece):
        # fill in the spots on the board based on piece's location, shape,
        # and rotation
        for x in range(5):
            for y in range(5):
                if SHAPES[piece['shape']][piece['rotation']][x][y] != BLANK:
                    board[x + piece['x']][y + piece['y']] = piece['color']

    def hasHitBottom(self, board, piece):
        # Returns True if the piece's bottom is currently on top of something
        for x in range(5):
            for y in range(5):
                if SHAPES[piece['shape']][piece['rotation']][x][y] == BLANK or \
                   y + piece['y'] + 1 < 0:
                    continue
                if y + piece['y'] + 1 == BOARDHEIGHT:
                    return True
                if board[x + piece['x']][y + piece['y'] + 1] != BLANK:
                    return True
        return False

    def isOnBoard(self, x, y):
        # Returns True if the x,y coordinates point to a block space that on
        # the board, and returns False if they are outside of the board.
        return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT

    def isValidPosition(self, board, piece, adjX=0, adjY=0):
        # Return True if the piece is within the board and not colliding
        # with any blocks on the board.
        for x in range(5):
            for y in range(5):
                if y + piece['y'] + adjY < 0 or \
                   SHAPES[piece['shape']][piece['rotation']][x][y] == BLANK:
                    continue
                if not self.isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                    return False
                if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                    return False
        return True

    def isCompleteLine(self, board, y):
        # Return True if the yth line from the top is filled with blocks
        # with no gaps.
        for x in range(BOARDWIDTH):
            if board[x][y] == BLANK:
                return False
        return True

    def deleteCompleteLines(self, board):
        # Remove any completed lines on the board, move everything above
        # them down, and return the number of complete lines.
        linesDeleted = 0
        y = BOARDHEIGHT - 1
        while y >= 0:
            if self.isCompleteLine(board, y):
                # Remove the line and pull everything above it down by one line.
                # I also call this mechanism "naive gravity".
                linesDeleted += 1
                for pullDownY in range(y, 0, -1):
                    for x in range(BOARDWIDTH):
                        board[x][pullDownY] = board[x][pullDownY - 1]
                # Set very top line to blank.
                for x in range(BOARDWIDTH):
                    board[x][0] = BLANK
            else:
                y -= 1
        return linesDeleted

    def convertToPixelCoords(self, x, y):
        # Convert the given x,y coordinates of the board to x,y coordinates of
        # the location on the screen.
        return (XMARGIN + (x * BLOCKSIZE)), ((BOARDTOP + (y * BLOCKSIZE)))

    def drawBoardBorder(self):
        # draw the border around the board
        pygame.draw.rect(self.screen, BORDERCOLOR, (XMARGIN - 3, BOARDTOP - 7, (BOARDWIDTH * BLOCKSIZE) + 8, (BOARDHEIGHT * BLOCKSIZE) + 8), 3)

    def drawBoard(self, board):
        self.drawBoardBorder()
        # fill the background of the board
        pygame.draw.rect(self.screen, BGCOLOR, (XMARGIN, BOARDTOP, BLOCKSIZE * BOARDWIDTH, BLOCKSIZE * BOARDHEIGHT))
        # draw the individual blocks on the board
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                if board[x][y] != BLANK:
                    pixelx, pixely = self.convertToPixelCoords(x, y)
                    pygame.draw.rect(self.screen, COLORS[board[x][y]], (pixelx+1, pixely+1, BLOCKSIZE-1, BLOCKSIZE-1))

    def drawStatus(self, score, level):
        # draw the level text
        levelSurf = BASICFONT.render('Level: %s' % level, True, WHITE)
        levelRect = levelSurf.get_rect()
        levelRect.topleft = (WINDOWWIDTH - 150, 20)
        self.screen.blit(levelSurf, levelRect)

        # draw the score text
        scoreSurf = BASICFONT.render('Score: %s' % score, True, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 150, 50)
        self.screen.blit(scoreSurf, scoreRect)

    def drawNextPiece(self, piece):
        # draw the "next" piece
        nextSurf = BASICFONT.render('Next:', True, WHITE)
        nextRect = nextSurf.get_rect()
        nextRect.topleft = (WINDOWWIDTH - 150, 80)
        self.screen.blit(nextSurf, nextRect)

        self.drawPiece(piece, customCoords=(WINDOWWIDTH - 170, 105))

    def drawPiece(self, piece, customCoords=(None, None)):
        shapeToDraw = SHAPES[piece['shape']][piece['rotation']]
        if customCoords == (None, None):
            pixelx, pixely = self.convertToPixelCoords(piece['x'], piece['y'])
        else:
            pixelx, pixely = customCoords

        # draw each of the blocks that make up the piece
        for x in range(5):
            for y in range(5):
                if shapeToDraw[x][y] != BLANK:
                    pygame.draw.rect(self.screen,
                                     COLORS[piece['color']],
                                    (pixelx + (x * BLOCKSIZE) + 1,
                                     pixely + (y * BLOCKSIZE) + 1,
                                     BLOCKSIZE-1, BLOCKSIZE-1)
                                    )

    def playMusic(self):
        if random.randint(0, 1) == 0:
            song = loadData('tetris.mid', 'music')
        else:
            song = loadData('funky_stars.mp3', 'music')
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(-1, 0.0)

    def stopMusic(self):
        pygame.mixer.music.stop()

class Paused(State):
    finished = 0

    def handle(self, event):
        State.handle(self, event)
        if event.type in [MOUSEBUTTONDOWN, KEYDOWN]:
            self.finished = 1

    def update(self, game):
        if self.finished:
            game.nextState = self.nextState()

    def firstDisplay(self, screen, text):
        screen.fill(BLACK)
        self.showTextScreen(screen, text, font="04b03.ttf")
        pygame.display.update()

    def showTextScreen(self, screen, text, font):
        antialiase = True
        titleFont = pygame.font.Font(loadData(font, 'font'), 100)

        # title shadow
        titleSurf = titleFont.render(text, antialiase, DARKGRAY)
        titleRect = titleSurf.get_rect(center=(int(WINDOWWIDTH / 2) + 3, int(WINDOWHEIGHT / 2 - 47)))
        screen.blit(titleSurf, titleRect)

        # title
        titleSurf = titleFont.render(text, antialiase, WHITE)
        titleRect = titleSurf.get_rect(center=(int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2 - 50)))
        screen.blit(titleSurf, titleRect)

        # presskey info
        pressKeySurf = BASICFONT.render('Press any key to start', antialiase, WHITE)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 50)
        screen.blit(pressKeySurf, pressKeyRect)

        # author info
        authorFont = pygame.font.Font(FONT, 18)
        authorSurf = authorFont.render("A Vayn production 2011", antialiase, WHITE)
        authorRect = authorSurf.get_rect()
        authorRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 170)
        screen.blit(authorSurf, authorRect)

class StartUp(Paused):
    nextState = Play

    def firstDisplay(self, screen):
        screen.fill(BLACK)
        text="PyTetris"
        self.showTextScreen(screen, text, font="marblerun.ttf")
        pygame.display.update()

class GameOver(Paused):
    nextState = Play

    def __init__(self):
        self.text = "Game Over"

    def firstDisplay(self, screen):
        self.showTextScreen(screen, self.text, font="04b03.ttf")
        pygame.display.update()

