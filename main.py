import numpy as np
import pygame
import time
import math
import sys

numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

mouseState = 0
objDimensions = (0, 0)
encoding = ""
offset = [0,0]

if len(sys.argv) == 2:
    with open(sys.argv[1], "r") as f:
        for line in f:
            if line[0] != '#':
                if '=' in line:
                    items = line.split(',')
                    objDimensions = (int(items[0].split()[-1]), int(items[1].split()[-1]))
                    print(objDimensions)
                else:
                    encoding += str(line.split('\n')[0])

pygame.init()
board = np.zeros((100, 100), dtype=bool)
screen = pygame.display.set_mode((900, 900))


def initialiseBoard(set, rle, size, initial):
    x0, y0 = initial
    xs, ys = size
    object = np.zeros((ys, xs), dtype=bool)
    states = []
    row = 0
    counter = ""
    for cmd in rle:
        if cmd in numbers:
            counter += cmd
        else:
            if cmd == 'b':
                states += [False for i in range(int(counter if counter != "" else '1'))]
            if cmd == 'o':
                states += [True for i in range(int(counter if counter != "" else '1'))]
            if cmd == '$' or cmd == '!':
                object[row, :len(states)] = states
                states = []
                row += int(counter if counter != "" else '1')
            counter = ""
    set[y0:y0 + ys, x0:x0 + xs] += object
    return set


def draw(set):
    for x in range(100):
        for y in range(100):
            if set[y + offset[1], x + offset[0]]:
                pygame.draw.rect(screen, (0, 0, 0), ((x * 10), (y * 10), 10, 10))
            else:
                pygame.draw.rect(screen, (255, 255, 255), ((x * 10), (y * 10), 10, 10))
    pygame.display.flip()


def CoordToGrid(coord):
    x, y = coord
    x = math.floor(x / 10)
    y = math.floor(y / 10)
    return (x, y)


def SafeIndex(set, coord):
    x, y = coord
    if x < 0 or x >= 100 or y < 0 or y >= 100:
        return False
    else:
        return set[y, x]


def update(set):
    clone = set.copy()
    for x in range(100):
        for y in range(100):
            surrounds = [SafeIndex(set, i) for i in
                         [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1),
                          (x, y + 1), (x + 1, y + 1)]]
            alive = sum(surrounds)
            if set[y, x]:
                if alive < 2 or alive > 3:
                    clone[y, x] = False
            else:
                if alive == 3:
                    clone[y, x] = True
    return clone


running = False

board = initialiseBoard(board, encoding, objDimensions, (35,35))

draw(board)

while True:
    start = time.time()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseState = 1
            if event.button == 3:
                mouseState = 2
            
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseState = 0
        elif event.type == pygame.KEYDOWN:
            print(event.key)
            if event.key == pygame.K_p:
                running = not running
            if event.key == pygame.K_q:
                pygame.quit()
                break

    if mouseState != 0:
        x, y = CoordToGrid(pygame.mouse.get_pos())
        if mouseState == 1:
            board[y, x] = True
        elif mouseState == 2:
            board[y, x] = False

    draw(board)
    if running:
        board = update(board)
    end = time.time()
    #print(start - end)


