#
# inverted_pendulum.py
#

__all__ = [
    "InvertedPendulum",
    ]

import numpy as np

class InvertedPendulum:

    def __init__(
        self,
        _Cart_mass: float,
        _pendulum_mass: float,
        _Cart_friction: float,
        _pendulum_length: float
    ):
        """
        Defines a cart robot of a 1D environment with an inverted pendulum.

        :param _Cart_mass: The mass of the cart, expressed in Kg
        :param _pendulum_mass: The mass of the medulum
        :param _Cart_friction: The friction coefficient of the cart
        :param _pendulum_length: The length of the pendulum

        """
        self.M = _Cart_mass
        self.m = _pendulum_mass
        self.b = _Cart_friction
        self.l = _pendulum_length / 2
        self.I = (self.m * 4 * self.l**2) / 3
        self.g = 9.8

        self.x = 0
        self.x_d = 0
        self.phi = 0
        self.phi_d = 0

    def p(self):
        return self.I * (self.M + self.m) + self.M * self.m * self.l * self.l

    def evaluate(self, delta_t, u):
        x1 = self.x + self.x_d * delta_t

        x_d1 = self.x_d \
              + delta_t * (-self.b * (self.I + self.m * self.l * self.l) / self.p()) * self.x_d \
              + delta_t * ((self.m * self.m * self.g * self.l * self.l) / self.p()) * self.phi \
              + delta_t * ((self.I + self.m * self.l * self.l) / self.p()) * u

        phi1 = self.phi + self.phi_d * delta_t

        phi_d1 = self.phi_d \
           + delta_t * ((-self.m * self.l * self.b) / self.p()) * self.x_d \
           + delta_t * ((self.m * self.g * self.l * (self.M + self.m)) / self.p()) * self.phi \
           + delta_t * ((self.m * self.l) / self.p()) * u

        self.x = x1
        self.x_d = x_d1
        self.phi = phi1
        self.phi_d = phi_d1

    def discrete_state_space(self, delta_t):
        a1 = [1, delta_t, 0, 0]
        a2 = [0, 1 + delta_t * (-self.b * (self.I + self.m * self.l * self.l) / self.p()),
              delta_t * ((self.m * self.m * self.g * self.l * self.l) / self.p()),
              0]
        a3 = [0, 0, 1, delta_t]
        a4 = [0, delta_t * ((-self.m * self.l * self.b) / self.p()),
              delta_t * ((self.m * self.g * self.l * (self.M + self.m)) / self.p()),
              1]
        A = np.array([a1, a2, a3, a4])
        B = np.array([[0],
                      [delta_t * ((self.I + self.m * self.l * self.l) / self.p())],
                      [0],
                      [delta_t * ((self.m * self.l) / self.p())] ] )
        return (A, B)

    def get_status(self) -> tuple[float, float, float, float]:
        return self.x, self.x_d, self.phi, self.phi_d

    def set_angle(self, phi):
        self.phi = phi

