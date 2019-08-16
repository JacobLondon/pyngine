class Event(object):
    """@brief Event object is used to simplify connecting a
    keypress or set of keypresses to a given function.
    """

    def __init__(self, controller, action=None, keys=()):
        """@brief Setup the event into the controller. \\
        @param Controller the parent controller. \\
        @param key Tuple of pygame.key presses. \\
        @param action A function to call on when the key combination is pressed
        """
        self.keys = keys
        self.action = action
        self.controller = controller
        self.controller.add_event(self)

    def halt(self):
        """@brief Forcibly stop the input from being read until the next input.
        """
        for key in self.keys:
            self.controller.keyboard.presses[key] = False
