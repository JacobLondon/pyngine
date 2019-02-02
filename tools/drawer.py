
''' Acts like a component but with custom functions to pass in
'''
class Drawer(object):

    def __init__(self, controller, refresh=None, load=None, z=0):
        controller.add(self, z)

        if refresh is not None:
            self.refresh = refresh
        if load is not None:
            self.load = load

    def __str__(self):
        return 'Drawer'

    def load(self):
        pass

    def refresh(self):
        pass