# Quadruped Robot Dog

A Raspberry Pi-powered quadruped robot dog controlled by a PS4 controller. Uses 8 servo motors and the Adafruit PCA9685 driver for walking, turning, sitting, and dancing. You can find images, videos, and CAD screenshots in the following [google drive folder](https://drive.google.com/drive/folders/1YYMrmW3EgGKGc-ENeqzOh4piAwOo36y2?usp=drive_link).


## Features

- PS4 controller support (USB/Bluetooth)
- Realistic gait & motion logic
- Modular OOP design for leg control
- Powered by Raspberry Pi + PCA9685


## Hardware

- Raspberry Pi (any model with GPIO)
- Adafruit PCA9685 16-Channel PWM Driver
- 12x Servo Motors (e.g. MG90s)
- External 5V power supply
- PS4 Controller (USB or Bluetooth)
- Optional: USB Bluetooth Dongle


## Setup

```bash
sudo apt update && sudo apt upgrade
sudo raspi-config  # Enable I2C
pip3 install adafruit-circuitpython-servokit pyPS4Controller adafruit-blinka
sudo apt install i2c-tools
i2cdetect -y 1  # Should show 0x40
```


## Usage

```bash
python3 Controller.py
```


## PS4 Default Controls:

- `R2` - Walk Forward
- `L2` - Walk Backward
- `↑/↓/←/→` - Turn
- `X` - Default Standing Position
- `O` - Sit
- `▢` - Dance
- `△` - Lift a leg

## File Structure

```
robot-dog/
├── Controller.py
├── Walk.py
└── README.md
```