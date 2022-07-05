import random
import sys
import pygame as pg
from pygame.locals import *

# makes it so you can stretch and squash display i think
fps = 15
window_width = 480
window_height = 480
cellsize = 20

assert window_height % cellsize == 0, "Window width must be a multiple of cell size."
assert window_width % cellsize == 0, "Window height must be a multiple of cell size."
cellwidth = int(window_width / cellsize)
cellheight = int(window_height / cellsize)

#colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
darkgreen = (0, 155, 0)
darkgray = (40, 40, 40)
bgcolor = darkgreen

#d..ire...ctions?
up = 'up'
down = 'down'
left = 'left'
right = 'right'

head = 0  # candygrammar


def main():
    global fpsclock, displaysurf, basicfont

    pg.init()
    fpsclock = pg.time.Clock()
    displaysurf = pg.display.set_mode((window_width, window_height))
    basicfont = pg.font.Font('freesansbold.ttf', 18)
    pg.display.set_caption('SNAKE!!!!!!')

    showStartScreen()
    while True:
        rungame()
        showGameOverScreen()


def rungame():
    #says to set a random start point
    startx = random.randint(5, cellwidth - 6)
    starty = random.randint(5, cellheight - 6)
    snekCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = right

    apple = getRandomLocation()

    while True:  # game loop
        for event in pg.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if(event.key == K_LEFT or event.key == K_a) and direction != right:
                    direction = left
                elif(event.key == K_RIGHT or event.key == K_d) and direction != left:
                    direction = right
                elif(event.key == K_UP or event.key == K_w) and direction != down:
                    direction = up
                elif(event.key == K_DOWN or event.key == K_s) and direction != up:
                    direction = down
                elif event.key == K_ESCAPE:
                    terminate()

        #check if worm hits itself or an edge
        if snekCoords[head]['x'] == -1 or snekCoords[head]['x'] == cellwidth or snekCoords[head]['y'] == cellheight or snekCoords[head]['y'] == -1:
            return  # game over
        for snekBody in snekCoords[1:]:
            if snekBody['x'] == snekCoords[head]['x'] and snekBody['y'] == snekCoords[head]['y']:
                return  # also game over

        # check if worm has eaten apple
        if snekCoords[head]['x'] == apple['x'] and snekCoords[head]['y'] == apple['y']:
            # don't remove tail seg
            apple = getRandomLocation()  # set new apple
        else:
            del snekCoords[-1]  # remove worm tail segment

        # add segment in the direction that worm 'moves'
        if direction == up:
            newHead = {'x':snekCoords[head]['x'], 'y':snekCoords[head]['y'] - 1}
        elif direction == down:
            newHead = {'x': snekCoords[head]['x'], 'y': snekCoords[head]['y'] + 1}
        elif direction == left:
            newHead = {'x': snekCoords[head]['x'] - 1, 'y': snekCoords[head]['y']}
        elif direction == right:
            newHead = {'x': snekCoords[head]['x'] + 1, 'y': snekCoords[head]['y']}
        snekCoords.insert(0, newHead)
        displaysurf.fill(bgcolor)
        drawGrid()
        drawSnake(snekCoords)
        drawApple(apple)
        drawScore(len(snekCoords) - 3)
        pg.display.update()
        fpsclock.tick(fps)


def drawPressKeyMsg():
    pressKeySurf = basicfont.render('Press a key to play.', True, darkgray)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (window_width - 200, window_height - 30)
    displaysurf.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pg.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pg.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pg.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Snake!!', True, white, darkgreen)
    titleSurf2 = titleFont.render('Snake!!', True, green)

    degrees1 = 0
    degrees2 = 0
    while True:
        displaysurf.fill(bgcolor)
        rotatedSurf1 = pg.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (window_width/2, window_height/2)
        displaysurf.blit(rotatedSurf1, rotatedRect1)
        rotatedSurf2 = pg.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (window_width / 2, window_height / 2)
        displaysurf.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pg.event.get()  # clear event queue
            return
        pg.display.update()
        fpsclock.tick(fps)
        degrees1 += 3  # rotate by 3 deg each frame
        degrees2 += 7  # rotate by 7 deg each frame


def terminate():
    pg.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, cellwidth - 1), 'y': random.randint(0, cellheight - 1)}


def showGameOverScreen():
    gameOverFont = pg.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, white)
    overSurf = gameOverFont.render('Over', True, white)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (window_width/2, 10)
    overRect.midtop = (window_width / 2, gameRect.height + 10 + 25)

    displaysurf.blit(gameSurf, gameRect)
    displaysurf.blit(overSurf, overRect)
    drawPressKeyMsg()
    pg.display.update()
    pg.time.wait(500)
    checkForKeyPress()  # clear key presses in queue


    while True:
        if checkForKeyPress():
            pg.event.get()  # clear event queue
            return


def drawScore(score):
    scoresurf = basicfont.render('Score: %s' % (score), True, white)
    scoreRect = scoresurf.get_rect()
    scoreRect.topleft = (window_width - 120, 10)
    displaysurf.blit(scoresurf, scoreRect)


def drawSnake(snekCoords):
    for coord in snekCoords:
        x = coord['x'] * cellsize
        y = coord['y'] * cellsize
        snekSegRect = pg.Rect(x, y, cellsize, cellsize)
        pg.draw.rect(displaysurf, darkgreen, snekSegRect)
        snekInnerSegRect = pg.Rect(x + 4, y + 4, cellsize - 8, cellsize -8)
        pg.draw.rect(displaysurf, green, snekInnerSegRect)


def drawApple(coord):
    x = coord['x'] * cellsize
    y = coord['y'] * cellsize
    appleRect = pg.Rect(x, y, cellsize, cellsize)
    pg.draw.rect(displaysurf, red, appleRect)


def drawGrid():
    for x in range(0, window_width, cellsize):  # draw vert lines
        pg.draw.line(displaysurf, darkgray, (x, 0), (x, window_height))
    for y in range(0, window_height, cellsize):  # draw hoz lines
        pg.draw.line(displaysurf, darkgray, (0, y), (window_width, y))


if __name__ == '__main__':
    main()
