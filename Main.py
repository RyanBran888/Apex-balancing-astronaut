from machine import Pin, SoftI2C, PWM
from mpu6050 import MPU6050
from time import sleep
import math

servo_roll = PWM(Pin(11))
servo_roll.freq(50)
servo_pitch = PWM(Pin(3))
servo_pitch.freq(50)

i2c = SoftI2C(scl=Pin(21), sda=Pin(20))
mpu = MPU6050(i2c)

def angle_to_duty(angle):
    angle = max(0, min(180, angle))
    min_duty = 1638
    max_duty = 8192
    return int(min_duty + (angle / 180) * (max_duty - min_duty))

def set_servo_angle(servo, angle):
    servo.duty_u16(angle_to_duty(angle))

SMOOTH_FACTOR = 0.90  # Less smoothing, more responsive
MOVEMENT_THRESHOLD = 0.2  # Smaller threshold for movement detection

def smooth(prev, new, factor=SMOOTH_FACTOR):
    return prev * factor + new * (1 - factor)

def get_pitch_roll():
    accel = mpu.get_accel()
    ax, ay, az = accel['x'], accel['y'], accel['z']
    pitch = math.degrees(math.atan2(ax, math.sqrt(ay**2 + az**2)))
    roll = math.degrees(math.atan2(ay, math.sqrt(ax**2 + az**2)))
    return pitch, roll

pitch_offset = 0
roll_offset = 0

roll_center = 140
pitch_center = 90

prev_roll = roll_center
prev_pitch = pitch_center

set_servo_angle(servo_roll, roll_center)
set_servo_angle(servo_pitch, pitch_center)

while True:
    pitch, roll = get_pitch_roll()
    pitch = pitch
    roll = roll
    pitch = max(-45, min(45, pitch - pitch_offset))
    roll = max(-45, min(45, roll - roll_offset))

    servo_roll_angle = roll_center - max(-30, min(30, roll * 0.66))
    servo_pitch_angle = pitch_center - max(-30, min(30, pitch * 0.66))

    servo_roll_angle = max(0, min(180, servo_roll_angle))
    servo_pitch_angle = max(0, min(180, servo_pitch_angle))

    smooth_roll = smooth(prev_roll, servo_roll_angle)
    smooth_pitch = smooth(prev_pitch, servo_pitch_angle)

    if abs(smooth_roll - prev_roll) > MOVEMENT_THRESHOLD:
        set_servo_angle(servo_roll, smooth_roll)
        prev_roll = smooth_roll

    if abs(smooth_pitch - prev_pitch) > MOVEMENT_THRESHOLD:
        set_servo_angle(servo_pitch, smooth_pitch)
        prev_pitch = smooth_pitch
    sleep(0.05)
