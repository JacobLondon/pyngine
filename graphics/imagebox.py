
from .component import Component
from .image import Image

class Imagebox(Component):

    def __init__(self, controller, path, parent=None, z=0, in_foreground=True):
        Component.__init__(self, controller, parent, z, in_foreground)
        
        self.image = Image(path)
        self.reset = self.image.reset
        self.rotate_by = self.image.rotate_by
        self.rotate_to = self.image.rotate_to
        self.scale_by = self.image.scale_by
        self.scale_to = self.image.scale_to

    def load(self):
        self.width = self.image.width
        self.height = self.image.height
        self.set_anchor()

        self.image.visible = self.visible
        self.image.loc = self.anchored_loc

    def draw(self):
        self.image.draw(self.controller.interface.display)

