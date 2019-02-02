import pygame

from .component import Component
from .painter import Painter

class Panel(Component):

    def __init__(self, controller, parent=None, z=0):
        Component.__init__(self, controller, parent, z)
        self.painter = Painter(self.controller)
        self.text = 'Panel'

    def load(self):
        self.set_anchor()
        self.painter.color = self.background

    def draw(self):

        # draw the area of the panel
        self.painter.color = self.background
        self.painter.fill_area(
            self.anchored_loc[0],
            self.anchored_loc[1],
            self.width,
            self.height)
