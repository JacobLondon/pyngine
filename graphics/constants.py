import pygame

class Color(object):

    black = (0,0,0)
    dark_gray = (80,80,80)
    light_gray = (160,160,160)
    white = (255,255,255)
    red = (255,0,0)
    blue = (0,0,255)
    green = (0,255,0)

    background = black
    foreground = white
    pause = (24, 26, 31)
    button = (80,84,92)
    hover = (144,151,165)
    missile = (57,179,255)

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

class Mouse(object):
    l_click = 1
    m_click = 2
    r_click = 3
    scroll_up = 4
    scroll_down = 5
