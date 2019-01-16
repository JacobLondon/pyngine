
from .constants import Anchor

class Screen_Object(object):

    def __init__(self):
        self.loc = (0, 0)
        self.anchored_loc = (0, 0)
        self.width = 0
        self.height = 0
        self.anchor = Anchor.northwest
        self.visible = True

    # set the relative location determined by the anchor used
    def set_anchor(self):

        if self.anchor == Anchor.northwest:
            self.anchored_loc = self.loc
        elif self.anchor == Anchor.northeast:
            self.anchored_loc = (self.loc[0] - self.width, self.loc[1])
        elif self.anchor == Anchor.southwest:
            self.anchored_loc = (self.loc[0], self.loc[1] - self.height)
        elif self.anchor == Anchor.southeast:
            self.anchored_loc = (self.loc[0] - self.width, self.loc[1] - self.height)
        elif self.anchor == Anchor.center:
            self.anchored_loc = (self.loc[0] - self.width / 2, self.loc[1] - self.height / 2)