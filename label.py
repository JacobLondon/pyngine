import pygame

from .constants import Color, Font, Anchor
from .component import Component

class Label(Component):

    def __init__(self, controller, text, parent=None):
        Component.__init__(self, controller, parent)
        self.text = text

    def load(self):
        pygame.font.init()
        self.width, self.height = self.font.size(self.text)
        self.set_anchor()

    def draw(self):

        # draw the text in the component
        surface_args = [self.text, True, self.foreground, self.background]
        self.text_surface = self.font.render(*surface_args)
        self.controller.interface.display.blit(self.text_surface, self.anchored_loc)
