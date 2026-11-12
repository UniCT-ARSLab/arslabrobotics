#
# imu_driver.py
#

__all__ = [
    "IMUDriver"
    ]


import serial

class IMUDriver:

    gyro_res = 0.00875
    acc_res = 0.000224

    def __init__(self, port='/dev/ttyACM0', baud=115200):
        self.__p = port
        self.__b = baud

    def open(self):
        self.__ser = serial.Serial(self.__p, self.__b, 8, "N", 1, 1000)

    def sample(self):
        self.__ser.write([0x20])
        while True:
            line = self.__ser.readline()
            line = line.decode('utf8')
            #print(line)
            if line[0:1] == "#":
                break
        values = list(map(int, line[1:].split()))
        values[0] *= self.gyro_res
        values[1] *= self.gyro_res
        values[2] *= self.gyro_res
        values[3] *= self.acc_res
        values[4] *= self.acc_res
        values[5] *= self.acc_res
        return values



if __name__ == "__main__":
    import math

    drv = IMUDriver()
    drv.open()
    while True:
        v = drv.sample()
        angle = math.degrees(math.atan2(v[4], v[5]))
        print(v[4:6], angle)

