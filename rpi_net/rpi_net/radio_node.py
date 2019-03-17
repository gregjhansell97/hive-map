import asyncio
import json

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
        self.connect_serial()

    def connect_serial(self):
        '''
        Attempts to make a serial connection to an arduino with a radio comm unit
        '''
        ports = list(list_ports.comports())
        self.ser = None
        # Searches for Arduino name on Windows Systems
        for p in ports:
            if "Arduino" in p.description:
                self.ser = serial.Serial(p.device, 9600)
                break
        # Probably not connected or it's running a real OS
        if self.ser is None:
            if ports:
                self.ser = serial.Serial(ports[0].device, 9600)

    async def run(self):
        while True:
            await asyncio.sleep(0.1)

            if self.ser is not None:
                line = self.ser.readline()
                try:
                    A_layer_json = json.loads(line)
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
                except (AttributeError, KeyError, UnicodeDecodeError, json.decoder.JSONDecodeError):
                    pass


    async def run_stubbed(self):
        while True:
            await asyncio.sleep(0.1)
            fakeState = {23: {
                "dynamic_props":{
                    "occupied" : randint(0,1)}
                }
            }
            await self.main_server.set_room_state(fakeState)
