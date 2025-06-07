from machine import Pin, SoftI2C, PWM
from mpu6050 import MPU6050
from time import sleep
import math
servo_p = PWM(Pin(11))
servo_p.freq(50)
servo_r = PWM(Pin(3))
servo_r.freq(50)
i2c = SoftI2C(scl=Pin(21), sda=Pin(20))
print(i2c.scan())
mpu = MPU6050(i2c)
def angle_to_duty(angle):
    min_duty = 1638
    max_duty = 8192
    duty = int(min_duty + (angle/180) * (max_duty - min_duty))
    return duty
def set_servo_angle(servo, angle):
    servo.duty_u16(angle_to_duty(angle))
def smooth(prev, new, factor=0.9):
    return prev * factor + new * (1 - factor)
prev_pitch = 90
prev_roll = 90
def get_pitch_roll():
    accel = mpu.get_gyro()
    ax = accel['x']
    ay = accel['y']
    az = accel['z']
    pitch = math.degrees(math.atan2(ax, math.sqrt(ay**2 + az**2)))
    roll = math.degrees(math.atan2(ay, math.sqrt(ax**2 + az**2)))
    pitch = -pitch
    roll = -roll
    return pitch, roll
set_servo_angle(servo_p, 90)
set_servo_angle(servo_r, 90)
def get_tilt_direction():
    accel = mpu.get_gyro()
    ax = accel['x']
    ay = accel['y']
    az = accel['z']
    pitch = math.degrees(math.atan2(ax, math.sqrt(ay**2 + az**2)))
    roll = math.degrees(math.atan2(ay, math.sqrt(ax**2 + az**2)))
    direction = []
    if pitch > 10:
        direction.append("tilting forward")
    elif pitch < -10:
        direction.append("tilting backward")
    
    if roll > 10:
        direction.app
        end("tilting right")
    elif roll < -10:
        direction.append("tilting left")

    if not direction:
        direction.append("flat")

    return pitch, roll, direction
while True:
    
    pitch, roll = get_pitch_roll()
    servo_pitch_angle = 90 - pitch
    servo_roll_angle = 90 - roll
    smooth_roll = smooth(prev_roll, servo_roll_angle)
    smooth_pitch = smooth(prev_pitch, servo_pitch_angle)
    if abs(smooth_pitch - prev_pitch) > 1:
        set_servo_angle(servo_p, smooth_pitch)
        prev_pitch = smooth_pitch
    if abs(smooth_roll - prev_roll) > 1:
        set_servo_angle(servo_r, smooth_roll)
        prev_roll = smooth_roll
    print(f"Pitch: {pitch:.1f}, Roll: {roll:.1f} -> Servo P: {servo_pitch_angle:.1f}, Servo R: {servo_roll_angle:.1f}")
    
