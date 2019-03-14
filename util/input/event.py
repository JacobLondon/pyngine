"""Event object is used to simplify connecting a
keypress or set of keypresses to a given function.
"""
class Event(object):

    """Setup the event into the controller
    @param controller: the parent controller
    @param key: tuple of pygame.key presses
    @param action: a function to call on when the key combination is pressed
    """
    def __init__(self, controller, action=None, keys=()):
        self.keys = keys
        self.action = action
        controller.add_event(self)
