import pygame

from .color import colors as Color

"""Helper class to use pygame for drawing lines/shapes/areas"""
class Painter(object):
    
    def __init__(self, interface):
        self.display = interface.display
        self.tile_width = interface.tile_width
        self.tile_height = interface.tile_height

    """Fill tile with color"""
    def fill_tile(self, gx, gy, color=Color['white']):
        area = [gx * self.tile_width, gy * self.tile_height, self.tile_width, self.tile_height]
        pygame.draw.rect(self.display, color, area)

    """Fill area with color"""
    def fill_area(self, x, y, width, height, color=Color['white']):
        area = [x, y, width, height]
        pygame.draw.rect(self.display, color, area)

    """Draw line from x0, y0 to x1, y1"""
    def draw_line(self, x0, y0, x1, y1, color=Color['white']):
        pygame.draw.line(self.display, color, (x0, y0), (x1, y1))

    """Draw triangle border lines"""
    def draw_triangle(self, x0, y0, x1, y1, x2, y2, color=Color['white']):
        self.draw_line(x0, y0, x1, y1, color)
        self.draw_line(x1, y1, x2, y2, color)
        self.draw_line(x2, y2, x0, y0, color)

    """Fill the triangle with color"""
    def fill_triangle(self, x0, y0, x1, y1, x2, y2, color=Color['white']):
        pointlist = [(x0, y0), (x1, y1), (x2, y2)]
        pygame.draw.polygon(self.display, color, pointlist)
