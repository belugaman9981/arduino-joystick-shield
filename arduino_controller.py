import serial
import pydirectinput
import time

# CHANGE THIS TO YOUR ARDUINO COM PORT
PORT = "COM3"

arduino = serial.Serial(PORT, 115200, timeout=1)

time.sleep(2)

pydirectinput.PAUSE = 0

held = set()

def hold(key):
    if key not in held:
        pydirectinput.keyDown(key)
        held.add(key)

def release(key):
    if key in held:
        pydirectinput.keyUp(key)
        held.remove(key)

def update_key(key, pressed):
    if pressed:
        hold(key)
    else:
        release(key)

print("Arduino game controller running!")
print("CTRL+C to stop")

while True:
    try:
        line = arduino.readline().decode(errors="ignore").strip()

        if not line:
            continue

        parts = line.split(",")

        if len(parts) != 8:
            continue

        x = int(parts[0])
        y = int(parts[1])

        buttonA = int(parts[2])
        buttonB = int(parts[3])
        buttonC = int(parts[4])
        buttonD = int(parts[5])
        buttonE = int(parts[6])
        joystickButton = int(parts[7])

        # ----------------------
        # JOYSTICK -> WASD
        # ----------------------

        DEAD_LOW = 350
        DEAD_HIGH = 670

        # LEFT / RIGHT
        update_key("a", x < DEAD_LOW)
        update_key("d", x > DEAD_HIGH)

        # UP / DOWN
        update_key("w", y < DEAD_LOW)
        update_key("s", y > DEAD_HIGH)

        # ----------------------
        # BUTTONS
        # ----------------------

        update_key("space", buttonA)
        update_key("e", buttonB)
        update_key("shift", joystickButton)

        # Mouse attack
        if buttonC:
            pydirectinput.mouseDown(button="left")
        else:
            pydirectinput.mouseUp(button="left")

        # Mouse use / place
        if buttonD:
            pydirectinput.mouseDown(button="right")
        else:
            pydirectinput.mouseUp(button="right")

        update_key("esc", buttonE)

    except KeyboardInterrupt:
        break

    except Exception as e:
        print(e)

# Release everything when program closes
for key in list(held):
    pydirectinput.keyUp(key)

pydirectinput.mouseUp(button="left")
pydirectinput.mouseUp(button="right")

arduino.close()