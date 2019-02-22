
class Event(object):

    def __init__(self, controller, key, action):
        self.key = key
        self.action = action
        controller.add_event(self)
