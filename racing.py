import pygame
import time
import random
import math

screen_width = 640
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
game_icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("racing")
clock = pygame.time.Clock()

ticks = 0
score = 0
player_speed = 0
player_x = 0
player_momentum = 0
drag = 0.1

lanes = 4
lanesep = 100
lanewidth = 10

entities = []

def drawbg(col:tuple, lanecol:tuple):
    wallpos = (lanes/2)*lanesep+lanesep/2+lanewidth/2
    print(wallpos)
    wallwidth = 100
    screen.fill(col)
    pygame.draw.rect(screen, (123, 123, 123), (-wallpos-wallwidth+screen_width/2, 0, wallwidth, screen_height)) #left wall
    pygame.draw.rect(screen, (123, 123, 123), (wallpos+screen_width/2, 0, wallwidth, screen_height)) #right wall
    for i in range(lanes):
        lanepos = screen_width/2-(i*lanesep)-lanewidth/2+(lanes/2)*lanesep-lanesep/2 #definitley overley complicated but I can't be bothered to fix it (rn atleast)
        pygame.draw.rect(screen, lanecol, (lanepos-player_x, 0, lanewidth, screen_height*0.8))
    pygame.draw.rect(screen, (0, 0, 0), (screen_width/2-5, screen_height/2-5, 10, 10)) #middle of screen

def entitytick():
    #draw entities
    for entity in entities:
        entity["y"] -= 1
        pygame.draw.rect(screen, entity["col"], (entity["x"], entity["y"], entity["xsc"], entity["ysc"]))

running_program = True
while running_program:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_program = False

    drawbg((143, 143, 143), (101, 101, 101))
    #(123, 123, 123)

    entitytick()

    pygame.display.update()
    clock.tick(60)
    ticks += 1