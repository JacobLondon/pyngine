import pygame
from decimal import *

from .constants import Color, Font, Anchor
from .component import Component
from .panel import Panel
from .label import Label
from .layout import Relative

class Bar(Component):
    
    def __init__(self, controller, parent=None):
        Component.__init__(self, controller, parent)
        self.percentage = 0
        self.text = '0 %'

        self.background = Color.dark_gray
        self.foreground = Color.green
        self.font = Font.large
        self.width, self.height = self.font.size(self.text)

        # panels for front/back, label for percentage text
        self.back_panel = Panel(self.controller, parent=self)
        self.front_panel = Panel(self.controller, parent=self)
        self.label = Label(self.controller, self.text, parent=self)
        self.label.anchor = Anchor.center

    def load(self):

        self.set_anchor()

        # update the background
        self.back_panel.loc = self.loc
        self.back_panel.width = self.width
        self.back_panel.height = self.height
        self.back_panel.background = self.background
        self.back_panel.anchor = self.anchor
        self.back_panel.visible = self.visible
        self.back_panel.load()

        # update foreground
        self.load_layout = Relative(self.back_panel)
        self.front_panel.loc = self.load_layout.northwest
        self.front_panel.width = self.width * self.percentage / 100
        self.front_panel.height = self.height
        self.front_panel.background = self.foreground
        self.front_panel.anchor = Anchor.northwest
        self.front_panel.visible = self.visible
        self.front_panel.load()

        # update the label with the percentage
        self.center_layout = Relative(self.back_panel)
        self.label.loc = self.center_layout.center
        self.label.text = self.text
        self.label.font = self.font
        self.label.foreground = Color.black
        self.label.background = None
        self.label.visible = self.visible
        self.label.load()

    def refresh_actions(self):
        self.text = str(self.percentage) + ' %'

    '''Increase the percentage bar showing
    total_size: the total number of steps needed for 100%
    step: the step that the program is at
    '''
    def increment(self, total_size, step):
        if step > total_size:
            self.percentage = 100
        elif step > 0:
            self.percentage = int(step / total_size * 100)
        else:
            self.percentage = 0

        self.load()

    def complete(self):
        self.percentage = 100
        self.load()