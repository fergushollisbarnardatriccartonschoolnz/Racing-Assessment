import pygame
import time
import random
import math
pygame.init()

devmode = True
devsettings = {"showhitboxes":True, "showsprites":True}

screen_width = 640
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
game_icon = pygame.image.load("game_icon.png")
pygame.display.set_icon(game_icon)
pygame.display.set_caption("racing")
car_lightred = None
car_red = pygame.image.load("car_red.png")
car_darkred = None
car_lightorange = None
car_orange = pygame.image.load("car_orange.png")
car_lightyellow = None
car_yellow = None
car_brown = None
car_olive = None
car_lightgreen = None
car_green = pygame.image.load("car_green.png")
car_darkgreen = None
car_cyan = pygame.image.load("car_cyan.png")
car_lightblue = None
car_blue = pygame.image.load("car_blue.png")
car_darkblue = None
car_lightpurple = None
car_purple = pygame.image.load("car_purple.png")
car_darkpurple = None
car_light = None
car_pink = None
car_darkpink = None
car_white = None
car_lightgray = None
car_gray = None
car_darkgray = None
car_black = None
clock = pygame.time.Clock()

ticks = 0
score = 0
difficulty = 1
ticks_ingame = 0
player_speed = 1
player_x = 0
player_y = screen_height*0.75
player_momentum = 0
drag = 0.1
player_x_size = 43
player_y_size = 86

lanes = 4
lanesep = 100
lanewidth = 10

entities = []#{"col":(255, 255, 255), "lane":0, "y":0, "xsc":20, "ysc":20}]

                #lanenumber, time remaining until lane can be generated in again
recent_generations = {"0":0}

def q():
    pygame.quit()
    quit()

def drawbg(col:tuple, lanecol:tuple|None, wallcol:tuple|None):
    screen.fill(col)
    if wallcol:
        pygame.draw.rect(screen, wallcol, (-wallpos-wallwidth+screen_width/2, 0, wallwidth, screen_height)) #left wall
        pygame.draw.rect(screen, wallcol, (wallpos+screen_width/2, 0, wallwidth, screen_height)) #right wall
    if lanecol:
        for i in range(lanes):
            lanepos = screen_width/2-(i*lanesep)-lanewidth/2+(lanes/2)*lanesep-lanesep/2
            pygame.draw.rect(screen, lanecol, (lanepos, 0, lanewidth, screen_height))
    if not inmenu and devmode:
        pygame.draw.rect(screen, (0, 0, 0), (screen_width/2-5, screen_height/2-5, 10, 10)) #middle of screen

def entitytick():
    temp = False

    #draw entities
    score_to_add = 0
    for entity in entities:
        entity["y"] += difficulty
        ent_xpos = screen_width/2+(entity["lane"]*lanesep)-(lanes*lanesep)/2-entity["xsc"]/2
        if not devmode or (devmode and devsettings["showsprites"]):
            #pygame.draw.rect(screen, entity["col"], (ent_xpos, entity["y"], entity["xsc"], entity["ysc"]))
            screen.blit(pygame.transform.scale(pygame.transform.flip(car_red, False, True), (entity["xsc"], entity["ysc"])), ((ent_xpos, entity["y"]), (entity["xsc"], entity["ysc"])))
        if devmode and devsettings["showhitboxes"]:
            pygame.draw.rect(screen, (255, 0, 0), (ent_xpos, entity["y"], 2, entity["ysc"]))
            pygame.draw.rect(screen, (255, 0, 0), (ent_xpos, entity["y"], entity["xsc"], 2))
            pygame.draw.rect(screen, (255, 0, 0), (ent_xpos+entity["xsc"]-2, entity["y"], 2, entity["ysc"]))
            pygame.draw.rect(screen, (255, 0, 0), (ent_xpos, entity["y"]+entity["ysc"]-2, entity["xsc"], 2))
        if entity["y"] > screen_height:
            entities.pop(entities.index(entity))
            score_to_add += 1
        elif entity["y"] > player_y-player_y_size-entity["ysc"] and entity["y"] < player_y and ent_xpos > screen_width/2+player_x-player_x_size/2-entity["xsc"] and ent_xpos < screen_width/2+player_x+player_x_size/2:
            temp = True

    #generate entities
    for i in range(lanes):
        rand_value = random.randint(0, round(((1+math.sqrt(len(entities)+1))*50)/math.log(score+10)))
        if rand_value == 0 and str(i) not in recent_generations:
            entities.append({"col":(255, 255, 255), "lane":random.randint(0, lanes), "y":-120, "xsc":60, "ysc":120})
            recent_generations[str(i)] = math.ceil(120/difficulty)
        if str(i) in recent_generations:
            recent_generations[str(i)] -= 1
            if recent_generations[str(i)] <= 0:
                recent_generations.pop(str(i))

    if temp:
        return "ded"
    return score_to_add

def message(msg:str, txt_colour:tuple, bkgd_colour:tuple|None, pos:tuple, f:str, fontsize:int|float):
    font = pygame.font.Font(f, fontsize)
    txt = font.render(msg, True, txt_colour, bkgd_colour)
    text_box = txt.get_rect(center = pos)
    screen.blit(txt, text_box)

inmenu = True
mov = [0, 0]
keys_left = [pygame.K_a, pygame.K_LEFT]
keys_right = [pygame.K_d, pygame.K_RIGHT]
while 1==1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            q()
        if event.type == pygame.KEYDOWN:
            if event.key in keys_left:
                mov[0] = player_speed
            if event.key in keys_right:
                mov[1] = player_speed
            if event.key == pygame.K_SPACE:
                if inmenu:
                    inmenu = False
                else:
                    inmenu = True
        if event.type == pygame.KEYUP:
            if event.key in keys_left:
                mov[0] = 0
            if event.key in keys_right:
                mov[1] = 0

    if not inmenu:
        wallpos = (lanes/2)*lanesep+lanesep/2-lanewidth/2
        wallwidth = 100

        drawbg((143, 143, 143), (101, 101, 101), (123, 123, 123))
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
        if not devmode or (devmode and devsettings["showsprites"]):
            screen.blit(pygame.transform.scale(car_red, (player_x_size, player_y_size)), ((screen_width/2+player_x-player_x_size/2, player_y-player_y_size), (player_x_size, player_y_size)))
            #pygame.draw.rect(screen, (255, 200, 255), (screen_width/2+player_x-player_x_size/2, player_y-player_y_size, player_x_size, player_y_size))
        if devmode and devsettings["showhitboxes"]:
            pygame.draw.rect(screen, (0, 0, 255), (screen_width/2+player_x-player_x_size/2, player_y-player_y_size, 2, player_y_size))
            pygame.draw.rect(screen, (0, 0, 255), (screen_width/2+player_x-player_x_size/2, player_y-player_y_size, player_x_size, 2))
            pygame.draw.rect(screen, (0, 0, 255), (screen_width/2+player_x+player_x_size/2-2, player_y-player_y_size, 2, player_y_size))
            pygame.draw.rect(screen, (0, 0, 255), (screen_width/2+player_x-player_x_size/2, player_y-2, player_x_size, 2))

        entity_output = entitytick()
        if entity_output == "ded":
            message("game over ):", (0, 0, 0), None, (screen_width/2, screen_height/2), "freesansbold.ttf", 28)
            message(f"Score: {score}", (0, 0, 0), None, (screen_width/2, 50), "freesansbold.ttf", 20)
            message("(space to restart)", (0, 0, 0), None, (screen_width/2, screen_height/2+50), "freesansbold.ttf", 18)
            pygame.display.update()
            while 1==1:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        q()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            inmenu = True
                if inmenu:
                    ticks = 0
                    ticks_ingame = 0
                    score = 0
                    player_x = 0
                    mov = [0, 0]
                    entities = []
                    lanes = 4
                    lanesep = 100
                    lanewidth = 10
                    break

        if not inmenu:
            score += entity_output
            ticks_ingame += 1
            message(f"Score: {score}", (0, 0, 0), None, (screen_width/2, 50), "freesansbold.ttf", 20)

    else:
        drawbg((54, 54, 54), None, None)
        message("racing.assess", (255, 255, 255), None, (screen_width/2, 147), "freesansbold.ttf", 60)
        if ticks_ingame <= 0:
            message("Press space to play", (255, 255, 255), None, (screen_width/2, 212), "freesansbold.ttf", 28)
        else:
            message("Paused, press space to unpause", (255, 255, 255), None, (screen_width/2, 212), "freesansbold.ttf", 28)

    pygame.display.update()
    clock.tick(60)
    ticks += 1
    difficulty = math.log(score+50)/1.69897