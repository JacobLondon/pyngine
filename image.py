import pygame

from .screen_object import Screen_Object

class Image(Screen_Object):

    def __init__(self, path):
        Screen_Object.__init__(self)
        self.path = path

        self.surf = pygame.image.load(self.path).convert_alpha()
        self.width = self.surf.get_width()
        self.height = self.surf.get_height()

        self.reset()

    def reset(self):
        self.angle = 0
        self.scale = 1

    def rotate(self, degrees):
        self.angle = (self.angle + degrees) % 360
        self.surf = pygame.transform.rotate(self.surf, self.angle)

    def scale(self, percentage):
        self.scale *= percentage
        sfactor = (self.width * self.scale, self.height * self.scale)
        self.surf = pygame.transform.scale(self.surf, sfactor)

    def draw(self, display):
        if self.visible:
            display.blit(self.surf, self.anchored_loc)

