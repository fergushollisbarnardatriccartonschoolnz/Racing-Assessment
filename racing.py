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

running_program = True
while running_program:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_program = False

    clock.tick(60)