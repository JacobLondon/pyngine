import sys
sys.path.append('..')

from src import *

class ExampleController(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface, debug=True)

if __name__ ==  '__main__':
    # create a pygame interface
    interface = Interface()
    # create a controller to run the interface
    example = ExampleController(interface)
    # run the controller
    example.run()
    