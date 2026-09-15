import serial

PORT = "COM3"   # change this
BAUD = 9600

arduino = serial.Serial(PORT, BAUD, timeout=1)

while True:
    line = arduino.readline().decode(errors="ignore").strip()
    if line:
        print(line)