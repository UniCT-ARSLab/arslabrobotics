#
# cart model for simulation with godot
#
# TO BE USED WITH godot/cart2D_no_physics
#

import arslabrobotics as ar
import threading
import sys
import math

class CartModel:

    def __init__(self, plotting = False):
        self.dds = ar.dds.DDS()
        self.dds.start()
        #dds.subscribe(['tick'])
        self.WB = 0.3
        self.cart2d = ar.system.TwoWheelsCart2D(10.0, 0.15, 0.9, 0.9, self.WB)
        self.speed_ctrl = ar.control.DifferentialDriveSpeedControl(10.0, 2.0, 0.0, 20.0)
        self.polar_ctrl = ar.control.Polar2DController(0.5,
                                                       1.0, # 1 m/s
                                                       0.4,
                                                       math.radians(90)) # 180 deg/s

        self.wheel_targets = [0, 0]
        self.pos_target = [0, 0]
        self.plotting = plotting

        if self.plotting:
            self.dpleft = ar.data.DataPlotter()
            self.dpleft.set_x("time (seconds)")
            self.dpleft.add_y("speed", "left speed (m/s)")

            self.dpright = ar.data.DataPlotter()
            self.dpright.set_x("time (seconds)")
            self.dpright.add_y("speed", "right speed (m/s)")

        self.t = threading.Thread(target = self.run)
        self.t.start()


    def set_wheel_targets(self, VL, VR):
        self.wheel_targets = [VL, VR]
        self.speed_ctrl.set_targets(VL, VR)

    def set_pos_target(self, X, Y):
        self.pos_target = [X, Y]

    def run(self):
        t = ar.utils.Time()
        t.start()
        self.running = True
        while self.running:
            #dds.wait('tick')
            t.sleep(0.05)
            delta_t = t.elapsed()

            pose = self.cart2d.get_pose()
            # polar control
            (v, w) = self.polar_ctrl.evaluate(delta_t,
                                              self.pos_target[0], self.pos_target[1],
                                              pose)

            # speed control
            (vl, vr) = self.cart2d.get_wheel_speeds()
            vl_t = v - w / self.WB
            vr_t = v + w / self.WB
            self.speed_ctrl.set_targets(vl_t, vr_t)
            (fl, fr) = self.speed_ctrl.evaluate(delta_t, vl, vr)

            # cart model
            self.cart2d.evaluate(delta_t, fl, fr)

            self.dds.publish('X', pose[0], ar.dds.DDS_TYPE_FLOAT)
            self.dds.publish('Y', pose[1], ar.dds.DDS_TYPE_FLOAT)
            self.dds.publish('Theta', pose[2], ar.dds.DDS_TYPE_FLOAT)

            if self.plotting:
                self.dpleft.append_x(t.get())
                self.dpleft.append_y("speed", vl)

                self.dpright.append_x(t.get())
                self.dpright.append_y("speed", vr)

                if t.get() > 10:
                    self.dpleft.plot()
                    self.dpright.plot()
                    self.dds.stop()
                    sys.exit(0)

        self.dds.stop()



if __name__ == "__main__":
    m = CartModel(plotting = True)
    #m.set_wheel_targets(1.2,1.2)
    m.set_pos_target(1.2,0.5)

