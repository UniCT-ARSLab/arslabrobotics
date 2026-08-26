#
# speed.py
#

__all__ = [
    "DifferentialDriveSpeedControl"
    ]

from arslabrobotics.control.pid import *
from typing import Optional

class DifferentialDriveSpeedControl:

    def __init__(self, kp : float, ki : float, kd : float, sat: Optional[float] = None):
        """
        A class that implements the speed PID controllers for a differential drive robot.

        :param kp: The proportional constant
        :param ki: The integral constant
        :param kd: The derivative constant
        :param sat: The optional saturation value of the PID output

        """
        self.left_wheel = PID_Controller(kp, ki, kd, sat)
        self.right_wheel = PID_Controller(kp, ki, kd, sat)

        self.left_target = 0
        self.right_target = 0

    def set_targets(self, l : float, r : float) -> None:
        """
        Sets the target speed of the wheels.

        :param l: target speed of the left wheel
        :param r: target speed of the right wheel

        """
        self.left_target = l
        self.right_target = r

    def evaluate(self, delta_t, left_current, right_current):
        """
        Runs the controllers.

        :param delta_t: Sampling time
        :param left_current: Current speed of the left wheel
        :param right_current: Current speed of the right wheel
        :return: A tuple representing the outputs of the controllers (left_out, right_out)

        """
        left_out = self.left_wheel.evaluate(delta_t, self.left_target - left_current)
        right_out = self.right_wheel.evaluate(delta_t, self.right_target - right_current)
        return (left_out, right_out)


