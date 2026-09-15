import serial
import time
import pydirectinput

PORT = "COM11"
BAUD = 9600

pydirectinput.PAUSE = 0.01

print("Connecting to Arduino...")
arduino = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

# -------------------------
# AUTO CALIBRATION
# -------------------------

print("DON'T TOUCH THE JOYSTICK")
print("Calibrating...")

xs = []
ys = []

start = time.time()

while time.time() - start < 2:
    line = arduino.readline().decode(errors="ignore").strip()

    try:
        values = {}

        for item in line.split():
            if "=" in item:
                name, value = item.split("=")
                values[name] = int(value)

        xs.append(values["X"])
        ys.append(values["Y"])

    except:
        pass

CENTER_X = sum(xs) // len(xs)
CENTER_Y = sum(ys) // len(ys)

print()
print("Calibration complete!")
print("CENTER X:", CENTER_X)
print("CENTER Y:", CENTER_Y)
print()

DEADZONE = 60

held = set()


def key_down(key):
    if key not in held:
        pydirectinput.keyDown(key)
        held.add(key)
        print("DOWN:", key)


def key_up(key):
    if key in held:
        pydirectinput.keyUp(key)
        held.remove(key)
        print("UP:", key)


def set_key(key, condition):
    if condition:
        key_down(key)
    else:
        key_up(key)


print("Controller running!")
print("Move joystick. Ctrl+C to stop.")
print()

try:

    while True:

        line = arduino.readline().decode(errors="ignore").strip()

        if not line:
            continue

        try:
            values = {}

            for item in line.split():
                if "=" in item:
                    name, value = item.split("=")
                    values[name] = int(value)

            x = values["X"]
            y = values["Y"]

        except:
            continue

        # LEFT / RIGHT
        set_key("a", x < CENTER_X - DEADZONE)
        set_key("d", x > CENTER_X + DEADZONE)

        # UP / DOWN
        set_key("w", y < CENTER_Y - DEADZONE)
        set_key("s", y > CENTER_Y + DEADZONE)

except KeyboardInterrupt:

    print("\nStopping...")

finally:

    for key in list(held):
        pydirectinput.keyUp(key)

    arduino.close()