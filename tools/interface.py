import pygame

from .graphics import Color
from .constants import Font

"""Pygame interface for controller to use.

Use defaults to simplify screen/display creation.
"""
class Interface(object):

    def __init__(self, window_text='Pyngine', resolution=(400,400), grid_width=40, grid_height=40, refresh_rate=60):

        # pygame initialization
        pygame.init()
        pygame.font.init()

        # screen definitions
        self.resolution = resolution
        self.tile_width = resolution[0] / grid_width
        self.tile_height = resolution[1] / grid_height
        self.center = (self.resolution[0] / 2, self.resolution[1] / 2)
        self.area = [0, 0, self.resolution[0], self.resolution[1]]

        # how long each from SHOULD take
        self.refresh_rate = refresh_rate
        self.frame_time = 1 / self.refresh_rate

        # pygame variables and initialization
        self.display = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(window_text)
        pygame.display.update()
        self.clock = pygame.time.Clock()

        # calling close is the same as calling pygame.quit()
        self.close = pygame.quit

    """Return the x, y tile that the mouse is in."""
    def get_mouse_tile(self):
        x, y = pygame.mouse.get_pos()
        tx = x // self.tile_width
        ty = y // self.tile_height
        return (tx, ty)

    """Return the top left x, y pixel that tile tx, ty is at"""
    def get_tile_pixel(self, tx, ty):
        return (tx * self.tile_width, ty * self.tile_height)

    """Update Pygame based on clock and refresh rate."""
    def update(self):
        # update loaded images
        pygame.display.update()
        self.clock.tick(self.refresh_rate)

    """Set the screen to black"""
    def clear(self):
        pygame.draw.rect(self.display, Color['black'], self.area)
