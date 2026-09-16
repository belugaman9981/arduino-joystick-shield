import serial
import time
import pydirectinput

# ==========================================================
# SETTINGS
# ==========================================================

PORT = "COM11"
BAUD = 9600

# Larger = joystick must move farther before activating
MOVEMENT_DEADZONE = 70

# Turning deadzone
TURN_DEADZONE = 45

# Higher number = faster camera turning
TURN_SPEED = 18

# Maximum joystick distance from center used for scaling
MAX_AXIS_DISTANCE = 350

pydirectinput.PAUSE = 0


# ==========================================================
# CONNECT TO ARDUINO
# ==========================================================

print("Connecting to Arduino...")

arduino = serial.Serial(
    PORT,
    BAUD,
    timeout=1
)

time.sleep(2)


# ==========================================================
# AUTO CALIBRATION
# ==========================================================

print()
print("===================================")
print("DO NOT TOUCH THE JOYSTICK")
print("Calibrating...")
print("===================================")

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


if not xs or not ys:

    print("ERROR: Arduino joystick data not received.")
    arduino.close()

    input("Press Enter to exit...")

    raise SystemExit


CENTER_X = sum(xs) // len(xs)
CENTER_Y = sum(ys) // len(ys)


print()
print("Calibration finished.")
print("Center X:", CENTER_X)
print("Center Y:", CENTER_Y)

print()
print("CONTROLLER ACTIVE")
print()
print("DOWN  -> MOVE FORWARD")
print("UP    -> MOVE BACKWARD")
print("LEFT  -> TURN LEFT")
print("RIGHT -> TURN RIGHT")
print()
print("TOP YELLOW    -> JUMP")
print("BOTTOM YELLOW -> E")
print("LEFT BLUE     -> LEFT CLICK")
print("RIGHT BLUE    -> RIGHT CLICK")
print("STICK PRESS   -> SHIFT")
print()
print("Ctrl+C to stop.")
print()


# ==========================================================
# KEYBOARD HANDLING
# ==========================================================

held_keys = set()


def key_down(key):

    if key not in held_keys:

        pydirectinput.keyDown(key)

        held_keys.add(key)


def key_up(key):

    if key in held_keys:

        pydirectinput.keyUp(key)

        held_keys.remove(key)


def set_key(key, pressed):

    if pressed:

        key_down(key)

    else:

        key_up(key)


# ==========================================================
# MOUSE BUTTON HANDLING
# ==========================================================

left_mouse_held = False
right_mouse_held = False


def set_left_mouse(pressed):

    global left_mouse_held

    if pressed and not left_mouse_held:

        pydirectinput.mouseDown(
            button="left"
        )

        left_mouse_held = True

    elif not pressed and left_mouse_held:

        pydirectinput.mouseUp(
            button="left"
        )

        left_mouse_held = False


def set_right_mouse(pressed):

    global right_mouse_held

    if pressed and not right_mouse_held:

        pydirectinput.mouseDown(
            button="right"
        )

        right_mouse_held = True

    elif not pressed and right_mouse_held:

        pydirectinput.mouseUp(
            button="right"
        )

        right_mouse_held = False


# ==========================================================
# TURNING
# ==========================================================

def calculate_turn(axis_value):

    difference = axis_value - CENTER_X

    if abs(difference) < TURN_DEADZONE:
        return 0

    direction = 1

    if difference < 0:
        direction = -1

    strength = (
        abs(difference) - TURN_DEADZONE
    )

    strength = strength / MAX_AXIS_DISTANCE

    if strength > 1:
        strength = 1

    turn_amount = int(
        strength * TURN_SPEED
    )

    if turn_amount < 1:
        turn_amount = 1

    return turn_amount * direction


# ==========================================================
# MAIN LOOP
# ==========================================================

try:

    while True:

        line = arduino.readline().decode(
            errors="ignore"
        ).strip()

        if not line:
            continue


        # --------------------------------------------------
        # READ ARDUINO VALUES
        # --------------------------------------------------

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


        # ==================================================
        # FORWARD / BACKWARD
        #
        # YOUR SHIELD:
        #
        # Physical DOWN = W
        # Physical UP   = S
        # ==================================================

        forward = (
            y > CENTER_Y + MOVEMENT_DEADZONE
        )

        backward = (
            y < CENTER_Y - MOVEMENT_DEADZONE
        )


        set_key(
            "w",
            forward
        )

        set_key(
            "s",
            backward
        )


        # ==================================================
        # CAMERA TURNING
        #
        # LEFT / RIGHT on joystick now moves the mouse.
        # ==================================================

        turn_amount = calculate_turn(x)

        if turn_amount != 0:

            pydirectinput.moveRel(
                turn_amount,
                0,
                duration=0
            )


        # ==================================================
        # BUTTONS
        # ==================================================

        # Top yellow = jump
        set_key(
            "space",
            top_button == 1
        )


        # Bottom yellow = E
        set_key(
            "e",
            bottom_button == 1
        )


        # Joystick click = sprint
        set_key(
            "shift",
            stick_button == 1
        )


        # Left blue = attack
        set_left_mouse(
            left_button == 1
        )


        # Right blue = use/place
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
