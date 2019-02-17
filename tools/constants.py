import pygame

class Dir(object):

    right = 1
    left = 2
    down = 3
    up = 4
    up_right = 5
    down_right = 6
    down_left = 7
    up_left = 8

class Font(object):
    pygame.font.init()
    default = 'Calibri'

    small = pygame.font.SysFont(default, 10)
    standard = pygame.font.SysFont(default, 20)
    large = pygame.font.SysFont(default, 40)

    button = pygame.font.SysFont(default, 40)
    menu = pygame.font.SysFont(default, 60)
    title = pygame.font.SysFont(default, 80)
