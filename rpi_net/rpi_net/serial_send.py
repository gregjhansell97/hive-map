import serial

import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())
print("---------- available serial ports ---------- ")
for p in ports:
    print(p)
print("-------------------------------------------- ")

ser = None
for p in ports:
	if "Arduino" in p.description:
		print("opening port")
		print(p.device)
		ser = serial.Serial(p.device, 9600)
		break
if ser == None:
	raise Exception("No Arduino found!")

while True:
    print(ser.readline())
