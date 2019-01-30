import pygame

from .constants import Color

class Painter(object):
    
    def __init__(self, display, color=Color.white):
        self.color = color
        self.display = display

    # fill tile with color
    def fill_tile(self, gx, gy):
        area = [gx * self.tile_width, gy * self.tile_height, self.tile_width, self.tile_height]
        pygame.draw.rect(self.display, self.color, area)

    # fill given area with color
    def fill_area(self, x, y, width, height):
        area = [x, y, width, height]
        pygame.draw.rect(self.display, self.color, area)

    def draw_line(self, x0, y0, x1, y1):
        pygame.draw.line(self.display, self.color, (x0, y0), (x1, y1))

    def draw_triangle(self, x0, y0, x1, y1, x2, y2):
        self.draw_line(x0, y0, x1, y1, self.color)
        self.draw_line(x1, y1, x2, y2, self.color)
        self.draw_line(x2, y2, x0, y0, self.color)

    def fill_triangle(self, x0, y0, x1, y1, x2, y2):
        pointlist = [(x0, y0), (x1, y1), (x2, y2)]
        pygame.draw.polygon(self.display, self.color, pointlist)
