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


def main():
    pygame.init()
    (width, height) = (800,600)
    pygame.display.set_mode((width, height), DOUBLEBUF|OPENGL)

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()
    gluPerspective(20, width / float(height), 5, 15)
    glViewport(0, 0, width, height)

    glMatrixMode(GL_MODELVIEW)

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

        gyro_angle += imu_data[0] * delta_t
        acc_angle = np.degrees(np.atan2(imu_data[4], imu_data[5]))

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -10)
        glRotatef(-acc_angle, 0, 0, 1)
        Cube()
        pygame.display.flip()

main()
