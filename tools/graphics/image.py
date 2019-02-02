import pygame, numpy as np

from ..gui.screen_object import ScreenObject

"""Wrapper class for pygame's image functionality

NOTE: Image does NOT handle z index placement.
Images should be loaded into drawers/imageboxes for image drawing
with z index placement.
"""
class Image(ScreenObject):

    def __init__(self, path):
        ScreenObject.__init__(self)
        self.path = path

        # get details about the surface
        self.surf = pygame.image.load(self.path).convert_alpha()
        self.width = self.surf.get_width()
        self.height = self.surf.get_height()

        self.reset()

    def __str__(self):
        return self.path

    """Reset the rotation/scaling of an image"""
    def reset(self):
        self.angle = 0
        self.scale = 1

    """Rotate TO a given angle

    WARNING: Functionality NOT tested
    """
    def rotate_to(self, radians):

        # delta angle how much to rotate by to get from current to required angle
        end_angle = radians * 180 / np.pi
        self.angle = end_angle - self.angle

        self.surf = pygame.transform.rotate(self.surf, self.angle)
        
    """Scale image to given width/height"""
    def scale_to(self, width, height):
        sfactor = (int(width), int(height))
        self.surf = pygame.transform.scale(self.surf, sfactor)

    """Rotate BY a given angle from the current angle

    WARNING: Functionality NOT tested
    """
    def rotate_by(self, radians):
        self.angle = (self.angle + radians * 180 / np.pi) % 360

        self.surf = pygame.transform.rotate(self.surf, self.angle)

    """Scale image by percentage"""
    def scale_by(self, percentage):
        self.scale *= percentage
        sfactor = (self.width * self.scale, self.height * self.scale)
        self.surf = pygame.transform.scale(self.surf, sfactor)

    """Draw image if visible"""
    def draw(self, display):
        if self.visible:
            display.blit(self.surf, self.loc)

    """Fill all pixels of the surface with color, preserve transparency."""
    def fill(self, color):
        w, h = self.surf.get_size()
        r, g, b = color
        for x in range(w):
            for y in range(h):
                a = self.surf.get_at((x, y))[3]
                self.surf.set_at((x, y), pygame.Color(r, g, b, a))