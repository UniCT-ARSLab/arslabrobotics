#
#
#

from phidias.Types import *
from phidias.Main import *
from phidias.Lib import *

from cart_model import *

class CartInstance:

    _instance = None

    def __init__(self):
        CartInstance._instance = self
        self.cart = CartModel()

    def go_to(self, X, Y):
        self.cart.set_pos_target(X, Y)


class CartStart(Action):
    def execute(self):
        unused = CartInstance()


class CartGo(Action):
    def execute(self, x, y):
        CartInstance._instance.go_to(x(), y())


class go(Procedure): pass


go() >> [ CartStart(), CartGo(1.5, 1.5) ]

PHIDIAS.run()
PHIDIAS.shell(globals())
