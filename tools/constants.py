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
    standard = pygame.font.SysFont('Sans MS', 20)
    large = pygame.font.SysFont('Sans MS', 40)
    menu = pygame.font.SysFont('Sans MS', 60)
    button = pygame.font.SysFont('Sans MS', 40)

class Anchor(object):
    northwest = 0
    northeast = 1
    southeast = 2
    southwest = 3
    center = 4
