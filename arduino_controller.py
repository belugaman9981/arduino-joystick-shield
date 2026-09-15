import serial
import time

PORT = "COM3"   # CHANGE THIS
BAUD = 9600

print(f"Opening {PORT}...")

arduino = serial.Serial(PORT, BAUD, timeout=1)

# Arduino often resets when serial opens
time.sleep(2)

print("Connected.")
print("Waiting for Arduino data... Press Ctrl+C to stop.\n")

try:
    while True:
        data = arduino.readline()

        if data:
            print(data.decode(errors="ignore").strip())
        else:
            print("No data received...")

except KeyboardInterrupt:
    print("\nStopped.")

finally:
    arduino.close()