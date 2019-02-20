
class Event(object):

    def __init__(controller, key, action):
        self.key = key
        self.action = action
        controller.add_event(self)

    def action(self):
        pass