from ..graphics import Image
from .component import Component

"""Component to hold an image for simpler z index placement"""
class Imagebox(Component):

    def __init__(self, controller, path, parent=None, z=0):
        Component.__init__(self, controller, parent, z)
        self.text = 'Imagebox'
        
        # create image and set methods to be the same
        self.image = Image(path)
        self.reset = self.image.reset
        self.rotate_by = self.image.rotate_by
        self.rotate_to = self.image.rotate_to
        self.scale_by = self.image.scale_by
        self.scale_to = self.image.scale_to

    """Load the image itself into the component"""
    def load(self):
        self.width = self.image.width
        self.height = self.image.height
        self.set_anchor()

        self.image.visible = self.visible
        self.image.loc = self.anchored_loc

    """Draw using the image's draw method"""
    def draw(self):
        self.image.draw(self.controller.interface.display)

