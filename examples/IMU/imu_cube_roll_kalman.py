#
#
#
import numpy as np
import arslabrobotics as ar

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

class RollAngleKF:

    def __init__(self):
        self.A = np.array( [ [1, 1e-2],
                              [0, 1] ] )
        self.x = np.array( [ [0], [0] ])

        self.Q = np.eye(2) * 1e-3
        self.R = np.eye(2) * 1e-2
        self.P = np.eye(2)
        self.H = np.array( [ [1, 0],
                             [0, 0] ])

    def predict(self, delta_t, omega):
        self.A[0, 1] = delta_t  # update A
        self.x[1, 0] = omega    # add first measurement

        self.x = self.A @ self.x
        self.P = self.A @ self.P @ self.A.T + self.Q

    def udpate(self, acc_angle):
        z = np.array( [ [acc_angle], [0] ])
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ (z - self.H @ self.x)
        self.P = (np.eye(2) - K @ self.H) @ self.P



def main():
    pygame.init()
    (width, height) = (800,600)
    pygame.display.set_mode((width, height), DOUBLEBUF|OPENGL)

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()
    gluPerspective(20, width / float(height), 5, 15)
    glViewport(0, 0, width, height)

    glMatrixMode(GL_MODELVIEW)

    filter = RollAngleKF()

    imu = ar.system.IMUDriver()
    imu.open()

    tm = ar.utils.Time()
    tm.start()

    glMatrixMode(GL_MODELVIEW)

    gyro_angle = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        imu_data = imu.sample()
        delta_t = tm.elapsed()

        filter.predict(delta_t, imu_data[0])

        gyro_angle += imu_data[0] * delta_t
        acc_angle = np.degrees(np.atan2(imu_data[4], imu_data[5]))

        filter.update(acc_angle)

        filtered_angle = filter.x[0,0]

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -10)
        glRotatef(-filtered_angle, 0, 0, 1)
        Cube()
        pygame.display.flip()

main()
