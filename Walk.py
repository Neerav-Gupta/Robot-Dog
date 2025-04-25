from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

class Motor():
    def __init__(self, port, default):
        self.port = port
        self.default = default
    
    def set(self, value):
        kit.servo[self.port].angle = value
    
    def reset(self):
        kit.servo[self.port].angle = self.default
    
class Leg():
    def __init__(self, motor1, motor2, motor3):
        self.motor1 = motor1
        self.motor2 = motor2
        self.motor3 = motor3
        self.motors = [motor1, motor2, motor3]
        
    def reset(self):
        for motor in self.motors:
            motor.reset()
        
class Robot():
    def __init__(self, leg1, leg2, leg3, leg4):
        self.leg1 = leg1
        self.leg2 = leg2
        self.leg3 = leg3
        self.leg4 = leg4
        self.legs = [leg1, leg2, leg3, leg4]
    
    def reset(self):
        for leg in self.legs:
            leg.reset()

BR1 = Motor(0, 75)
BR2 = Motor(4, 130)
BR3 = Motor(8, 90)
BR_leg = Leg(BR1, BR2, BR3)

BL1 = Motor(1, 100)
BL2 = Motor(5, 45)
BL3 = Motor(9, 100)
BL_leg = Leg(BL1, BL2, BL3)

FR1 = Motor(2, 95)
FR2 = Motor(6, 140)
FR3 = Motor(10, 75)
FR_leg = Leg(FR1, FR2, FR3)

FL1 = Motor(3, 80)
FL2 = Motor(7, 40)
FL3 = Motor(11, 110)
FL_leg = Leg(FL1, FL2, FL3)


robot = Robot(BR_leg, BL_leg, FR_leg, FL_leg)

def reset():
    robot.reset()
    time.sleep(0.25)
    
def walk():
    FL3.set(FL3.default+10)
    BR3.set(BR3.default-10)
    time.sleep(0.1)
    FL2.set(FL2.default-20)
    BR2.set(BR2.default+20)
    time.sleep(0.1)
    FL3.reset()
    BR3.reset()
    time.sleep(0.1)
    FR3.set(FR3.default-10)
    BL3.set(BL3.default+10)
    FL2.reset()
    BR2.reset()
    time.sleep(0.1)
    FR2.set(FR2.default+20)
    BL2.set(BL2.default-20)
    time.sleep(0.1)
    FR3.reset()
    BL3.reset()
    time.sleep(0.1)
    FR2.reset()
    BL2.reset()
    robot.reset()
    time.sleep(0.1)

def walk_right():
    FL3.set(FL3.default+10)
    BR3.set(BR3.default-10)
    time.sleep(0.1)
    FL1.set(FL1.default+20)
    BR1.set(BR1.default-20)
    time.sleep(0.1)
    FL3.reset()
    BR3.reset()
    time.sleep(0.1)
    FR3.set(FR3.default-10)
    BL3.set(BL3.default+10)
    FL1.reset()
    BR1.reset()
    time.sleep(0.1)
    FR1.set(FR1.default+20)
    BL1.set(BL1.default-20)
    time.sleep(0.1)
    FR3.reset()
    BL3.reset()
    time.sleep(0.1)
    FR1.reset()
    BL1.reset()
    robot.reset()
    time.sleep(0.1)

def walk_left():
    FL3.set(FL3.default+10)
    BR3.set(BR3.default-10)
    time.sleep(0.1)
    FL1.set(FL1.default-20)
    BR1.set(BR1.default+20)
    time.sleep(0.1)
    FL3.reset()
    BR3.reset()
    time.sleep(0.1)
    FR3.set(FR3.default-10)
    BL3.set(BL3.default+10)
    FL1.reset()
    BR1.reset()
    time.sleep(0.1)
    FR1.set(FR1.default-20)
    BL1.set(BL1.default+20)
    time.sleep(0.1)
    FR3.reset()
    BL3.reset()
    time.sleep(0.1)
    FR1.reset()
    BL1.reset()
    robot.reset()
    time.sleep(0.1)

def walk_back():
    FL3.set(FL3.default+10)
    BR3.set(BR3.default-10)
    time.sleep(0.1)
    FL2.set(FL2.default+20)
    BR2.set(BR2.default-20)
    time.sleep(0.1)
    FL3.reset()
    BR3.reset()
    time.sleep(0.1)
    FR3.set(FR3.default-10)
    BL3.set(BL3.default+10)
    FL2.reset()
    BR2.reset()
    time.sleep(0.1)
    FR2.set(FR2.default-20)
    BL2.set(BL2.default+20)
    time.sleep(0.1)
    FR3.reset()
    BL3.reset()
    time.sleep(0.1)
    FR2.reset()
    BL2.reset()
    robot.reset()
    time.sleep(0.1)

def turn_right():
    FL3.set(FL3.default+10)
    BR3.set(BR3.default-10)
    time.sleep(0.1)
    FL2.set(FL2.default-20)
    BR2.set(BR2.default-20)
    time.sleep(0.1)
    FL3.reset()
    BR3.reset()
    time.sleep(0.1)
    FR3.set(FR3.default-10)
    BL3.set(BL3.default+10)
    FL2.reset()
    BR2.reset()
    time.sleep(0.1)
    FR2.set(FR2.default-20)
    BL2.set(BL2.default-20)
    time.sleep(0.1)
    FR3.reset()
    BL3.reset()
    time.sleep(0.1)
    FR2.reset()
    BL2.reset()
    robot.reset()
    time.sleep(0.1)
    
def turn_left():
    FL3.set(FL3.default+10)
    BR3.set(BR3.default-10)
    time.sleep(0.1)
    FL2.set(FL2.default+20)
    BR2.set(BR2.default+20)
    time.sleep(0.1)
    FL3.reset()
    BR3.reset()
    time.sleep(0.1)
    FR3.set(FR3.default-10)
    BL3.set(BL3.default+10)
    FL2.reset()
    BR2.reset()
    time.sleep(0.1)
    FR2.set(FR2.default+20)
    BL2.set(BL2.default+20)
    time.sleep(0.1)
    FR3.reset()
    BL3.reset()
    time.sleep(0.1)
    FR2.reset()
    BL2.reset()
    robot.reset()
    time.sleep(0.1)
    
def sit():
    robot.reset();
    BR3.set(BR3.default-20)
    BL3.set(BL3.default+20)
    FR3.set(FR3.default+40)
    FL3.set(FL3.default-40)
    time.sleep(3)
    BR3.set(BR3.default-30)
    BL3.set(BL3.default+30)
    FR3.set(FR3.default+40)
    FL3.set(FL3.default-40)
    FL1.set(FL1.default+20)

def dance():
    for i in range(2):
        FL1.set(FL1.default-20)
        BR1.set(BR1.default+20)
        FR1.set(FR1.default-20)
        BL1.set(BL1.default+20)
        time.sleep(0.3)
        robot.reset()
        time.sleep(0.3)
        FL1.set(FL1.default+20)
        BR1.set(BR1.default-20)
        FR1.set(FR1.default+20)
        BL1.set(BL1.default-20)
        time.sleep(0.3)
        robot.reset()
        time.sleep(0.3)
        
    for i in range(3):
        BR3.set(BR3.default-20)
        time.sleep(0.2)
        robot.reset()
        time.sleep(0.2)
        BL3.set(BL3.default+20)
        time.sleep(0.2)
        robot.reset()
        time.sleep(0.2)
        FL3.set(FL3.default+20)
        time.sleep(0.2)
        robot.reset()
        time.sleep(0.2)
        FR3.set(FR3.default-20)
        time.sleep(0.2)
        robot.reset()
        time.sleep(0.2)
    
    walk()
    walk()
    walk_back()
    walk_back()
    walk()
    
    time.sleep(0.5)
    
    BR3.set(BR3.default-20)
    BL3.set(BL3.default+20)
    FR3.set(FR3.default+40)
    FL3.set(FL3.default-40)
    
def lift():
    
    FR3.set(FR3.default-20)
    FR2.set(FR2.default+40)
    time.sleep(1)
    FR3.set(FR3.default+60)
    time.sleep(1)
    FR2.set(180)
    FR3.set(FR3.default-20)