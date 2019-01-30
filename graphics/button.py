import pygame

from .constants import Color, Font, Anchor
from .component import Component
from .panel import Panel
from .label import Label
from .layout import Relative

class Button(Component):

        def __init__(self, controller, text, parent=None, z=0, in_foreground=True):
            Component.__init__(self, controller, parent, z, in_foreground)
            self.text = text
            self.action = None
            self.scale = 2
            self.pressed = False

            self.background = Color.button
            self.foreground = Color.black
            self.hover = Color.hover
            self.font = Font.button

            # adjust the button to the given scale size
            self.width, self.height = self.font.size(self.text)
            self.width *= self.scale
            self.height *= self.scale

            # button is made with a label on a panel
            self.panel = Panel(self.controller, parent=self)

            self.label = Label(self.controller, self.text, parent=self)
            self.label.anchor = Anchor.center

        def load(self):

            self.set_anchor()

            # update the panel with button's members
            self.panel.loc = self.loc
            self.panel.width = self.width
            self.panel.height = self.height
            self.panel.background = self.background
            self.panel.anchor = self.anchor
            self.panel.visible = self.visible
            self.panel.load()

            # update the label with button's members
            self.center_layout = Relative(self.panel)
            self.label.loc = self.center_layout.center
            self.label.text = self.text
            self.label.font = self.font
            self.label.foreground = self.foreground
            self.label.background = None
            self.label.visible = self.visible
            self.label.load()

        def refresh_actions(self):
            if self.hovering:
                self.panel.background = self.hover
            else:
                self.panel.background = self.background

            # do action on focus
            if self.focused and self.action is not None:
                self.focused = False
                self.action()
