import serial

from serial.tools import list_ports

ports = list(list_ports.comports())
print("---------- available serial ports ---------- ")
for p in ports:
    print(p)
print("-------------------------------------------- ")

ports = list(list_ports.comports())
ser = None
for p in ports:
    if "Arduino" in p.description:
        ser = serial.Serial(p.device, 9600)
        break
if ser is None:
    if ports:
        ser = serial.Serial(ports[0].device, 9600)

while True:
    if ser is not None:
        A_layer_json = ser.readline()
        print(str(A_layer_json))
