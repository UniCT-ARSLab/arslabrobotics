#
# basic.py
#

__all__ = [
    "Proportional",
    "Derivator",
    "Integrator",
    "LinearDynamicSystem"
    ]

import numpy as np

class Proportional:

    def __init__(self, _kp : float):
        """
        Defines proportional block

        :param _kp: The constant to be multiplied by the input

        """
        self.kp = _kp

    def evaluate(self, delta_t : float, _input : float) -> None:
        """
        Computes the output of proportional block

        :param _input: The input
        :param delta_t: The sampling time
        :return: The input times the constant

        """
        return _input * self.kp


class Derivator:

    def __init__(self):
        """
        Defines a derivator
        """
        self.prev_input = 0

    def evaluate(self, delta_t : float, _input : float) -> float:
        """
        Computes the output of the derivator block

        :param _input: The input
        :param delta_t: The sampling time
        :return: The input derivated

        """
        out = (_input - self.prev_input) / delta_t
        self.prev_input = _input
        return out


class Integrator:

    def __init__(self):
        """
        Defines an integrator
        """
        self.prev_output = 0

    def evaluate(self, delta_t : float, _input) -> float:
        """
        Computes the output of the integrator

        :param _input: The input
        :param delta_t: The sampling time
        :return: The integrated data

        """
        out = self.prev_output + _input * delta_t
        self.prev_output = out
        return out


class LinearDynamicSystem:

    def __init__(self, A, B, C):
        """
        Defines a linear system of type:

        ..math::

            \dot{x} = A x + B u\\
            y = C x

        :param A: The state matrix
        :param B: The input matrix
        :param C: The output matrix

        """
        self.A = np.array(A)
        self.B = np.array(B)
        self.C = np.array(C)
        self.order = len(A)
        self.x = np.array( [0] *  self.order)

    def evaluate(self, delta_t : float, _input : float):
        """
        Evaluates the output of the linear system given the input. Evaluation is made
        by using the Euler approximation.

        :param delta_t: The sampling time
        :param _input: The input
        :returns: The output

        """
        self.x = (self.A * delta_t + np.eye(self.order)) @ self.x + self.B * delta_t * _input
        output = self.C @ self.x
        return output.flatten().tolist()

    def eig(self):
        """
        Returns the eigenvalues of matrix A
        """
        return np.linalg.eig(self.A)

