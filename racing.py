import pygame
import time
import random
import math
pygame.init()

devmode = False
devsettings = {"showhitboxes":True, "showsprites":True}

screen_width = 640
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
game_icon = pygame.image.load("game_icon.png")
pygame.display.set_icon(game_icon)
pygame.display.set_caption("racing")
car_lightred = pygame.image.load("car_lightred.png")
car_red = pygame.image.load("car_red.png")
car_darkred = pygame.image.load("car_darkred.png")
car_lightorange = pygame.image.load("car_lightorange.png")
car_orange = pygame.image.load("car_orange.png")
car_lightyellow = pygame.image.load("car_lightyellow.png")
car_yellow = pygame.image.load("car_yellow.png")
car_brown = pygame.image.load("car_brown.png")
car_olive = pygame.image.load("car_olive.png")
car_lightgreen = pygame.image.load("car_lightgreen.png")
car_green = pygame.image.load("car_green.png")
car_darkgreen = pygame.image.load("car_darkgreen.png")
car_cyan = pygame.image.load("car_cyan.png")
car_lightblue = pygame.image.load("car_lightblue.png")
car_blue = pygame.image.load("car_blue.png")
car_darkblue = pygame.image.load("car_darkblue.png")
car_lightpurple = pygame.image.load("car_lightpurple.png")
car_purple = pygame.image.load("car_purple.png")
car_darkpurple = pygame.image.load("car_darkpurple.png")
car_lightpink = pygame.image.load("car_lightpink.png")
car_pink = pygame.image.load("car_pink.png")
car_darkpink = pygame.image.load("car_darkpink.png")
car_white = pygame.image.load("car_white.png")
car_lightgray = pygame.image.load("car_lightgray.png")
car_gray = pygame.image.load("car_gray.png")
car_darkgray = pygame.image.load("car_darkgray.png")
car_black = pygame.image.load("car_black.png")
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

current_biome = "null"
biomes = {
    "null":{"drag":0.1, "playerspd":1, "screenx":640, "screeny":640, "lanes":4, "lanesep":100, "lanewidth":10, "bgcol":(143, 143, 143), "lanecol":(101, 101, 101), "wallcol":(123, 123, 123), "carcols":(car_black, car_darkgray, car_gray, car_lightgray, car_white), "carsize":(60, 120)},
    "frost":{"drag":0.05, "playerspd":0.7815, "screenx":740, "screeny":640, "lanes":5, "lanesep":100, "lanewidth":10, "bgcol":(140, 140, 200), "lanecol":(100, 100, 160), "wallcol":(120, 120, 180), "carcols":(car_darkblue, car_blue, car_lightblue, car_cyan, car_white, car_lightgray), "carsize":(60, 120)},
    "volcanic":{"drag":0.175, "playerspd":1.135, "screenx":900, "screeny":720, "lanes":6, "lanesep":110, "lanewidth":12, "bgcol":(200, 140, 140), "lanecol":(160, 100, 100), "wallcol":(180, 120, 120), "carcols":(car_darkred, car_red, car_lightred, car_brown, car_orange, car_lightorange, car_yellow, car_lightyellow, car_black, car_darkgray), "carsize":(85, 170)},
    "grassland":{"drag":0.105, "playerspd":1.105, "screenx":960, "screeny":700, "lanes":8, "lanesep":102, "lanewidth":10, "bgcol":(100, 160, 100), "lanecol":(60, 120, 60), "wallcol":(80, 140, 80), "carcols":(car_darkgreen, car_green, car_lightgreen, car_gray, car_olive, car_blue, car_yellow, car_red, car_white, car_purple, car_pink, car_lightpink, car_lightpurple, car_lightblue, car_brown), "carsize":(70, 140)}
          }

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
            screen.blit(pygame.transform.scale(pygame.transform.flip(entity["col"], False, True), (entity["xsc"], entity["ysc"])), ((ent_xpos, entity["y"]), (entity["xsc"], entity["ysc"])))
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
        rand_value = random.randint(0, round(((1+math.sqrt(len(entities)+1))*127)/difficulty))
        if rand_value == 0 and str(i) not in recent_generations:
            entities.append({"col":random.choice(biomes[current_biome]["carcols"]), "lane":random.randint(0, lanes), "y":-biomes[current_biome]["carsize"][1], "xsc":biomes[current_biome]["carsize"][0], "ysc":biomes[current_biome]["carsize"][1]})
            recent_generations[str(i)] = math.ceil(120/difficulty)
        if str(i) in recent_generations:
            recent_generations[str(i)] -= 1
            if recent_generations[str(i)] <= 0:
                recent_generations.pop(str(i))

    if temp:
        return "ded"
    return score_to_add

def setbiome(biomename): #doesnt work right now ):
    current_biome = biomename
    entities = []
    screen_width = biomes[biomename]["screenx"]
    screen_height = biomes[biomename]["screeny"]
    screen = pygame.display.set_mode((screen_width, screen_height))
    lanes = biomes[biomename]["lanes"]
    lanesep = biomes[biomename]["lanesep"]
    lanewidth = biomes[biomename]["lanewidth"]
    drag = biomes[biomename]["drag"]

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

        drawbg(biomes[current_biome]["bgcol"], biomes[current_biome]["lanecol"], biomes[current_biome]["wallcol"])

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
            screen.blit(pygame.transform.scale(car_gray, (player_x_size, player_y_size)), ((screen_width/2+player_x-player_x_size/2, player_y-player_y_size), (player_x_size, player_y_size)))
            #pygame.draw.rect(screen, (255, 200, 255), (screen_width/2+player_x-player_x_size/2, player_y-player_y_size, player_x_size, player_y_size))
        if devmode and devsettings["showhitboxes"]:
            pygame.draw.rect(screen, (0, 0, 255), (screen_width/2+player_x-player_x_size/2, player_y-player_y_size, 2, player_y_size))
            pygame.draw.rect(screen, (0, 0, 255), (screen_width/2+player_x-player_x_size/2, player_y-player_y_size, player_x_size, 2))
            pygame.draw.rect(screen, (0, 0, 255), (screen_width/2+player_x+player_x_size/2-2, player_y-player_y_size, 2, player_y_size))
            pygame.draw.rect(screen, (0, 0, 255), (screen_width/2+player_x-player_x_size/2, player_y-2, player_x_size, 2))

        entity_output = entitytick()
        if entity_output == "ded":
            highscore_read = open("high_score.txt")
            hs = "".join(list(highscore_read))
            message(f"high score : {hs}", (0, 0, 0), None, (screen_width/2, screen_height/2+80), "freesansbold.ttf", 16)
            if int(hs) < score:
                highscore_write = open("high_score.txt", "w")
                highscore_write.write(str(score))
                highscore_write.close()
                message(f"new high score ({score}) (:", (0, 0, 0), None, (screen_width/2, screen_height/2-50), "freesansbold.ttf", 23)
            highscore_read.close()
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
                    for biomename in ["null"]:
                        current_biome = biomename
                        entities = []
                        screen_width = biomes[biomename]["screenx"]
                        screen_height = biomes[biomename]["screeny"]
                        screen = pygame.display.set_mode((screen_width, screen_height))
                        lanes = biomes[biomename]["lanes"]
                        lanesep = biomes[biomename]["lanesep"]
                        lanewidth = biomes[biomename]["lanewidth"]
                        drag = biomes[biomename]["drag"]
                        player_speed = biomes[biomename]["playerspd"]
                    ticks = 0
                    ticks_ingame = 0
                    score = 0
                    player_x = 0
                    mov = [0, 0]
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
    
    #biome changes
    if score >= 50 and current_biome == "null":
        for biomename in ["frost"]:
            screen.fill((40, 40, 40))
            pygame.display.update()
            clock.tick(1.65)
            current_biome = biomename
            entities = []
            screen_width = biomes[biomename]["screenx"]
            screen_height = biomes[biomename]["screeny"]
            screen = pygame.display.set_mode((screen_width, screen_height))
            lanes = biomes[biomename]["lanes"]
            lanesep = biomes[biomename]["lanesep"]
            lanewidth = biomes[biomename]["lanewidth"]
            drag = biomes[biomename]["drag"]
            player_speed = biomes[biomename]["playerspd"]
    if score >= 175 and current_biome == "frost":
        for biomename in ["volcanic"]:
            screen.fill((40, 40, 40))
            pygame.display.update()
            clock.tick(1.65)
            current_biome = biomename
            entities = []
            screen_width = biomes[biomename]["screenx"]
            screen_height = biomes[biomename]["screeny"]
            screen = pygame.display.set_mode((screen_width, screen_height))
            lanes = biomes[biomename]["lanes"]
            lanesep = biomes[biomename]["lanesep"]
            lanewidth = biomes[biomename]["lanewidth"]
            drag = biomes[biomename]["drag"]
            player_speed = biomes[biomename]["playerspd"]
    if score >= 315 and current_biome == "volcanic":
        for biomename in ["grassland"]:
            screen.fill((40, 40, 40))
            pygame.display.update()
            clock.tick(1.65)
            current_biome = biomename
            entities = []
            screen_width = biomes[biomename]["screenx"]
            screen_height = biomes[biomename]["screeny"]
            screen = pygame.display.set_mode((screen_width, screen_height))
            lanes = biomes[biomename]["lanes"]
            lanesep = biomes[biomename]["lanesep"]
            lanewidth = biomes[biomename]["lanewidth"]
            drag = biomes[biomename]["drag"]
            player_speed = biomes[biomename]["playerspd"]

    pygame.display.update()
    clock.tick(60)
    ticks += 1
    difficulty = math.log(score+50)/1.69897