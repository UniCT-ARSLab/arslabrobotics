#
# pid.py
#

__all__ = [
    "saturate",
    "P_Controller",
    "PI_Controller",
    "PID_Controller"
    ]

from arslabrobotics.system.basic import *
from typing import Optional

def saturate(inp: float, sat: float) -> tuple[float, bool]:
    """
    Saturates the input to a given value

    :param inp: the input
    :param sat: the saturation value
    :return: a tuple whose first element is the output,
             and the second is a boolean indicating if the saturation occurred
    """
    if inp > sat:
        return (sat, True)
    if inp < - sat:
        return (-sat, True)
    return (inp, False)


class P_Controller:

    def __init__(self, _kp: float, _sat: Optional[float] = None):
        """
        A Proportional controller with an optional saturation value

        :param _kp: The proportional constant
        :param _sat: The optional saturation value

        """
        self.kp = _kp
        self.saturation = _sat

    def evaluate(self, delta_t: float, _error: float) -> float:
        """
        Evaluates the controller

        :param delta_t: Sampling interval
        :param _error: Input value
        :return: Output value

        """
        out = self.kp * _error
        if self.saturation is not None:
            out, _ = saturate(out, self.saturation)
        return out


class PI_Controller:

    def __init__(self, _kp: float, _ki: float, _sat: Optional[float] = None):
        """
        A Proportional-Integral controller with an optional saturation value

        :param _kp: The proportional constant
        :param _ki: The integral constant
        :param _sat: The optional saturation value

        """
        self.kp = _kp
        self.ki = _ki
        self.i = Integrator()
        self.saturation = _sat
        self.in_saturation = False

    def evaluate(self, delta_t: float, _error: float) -> float:
        """
        Evaluates the controller

        :param delta_t: Sampling interval
        :param _error: Input value
        :return: Output value

        """
        out = self.kp * _error

        if self.in_saturation:
            out = out + self.ki * self.i.prev_output
        else:
            out = out + self.ki * self.i.evaluate(delta_t, _error)

        if self.saturation is not None:
            out, self.in_saturation = saturate(out, self.saturation)

        return out

class PID_Controller:

    def __init__(self, _kp: float, _ki: float, _kd : float, _sat: Optional[float] = None):
        """
        A Proportional-Integral-Derivative controller with an optional saturation value

        :param _kp: The proportional constant
        :param _ki: The integral constant
        :param _kd: The derivative constant
        :param _sat: The optional saturation value

        """
        self.kp = _kp
        self.ki = _ki
        self.kd = _kd
        self.saturation = _sat
        self.in_saturation = False
        self.I = Integrator()
        self.D = Derivator()

    def evaluate(self, delta_t: float, _error: float) -> float:
        """
        Evaluates the controller

        :param delta_t: Sampling interval
        :param _error: Input value
        :return: Output value

        """
        out = self.kp * _error

        if self.in_saturation:
            out = out + self.ki * self.I.prev_output
        else:
            out = out + self.ki * self.I.evaluate(delta_t, _error)

        out = out + self.kd * self.D.evaluate(delta_t, _error)

        if self.saturation is not None:
            out, self.in_saturation = saturate(out, self.saturation)

        return out

