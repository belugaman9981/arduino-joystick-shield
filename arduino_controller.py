import serial
import time
import pydirectinput

PORT = "COM11"
BAUD = 9600

pydirectinput.PAUSE = 0.01

print("Connecting to Arduino...")

arduino = serial.Serial(
    PORT,
    BAUD,
    timeout=1
)

time.sleep(2)

# =========================================================
# AUTO CALIBRATION
# =========================================================

print()
print("DO NOT TOUCH THE JOYSTICK")
print("Calibrating for 2 seconds...")

xs = []
ys = []

start = time.time()

while time.time() - start < 2:

    line = arduino.readline().decode(
        errors="ignore"
    ).strip()

    if not line:
        continue

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

if len(xs) == 0 or len(ys) == 0:

    print("ERROR: No joystick data received.")
    print("Check COM port and Arduino code.")

    arduino.close()

    input("Press Enter to exit...")

    raise SystemExit


CENTER_X = sum(xs) // len(xs)
CENTER_Y = sum(ys) // len(ys)

DEADZONE = 70

print()
print("Calibration complete.")
print("CENTER X:", CENTER_X)
print("CENTER Y:", CENTER_Y)
print()
print("Controller running.")
print()
print("Joystick mapping:")
print("DOWN  = W")
print("LEFT  = A")
print("UP    = S")
print("RIGHT = D")
print()
print("Buttons:")
print("TOP        = SPACE")
print("BOTTOM     = E")
print("LEFT BLUE  = LEFT CLICK")
print("RIGHT BLUE = RIGHT CLICK")
print("STICK CLICK = SHIFT")
print()
print("Press Ctrl+C to stop.")
print()


# =========================================================
# KEY HANDLING
# =========================================================

held_keys = set()


def key_down(key):

    if key not in held_keys:

        pydirectinput.keyDown(key)

        held_keys.add(key)

        print("DOWN:", key)


def key_up(key):

    if key in held_keys:

        pydirectinput.keyUp(key)

        held_keys.remove(key)

        print("UP:", key)


def set_key(key, pressed):

    if pressed:
        key_down(key)

    else:
        key_up(key)


# =========================================================
# MOUSE BUTTON HANDLING
# =========================================================

left_mouse_down = False
right_mouse_down = False


def set_left_mouse(pressed):

    global left_mouse_down

    if pressed and not left_mouse_down:

        pydirectinput.mouseDown(
            button="left"
        )

        left_mouse_down = True

        print("LEFT MOUSE DOWN")

    elif not pressed and left_mouse_down:

        pydirectinput.mouseUp(
            button="left"
        )

        left_mouse_down = False

        print("LEFT MOUSE UP")


def set_right_mouse(pressed):

    global right_mouse_down

    if pressed and not right_mouse_down:

        pydirectinput.mouseDown(
            button="right"
        )

        right_mouse_down = True

        print("RIGHT MOUSE DOWN")

    elif not pressed and right_mouse_down:

        pydirectinput.mouseUp(
            button="right"
        )

        right_mouse_down = False

        print("RIGHT MOUSE UP")


# =========================================================
# MAIN LOOP
# =========================================================

try:

    while True:

        line = arduino.readline().decode(
            errors="ignore"
        ).strip()

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

            left_button = values["LEFT"]
            right_button = values["RIGHT"]
            top_button = values["TOP"]
            bottom_button = values["BOTTOM"]
            stick_button = values["STICK"]

        except:
            continue


        # =================================================
        # JOYSTICK -> WASD
        #
        # Your joystick orientation:
        #
        # DOWN  = W
        # LEFT  = A
        # UP    = S
        # RIGHT = D
        # =================================================

        move_left = (
            x < CENTER_X - DEADZONE
        )

        move_right = (
            x > CENTER_X + DEADZONE
        )

        move_down_physical = (
            y > CENTER_Y + DEADZONE
        )

        move_up_physical = (
            y < CENTER_Y - DEADZONE
        )


        set_key(
            "a",
            move_left
        )

        set_key(
            "d",
            move_right
        )

        set_key(
            "w",
            move_down_physical
        )

        set_key(
            "s",
            move_up_physical
        )


        # =================================================
        # BUTTONS
        # =================================================

        # Top yellow button = jump

        set_key(
            "space",
            top_button == 1
        )


        # Bottom yellow button = E

        set_key(
            "e",
            bottom_button == 1
        )


        # Joystick press = sprint

        set_key(
            "shift",
            stick_button == 1
        )


        # Left blue button = attack

        set_left_mouse(
            left_button == 1
        )


        # Right blue button = use/place

        set_right_mouse(
            right_button == 1
        )


except KeyboardInterrupt:

    print()
    print("Stopping controller...")


finally:

    # Release keyboard keys

    for key in list(held_keys):

        pydirectinput.keyUp(key)


    # Release mouse buttons

    pydirectinput.mouseUp(
        button="left"
    )

    pydirectinput.mouseUp(
        button="right"
    )


    arduino.close()

    print("Controller stopped.")