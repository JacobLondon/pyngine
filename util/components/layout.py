
"""Create a grid within the given component
for ease of component placement on the display
"""
class Grid(object):

    """Map a grid to the given component"""
    def __init__(self, component, width=1, height=1):
        self.component = component
        self.width = component.width // width
        self.height = component.height // height

    # return top left pixel of given x, y coord on the grid
    """Return top left pixel x, y of a given grid intersection gx, gy"""
    def get_pixel(self, gx, gy):
        x = self.component.loc[0] + self.width * gx
        y = self.component.loc[1] + self.height * gy
        return (x, y)

"""Use relative locations on a given component
for ease of component placement on the display
"""
class Relative(object):

    """Find all relative locations within given component"""
    def __init__(self, component):

        self.x = component.anchored_loc[0]
        self.y = component.anchored_loc[1]
        self.width = component.width
        self.height = component.height

        # the pixel locations of the grid intersections
        self.north = (self.x + self.width / 2, self.y)
        self.northeast = (self.x + self.width, self.y)
        self.east = (self.x + self.width, self.y + self.height / 2)
        self.southeast = (self.x + self.width, self.y + self.height)
        self.south = (self.x + self.width / 2, self.y + self.height)
        self.southwest = (self.x, self.y + self.height)
        self.west = (self.x, self.y + self.height / 2)
        self.northwest = (self.x, self.y)

        self.center = (self.x + self.width / 2, self.y + self.height / 2)
