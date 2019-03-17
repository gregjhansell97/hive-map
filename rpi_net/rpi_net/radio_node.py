import asyncio

from random import randint

import serial
from serial.tools import list_ports

class RadioNode():
    def __init__(self, main_server):
        self.main_server = main_server

        self.json_map = {
            "c" : "occupied",
            "n" : "noiseLevel"
        }

    async def run(self):
        while True:
            await asyncio.sleep(0.1)

            ports = list(list_ports.comports())
            ser = None
            for p in ports:
                if "Arduino" in p.description:
                    ser = serial.Serial(p.device, 9600)
                    break
            if ser == None:
                if ports:
                    ser == serial.Serial(ports[0].device, 9600)
            if ser is not None:
                A_layer_json = ser.readline()
                print(A_layer_json)
                if "r" in A_layer_json.keys():
                    dynamic_props = {}

                    for A_layer_keyname in self.json_map.keys():
                        if A_layer_keyname in A_layer_json.keys():
                            dynamic_props[self.json_map[A_layer_keyname]] = A_layer_json[A_layer_keyname]

                    state = {
                            A_layer_json['r']:
                                {
                                "dynamic_props": dynamic_props
                                }
                        }
                    await self.main_server.set_room_state(state)



    async def run_stubbed(self):
        while True:
            await asyncio.sleep(0.1)
            fakeState = {randint(1,5): {
                "dynamic_props":{
                    "occupied" : randint(0,1)}
                }
            }
            await self.main_server.set_room_state(fakeState)
