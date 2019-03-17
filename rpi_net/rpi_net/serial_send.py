import serial
ser = serial.Serial("/dev/tty.usbserial", 9600)
while True:
    print(ser.readline())
