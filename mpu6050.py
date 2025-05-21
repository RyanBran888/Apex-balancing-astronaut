from machine import I2C
import time

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')

    def read_raw(self, reg):
        data = self.i2c.readfrom_mem(self.addr, reg, 2)
        value = int.from_bytes(data, 'big', True)
        return value

    def get_accel(self):
        return {
            'x': self.read_raw(0x3B) / 16384,
            'y': self.read_raw(0x3D) / 16384,
            'z': self.read_raw(0x3F) / 16384
        }

    def get_gyro(self):
        return {
            'x': self.read_raw(0x43) / 131,
            'y': self.read_raw(0x45) / 131,
            'z': self.read_raw(0x47) / 131
        }

    def get_temp(self):
        temp_raw = self.read_raw(0x41)
        return temp_raw / 340 + 36.53