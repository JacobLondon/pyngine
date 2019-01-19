import pygame

from .layout import Grid
from .constants import Color, Font, Anchor, Mouse
from .component import Component
from .panel import Panel

class Listbox(Component):

    def __init__(self, controller, parent=None, in_foreground=True):
        Component.__init__(self, controller, parent, in_foreground)
        self.scrolled_index = 0
        self.num_visible_items = 5
        self.subcomponents = []

        self.background = Color.dark_gray

        self.panel = Panel(self.controller, parent=None)

    def load(self):
        
        self.item_height = self.height / self.num_visible_items * 0.9
        self.set_anchor()

        # update the panel with correct attributes
        self.panel.loc = self.loc
        self.panel.width = self.width
        self.panel.height = self.height
        self.panel.background = self.background
        self.panel.anchor = self.anchor
        self.panel.visible = self.visible
        self.panel.load()

        self.item_layout = Grid(self, 1, self.num_visible_items)

        # traverse from the top shown component
        for i in range(self.num_visible_items):
            index = i + self.scrolled_index
            if index >= len(self.subcomponents):
                break

            self.subcomponents[index].visible = self.visible
            self.subcomponents[index].loc = self.item_layout.get_pixel(0, i)

            self.subcomponents[index].width = self.width
            self.subcomponents[index].height = self.item_height
            self.subcomponents[index].anchor = Anchor.northeast
            self.subcomponents[index].load()       

    def refresh_actions(self):

        # scroll control
        if self.hovering:
            if self.controller.mouse_presses[Mouse.scroll_up]:
                self.scroll_up()
            elif self.controller.mouse_presses[Mouse.scroll_down]:
                self.scroll_down()

    def scroll_up(self):
        print('scroll up')
        if self.scrolled_index - 1 >= 0:
            self.scrolled_index -= 1
            self.load()

    def scroll_down(self):
        print('scroll down')
        if self.scrolled_index + 1 <= len(self.subcomponents):
            self.scrolled_index += 1
            self.load()

    def add(self, component):
        self.subcomponents.append(component)

    def remove(self, component):
        self.subcomponents.remove(component)


