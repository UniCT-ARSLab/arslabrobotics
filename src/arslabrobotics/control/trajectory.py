#
# trajectory.py
#

import math
import numpy as np
from arslabrobotics.utils.geometry import *

# ------------------------------------------------------------

class VirtualRobot:
    """
    This class implements the algoritm of the linear trajectory
    generation for a virtual robot moving over a straight line of a certain distance
    with an acceleration, a cruise speed and a deceleration.
    """
    ACCEL = 0
    CRUISE = 1
    DECEL = 2
    TARGET = 3

    def __init__(self, _p_target : float, _vmax : float, _acc : float, _dec : float):
        """
        Initializes the linear trajectory

        :param _p_target: the distance to drive
        :param _vmax: the maximum speed
        :param _acc: the acceleration
        :param _dec: the deceleration

        """
        self.p_target = _p_target
        self.vmax = _vmax
        self.accel = _acc
        self.decel = _dec
        self.v = 0  # current speed
        self.p = 0  # current position
        self.phase = VirtualRobot.ACCEL
        self.decel_distance = 0.5 * _vmax * _vmax / _dec

    def start(self, _p_target : float):
        """
        Restarts the trajectory

        :param _p_target: the new distance to drive

        """
        self.p_target = _p_target
        self.v = 0  # current speed
        self.p = 0  # current position
        self.phase = VirtualRobot.ACCEL

    def evaluate(self, delta_t : float) -> None:
        """
        Executes a trajectory step

        :param delta_t: the sampling time

        """
        if self.phase == VirtualRobot.ACCEL:
            self.p = self.p + self.v * delta_t \
                     + self.accel * delta_t * delta_t / 2
            self.v = self.v + self.accel * delta_t
            distance = self.p_target - self.p
            if distance < 0:
                distance = 0
            if self.v >= self.vmax:
                self.v = self.vmax
                self.phase = VirtualRobot.CRUISE
            elif distance <= self.decel_distance:
                v_exp = math.sqrt(2 * self.decel * distance)
                if v_exp < self.v:
                    self.phase = VirtualRobot.DECEL

        elif self.phase == VirtualRobot.CRUISE:
            self.p = self.p + self.vmax * delta_t
            distance = self.p_target - self.p
            if distance <= self.decel_distance:
                self.phase = VirtualRobot.DECEL

        elif self.phase == VirtualRobot.DECEL:
            self.p = self.p + self.v * delta_t \
                     - self.decel * delta_t * delta_t / 2
            v = self.v - self.decel * delta_t
            if v >= 0:
                self.v = v
            if self.p >= self.p_target:
                self.v = 0
                self.p = self.p_target
                self.phase = VirtualRobot.TARGET
        elif self.phase == VirtualRobot.TARGET:
            self.v = 0
            self.p = self.p_target

    def speed(self) -> float:
        """
        Returns the current speed
        """
        return self.v

    def position(self) -> float:
        """
        Returns the current position
        """
        return self.p

    def target_got(self) -> bool:
        """
        Returns a boolean indicating if the distance has been traveled
        """
        return self.phase == VirtualRobot.TARGET

# ------------------------------------------------------------

class StraightLine2DMotion:
    """
    This class performs a linear motion over a 2D space form a point (x_start, y_start)
    to a point (x_end, y_end)
    """

    def __init__(self, _vmax : float, _acc : float, _dec : float):
        """
        Initializes the trajectory

        :param _vmax: the maximum speed
        :param _acc: the acceleration
        :param _dec: the deceleration

        """
        self.vmax = _vmax
        self.accel = _acc
        self.decel = _dec

    def start_motion(self, start : tuple[float, float], end : tuple[float, float]) -> None:
        """
        Starts the trajectory

        :param start: a tuple (x,y) indicating the starting point
        :param end: a tuple (x,y) indicating the ending point

        """
        (self.xs,self.ys) = start
        (self.xe,self.ye) = end
        dx = self.xe - self.xs
        dy = self.ye - self.ys
        self.heading = math.atan2(dy , dx)
        self.distance = math.sqrt(dx*dx + dy*dy)
        self.virtual_robot = VirtualRobot(self.distance,
                                          self.vmax, self.accel, self.decel)

    def evaluate(self, delta_t : float) -> tuple[float,float]:
        """
        Executes a trajectory step

        :param delta_t: the sampling time
        :return: the current position (x,y)

        """
        self.virtual_robot.evaluate(delta_t)
        xt = self.xs + self.virtual_robot.p * math.cos(self.heading)
        yt = self.ys + self.virtual_robot.p * math.sin(self.heading)
        return (xt, yt)

# ------------------------------------------------------------

class StraightLineMotion:

    """
    This class performs a linear motion over a generic n-dimensional space form a point
    start to a point end.

    Start and end are supposed to be robot poses made of cartesian coordinates and angles.

    """
    def __init__(self, _vmax : float, _acc : float, _dec : float, angles_index = -1):
        """
        Initializes the trajectory

        angles_index specifies the element in the pose where the angles start.
        For example, in a 2D where the pose is (x,y,theta), angles_index would be 2.

        :param _vmax: the maximum speed
        :param _acc: the acceleration
        :param _dec: the deceleration
        :param angles_index: the index in the pose where the angles start

        """
        self.vmax = _vmax
        self.accel = _acc
        self.decel = _dec
        self.angles_index = angles_index

    def start_motion(self, start, end):
        """
        Starts the trajectory

        :param start: the starting pose
        :param end: the ending pose

        """
        self.start = np.array(start)
        self.end = np.array(end)
        self.size = len(start)
        self.diff = self.end - self.start
        self.__normalize_angles(self.diff)
        self.distance = np.linalg.norm(self.diff)
        self.virtual_robot = VirtualRobot(self.distance,
                                          self.vmax, self.accel, self.decel)

    def evaluate(self, delta_t : float) -> list[float]:
        """
        Executes a trajectory step

        :param delta_t: the sampling time
        :return: the current position

        """
        self.virtual_robot.evaluate(delta_t)
        param = self.virtual_robot.p / self.distance
        new_pos = self.start + param * self.diff
        self.__normalize_angles(new_pos)
        return new_pos.flatten().tolist()

    def __normalize_angles(self, a):
        if self.angles_index >= 0:
            for i in range(self.angles_index, self.size):
                a[i] = normalize_angle(a[i])

    def target_got(self):
        """
        Returns a boolean indicating if the final position has been reached
        """
        return self.virtual_robot.target_got()

# ------------------------------------------------------------

class Path2D:
    """
    This class generates a trajectory using a list of points in a 2D space. It travels over the points
    making a stop for each point of the trajectory.
    """
    def __init__(self, _vmax : float, _acc : float, _dec : float, _threshold : float):
        """
        Initializes the path

        :param _vmax: the maximum speed
        :param _acc: the acceleration
        :param _dec: the deceleration
        :param _threshold: a distance threshold that is used to check if a point of
                           the trajectory has been reaced

        """
        self.threshold = _threshold
        self.path = [ ]
        self.trajectory = StraightLine2DMotion(_vmax, _acc, _dec)

    def set_path(self, path : list[tuple[float, float]]) -> None:
        """
        Specifies the path to be traveled

        :param path: a list of tuples (x,y)

        """
        self.path = path

    def start(self, start_pos : tuple[float,float]) -> None:
        """
        Starts the path specifying the starting position

        :param start_pos: a tuple (x,y)

        """
        self.current_target = self.path.pop(0)
        self.trajectory.start_motion(start_pos, self.current_target)

    def evaluate(self, delta_t : float, pose : tuple[float,float]):
        """
        Executes a trajectory step

        :param delta_t: the sampling time
        :param pose: the real current pose of the robot
        :return: the current position in the trajector or None if the path is over

        """
        (x, y) = self.trajectory.evaluate(delta_t)

        target_distance = math.hypot(pose[0] - self.current_target[0],
                                         pose[1] - self.current_target[1])

        if target_distance < self.threshold:
            if len(self.path) == 0:
                return None
            else:
                self.start( (x,y) )

        return (x,y)

 # ------------------------------------------------------------

class ContinuousPath2D:
    """
    This class generates a continuous trajectory using a list of points in a 2D space.
    It has the same behaviour of Path2D but avoids stopping for each point of the trajectory,
    instead it performs a smoothed motion.
    """
    def __init__(self, _vmax, _acc, _dec, _threshold):
        self.threshold = _threshold
        self.path = [ ]
        self.trajectory = VirtualRobot(0, _vmax, _acc, _dec)

    def set_path(self, path):
        self.path = path

    def start(self, start_pos):
        self.total_distance = 0
        self.cumulative_segment_length = []
        p = start_pos
        for next_point in self.path:
            d = math.hypot(next_point[0] - p[0],
                           next_point[1] - p[1])
            self.total_distance += d
            self.cumulative_segment_length.append(self.total_distance)
            p = next_point

        self.current_segment = 0
        self.first_segment_point = start_pos
        self.second_segment_point = self.path[0]
        self.trajectory.start(self.total_distance)
        self.end_of_path = False

    def evaluate(self, delta_t, current_pose):
        if self.end_of_path:
            d = math.hypot(self.path[-1][0] - current_pose[0],
                           self.path[-1][1] - current_pose[1])
            if d < self.threshold:
                return None
            else:
                return self.path[-1]
        self.trajectory.evaluate(delta_t)
        p = self.trajectory.position()
        if p >= self.cumulative_segment_length[self.current_segment]:
            self.current_segment += 1
            if self.current_segment == len(self.path):
                #print("End of path")
                self.end_of_path = True
                return self.path[-1]
            self.first_segment_point = self.second_segment_point
            self.second_segment_point = self.path[self.current_segment]

        # siamo all'interno del segmento "self.current_segment"
        #print("Segment ", self.current_segment, " - position ", p)

        dx = self.second_segment_point[0] - self.first_segment_point[0]
        dy = self.second_segment_point[1] - self.first_segment_point[1]
        angle = math.atan2(dy, dx)
        if self.current_segment == 0:
            distance_on_the_segment = p
        else:
            distance_on_the_segment = p - self.cumulative_segment_length[self.current_segment - 1]

        x = self.first_segment_point[0] + distance_on_the_segment * math.cos(angle)
        y = self.first_segment_point[1] + distance_on_the_segment * math.sin(angle)

        return (x,y)

