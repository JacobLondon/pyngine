import pygame

from .component import Component

"""A simple component used for displaying text"""
class Label(Component):

    def __init__(self, controller, text, parent=None, z=0):
        Component.__init__(self, controller, parent, z)
        self.text = text
        self.background = None

    """Load text details into Label"""
    def load(self):
        pygame.font.init()
        self.width, self.height = self.font.size(self.text)
        self.set_anchor()

    """Put the text into a surface and blit it to the display"""
    def draw(self):

        # draw the text in the component
        surface_args = [self.text, True, self.foreground, self.background]
        self.text_surface = self.font.render(*surface_args)
        self.controller.interface.display.blit(self.text_surface, self.anchored_loc)
