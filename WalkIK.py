# Not used in final version, but created for testing. Didn't have enough time to implement full IK and tune

import math
import time

from Walk import BL1, BL2, BL3, BR1, BR2, BR3, FL1, FL2, FL3, FR1, FR2, FR3

HIP_OFFSET = 25.0
THIGH = 55.0
SHIN = 65.0 
STAND_HEIGHT = 85.0
BODY_LENGTH = 120.0
BODY_WIDTH = 75.0
KNEES_POINT_BACKWARD = True
STEP_LENGTH = 30.0
STEP_HEIGHT = 18.0
STRAFE_LENGTH = 20.0
TURN_ANGLE = 10.0
STEP_TIME = 0.6 
FRAME_TIME = 0.02 

class IKLeg:
    def __init__(self, name, abduction, hip, knee, front, left, outward, forward, bend):
        self.name = name
        self.motors = (abduction, hip, knee)
        self.signs = (outward, forward, bend)
        self.hip_x = BODY_LENGTH / 2 if front else -BODY_LENGTH / 2
        self.hip_y = BODY_WIDTH / 2 if left else -BODY_WIDTH / 2
        self.left = left
        self.neutral_angles = leg_ik(0.0, HIP_OFFSET, STAND_HEIGHT)

    def neutral_foot(self):
        outward = HIP_OFFSET if self.left else -HIP_OFFSET
        return (self.hip_x, self.hip_y + outward, -STAND_HEIGHT)

    def to_leg_frame(self, foot):
        dx = foot[0] - self.hip_x
        dy = foot[1] - self.hip_y
        dz = foot[2]
        outward = dy if self.left else -dy
        return dx, outward, -dz

    def servo_angles(self, foot):
        angles = leg_ik(*self.to_leg_frame(foot))
        result = []
        for motor, sign, angle, neutral in zip(self.motors, self.signs, angles, self.neutral_angles):
            degrees = motor.default + sign * math.degrees(angle - neutral)
            result.append(min(180.0, max(0.0, degrees)))
        return result

    def move_foot(self, foot):
        for motor, degrees in zip(self.motors, self.servo_angles(foot)):
            motor.set(degrees)


def leg_ik(forward, outward, down):
    side = max(math.hypot(outward, down), HIP_OFFSET + 1e-6)
    leg_plane_down = math.sqrt(side ** 2 - HIP_OFFSET ** 2)
    abduction = math.atan2(outward, down) - math.atan2(HIP_OFFSET, leg_plane_down)

    reach = math.hypot(forward, leg_plane_down)
    reach = min(max(reach, abs(THIGH - SHIN) + 1e-6), THIGH + SHIN - 1e-6)
    knee_inside = math.acos((THIGH ** 2 + SHIN ** 2 - reach ** 2) / (2 * THIGH * SHIN))
    knee = math.pi - knee_inside

    foot_direction = math.atan2(forward, leg_plane_down)
    thigh_offset = math.acos((THIGH ** 2 + reach ** 2 - SHIN ** 2) / (2 * THIGH * reach))
    if KNEES_POINT_BACKWARD:
        hip = foot_direction - thigh_offset
    else:
        hip = foot_direction + thigh_offset
    return abduction, hip, knee


def leg_fk(abduction, hip, knee):
    shin_angle = hip + knee if KNEES_POINT_BACKWARD else hip - knee
    forward = THIGH * math.sin(hip) + SHIN * math.sin(shin_angle)
    leg_plane_down = THIGH * math.cos(hip) + SHIN * math.cos(shin_angle)
    outward = HIP_OFFSET * math.cos(abduction) + leg_plane_down * math.sin(abduction)
    down = -HIP_OFFSET * math.sin(abduction) + leg_plane_down * math.cos(abduction)
    return forward, outward, down


FL = IKLeg("FL", FL1, FL2, FL3, front=True, left=True, outward=-1, forward=-1, bend=+1)
FR = IKLeg("FR", FR1, FR2, FR3, front=True, left=False, outward=+1, forward=+1, bend=-1)
BL = IKLeg("BL", BL1, BL2, BL3, front=False, left=True, outward=+1, forward=-1, bend=+1)
BR = IKLeg("BR", BR1, BR2, BR3, front=False, left=False, outward=-1, forward=+1, bend=-1)
LEGS = [FL, FR, BL, BR]

PAIR_A = [FL, BR]
PAIR_B = [FR, BL]

feet = {leg: leg.neutral_foot() for leg in LEGS}


# ---------------------------------------------------------------------------
# Body poses
# ---------------------------------------------------------------------------

def unrotate(point, roll, pitch, yaw):
    x, y, z = point
    x, y = x * math.cos(-yaw) - y * math.sin(-yaw), x * math.sin(-yaw) + y * math.cos(-yaw)
    x, z = x * math.cos(-pitch) + z * math.sin(-pitch), -x * math.sin(-pitch) + z * math.cos(-pitch)
    y, z = y * math.cos(-roll) - z * math.sin(-roll), y * math.sin(-roll) + z * math.cos(-roll)
    return x, y, z


def posed_feet(roll=0.0, pitch=0.0, yaw=0.0, shift_x=0.0, shift_y=0.0, height=0.0):
    r, p, y = math.radians(roll), math.radians(pitch), math.radians(yaw)
    result = {}
    for leg in LEGS:
        fx, fy, fz = leg.neutral_foot()
        moved = (fx - shift_x, fy - shift_y, fz - height)
        result[leg] = unrotate(moved, r, p, y)
    return result


def move_feet(targets, duration):
    start = dict(feet)
    frames = max(1, int(duration / FRAME_TIME))
    for i in range(1, frames + 1):
        t = smooth(i / frames)
        for leg, target in targets.items():
            s = start[leg]
            feet[leg] = tuple(a + (b - a) * t for a, b in zip(s, target))
            leg.move_foot(feet[leg])
        time.sleep(FRAME_TIME)


def smooth(t):
    return t * t * (3 - 2 * t)

def step_vector(leg, step_x, step_y, step_yaw):
    yaw = math.radians(step_yaw)
    fx, fy, _ = leg.neutral_foot()
    return step_x - yaw * fy, step_y + yaw * fx


def foot_at(leg, step, progress, swing_fraction=None):
    fx, fy, fz = leg.neutral_foot()
    lift = 0.0
    if swing_fraction is not None:
        lift = STEP_HEIGHT * math.sin(math.pi * swing_fraction)
    return fx + step[0] * progress, fy + step[1] * progress, fz + lift


def trot(step_x=0.0, step_y=0.0, step_yaw=0.0):
    if any(math.dist(feet[leg], leg.neutral_foot()) > 0.5 for leg in LEGS):
        reset()
    steps = {leg: step_vector(leg, step_x, step_y, step_yaw) for leg in LEGS}
    phases = [
        (PAIR_A, PAIR_B, 0.0, 0.5, 0.0, -0.5, 0.25),
        (PAIR_B, PAIR_A, -0.5, 0.5, 0.5, -0.5, 0.5),
        (PAIR_A, PAIR_B, -0.5, 0.0, 0.5, 0.0, 0.25),
    ]
    for swing_pair, ground_pair, swing_from, swing_to, ground_from, ground_to, share in phases:
        frames = max(1, int(STEP_TIME * share / FRAME_TIME))
        for i in range(1, frames + 1):
            t = i / frames
            for leg in swing_pair:
                feet[leg] = foot_at(leg, steps[leg], swing_from + (swing_to - swing_from) * t, swing_fraction=t)
            for leg in ground_pair:
                feet[leg] = foot_at(leg, steps[leg], ground_from + (ground_to - ground_from) * t)
            for leg in LEGS:
                leg.move_foot(feet[leg])
            time.sleep(FRAME_TIME)

def reset():
    move_feet({leg: leg.neutral_foot() for leg in LEGS}, 0.25)


def walk():
    trot(step_x=STEP_LENGTH)


def walk_back():
    trot(step_x=-STEP_LENGTH)


def walk_right():
    trot(step_y=-STRAFE_LENGTH)


def walk_left():
    trot(step_y=STRAFE_LENGTH)


def turn_right():
    trot(step_yaw=-TURN_ANGLE)


def turn_left():
    trot(step_yaw=TURN_ANGLE)


def sit():
    reset()
    move_feet(posed_feet(pitch=-20, shift_x=-15, height=-10), 1.0)


def dance():
    reset()
    for _ in range(2):
        move_feet(posed_feet(shift_y=15, roll=-8), 0.3)
        move_feet(posed_feet(shift_y=-15, roll=8), 0.3)
    reset()

    for _ in range(3):
        for angle in range(0, 360, 30):
            a = math.radians(angle)
            move_feet(posed_feet(roll=10 * math.cos(a), pitch=10 * math.sin(a)), 0.07)
    reset()

    walk()
    walk()
    walk_back()
    walk_back()
    walk()

    time.sleep(0.5)
    sit()


def lift():
    reset()
    # Lean back and to the left so the other three feet hold the robot up.
    targets = posed_feet(shift_x=-15, shift_y=12, pitch=-5)
    move_feet(targets, 0.8)
    fx, fy, fz = targets[FR]
    targets[FR] = (fx + 35, fy, fz + 45)
    move_feet(targets, 0.8)
