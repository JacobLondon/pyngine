import pygame

from .component import Component

class Panel(Component):

    def __init__(self, controller):
        Component.__init__(self, controller)

    def load(self):
        self.set_anchor()

    def draw(self):

        # draw the area of the panel
        self.controller.interface.draw_area(
            self.anchored_loc[0],
            self.anchored_loc[1],
            self.width,
            self.height,
            self.background)
