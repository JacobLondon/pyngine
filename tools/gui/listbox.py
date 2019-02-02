import pygame

from ..graphics import Color
from ..constants import Font, Anchor
from ..mouse import Mouse
from .layout import Grid
from .component import Component
from .panel import Panel

class Listbox(Component):

    def __init__(self, controller, parent=None, z=0):
        Component.__init__(self, controller, parent)
        self.scrolled_index = 0
        self.num_visible_items = 5
        self.height_scaling = 0.9

        self.background = Color['darkgray']

    def load(self):
        
        self.item_height = self.height / self.num_visible_items * self.height_scaling
        self.set_anchor()

        self.item_layout = Grid(self, 1, self.num_visible_items)

        # traverse from the top shown component
        for i in range(len(self.subcomponents)):
            self.subcomponents[i].loc = self.item_layout.get_pixel(0, i - self.scrolled_index)
            self.subcomponents[i].width = self.width
            self.subcomponents[i].height = self.item_height
            self.subcomponents[i].anchor = Anchor.northeast

            # set visibility if on/off panel
            if i < self.scrolled_index:
                self.subcomponents[i].visible = False
            elif self.scrolled_index <= i < self.scrolled_index + self.num_visible_items:
                self.subcomponents[i].visible = self.visible
            else:
                self.subcomponents[i].visible = False
                
            self.subcomponents[i].load()

    def refresh_actions(self):

        # scroll control
        if self.hovering:
            if self.controller.mouse_presses[Mouse.scroll_up]:
                self.scroll_up()
            elif self.controller.mouse_presses[Mouse.scroll_down]:
                self.scroll_down()

    def scroll_up(self):
        if self.scrolled_index - 1 >= 0:
            self.scrolled_index -= 1
            self.load()

    def scroll_down(self):
        if self.scrolled_index + self.num_visible_items < len(self.subcomponents):
            self.scrolled_index += 1
            self.load()

    def add(self, component):
        self.subcomponents.append(component)

    def remove(self, component):
        self.subcomponents.remove(component)


