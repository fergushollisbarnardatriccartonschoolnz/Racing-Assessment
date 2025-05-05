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
player_speed = 1
player_x = 0
player_y = screen_height*0.75
player_momentum = 0
drag = 0.1
player_x_size = 50
player_y_size = 50

lanes = 4
lanesep = 100
lanewidth = 10

entities = []#{"col":(255, 255, 255), "lane":0, "y":0, "xsc":20, "ysc":20}]

def drawbg(col:tuple, lanecol:tuple):
    screen.fill(col)
    pygame.draw.rect(screen, (123, 123, 123), (-wallpos-wallwidth+screen_width/2, 0, wallwidth, screen_height)) #left wall
    pygame.draw.rect(screen, (123, 123, 123), (wallpos+screen_width/2, 0, wallwidth, screen_height)) #right wall
    for i in range(lanes):
        lanepos = screen_width/2-(i*lanesep)-lanewidth/2+(lanes/2)*lanesep-lanesep/2
        pygame.draw.rect(screen, lanecol, (lanepos, 0, lanewidth, screen_height*0.8))
    pygame.draw.rect(screen, (0, 0, 0), (screen_width/2-5, screen_height/2-5, 10, 10)) #middle of screen

def entitytick():
    #draw entities
    for entity in entities:
        entity["y"] += math.log(score+100)
        ent_xpos = screen_width/2+(entity["lane"]*lanesep)-(lanes*lanesep)/2-entity["xsc"]/2
        pygame.draw.rect(screen, entity["col"], (ent_xpos, entity["y"], entity["xsc"], entity["ysc"]))
        if entity["y"] > screen_height:
            entities.pop(entities.index(entity))
        elif entity["y"] > player_y-player_y_size-entity["ysc"] and entity["y"] < player_y and ent_xpos > screen_width/2+player_x-player_x_size/2-entity["xsc"] and ent_xpos < screen_width/2+player_x+player_x_size/2:
            return "end_program"

    #generate entities
    for i in range(lanes):
        if random.randint(0, round(1+math.sqrt(len(entities)+1))*50) == 0:
            entities.append({"col":(255, 255, 255), "lane":random.randint(0, lanes), "y":-60, "xsc":60, "ysc":60})

mov = [0, 0]
keys_left = [pygame.K_a, pygame.K_LEFT]
keys_right = [pygame.K_d, pygame.K_RIGHT]
running_program = True
while running_program:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_program = False
        if event.type == pygame.KEYDOWN:
            if event.key in keys_left:
                mov[0] = player_speed
            if event.key in keys_right:
                mov[1] = player_speed
        if event.type == pygame.KEYUP:
            if event.key in keys_left:
                mov[0] = 0
            if event.key in keys_right:
                mov[1] = 0

    wallpos = (lanes/2)*lanesep+lanesep/2-lanewidth/2
    wallwidth = 100

    drawbg((143, 143, 143), (101, 101, 101))
    #(123, 123, 123)

    #basically playertick
    player_momentum += (-mov[0] + mov[1])
    player_x += player_momentum
    if player_x > wallpos-player_x_size/2:
        player_momentum = -abs(player_momentum)
        player_x += player_momentum
    elif player_x < -wallpos+player_x_size/2:
        player_momentum = abs(player_momentum)
        player_x += player_momentum
    if player_momentum < drag and player_momentum > -drag:
        player_momentum = 0
    if player_momentum > drag:
        player_momentum -= drag
        player_momentum *= 1-drag
    if player_momentum < -drag:
        player_momentum += drag
        player_momentum *= 1-drag
    pygame.draw.rect(screen, (255, 200, 255), (screen_width/2+player_x-player_x_size/2, player_y-player_y_size, player_x_size, player_y_size))

    if entitytick() == "end_program":
        clock.tick(0.3)
        running_program = False

    pygame.display.update()
    clock.tick(60)
    ticks += 1