import asyncio

from random import randint
from nrf24 import NRF24
import json

class RadioNode():
    def __init__(self, main_server):
        self.main_server = main_server

        self.json_map = {
            "c" : "occupied",
            "n" : "noiseLevel"
        }

        self.radio = NRF24()
        self.radio.begin(1, 0, "P8_23", "P8_24")
        radio.setRetries(15,15)

        radio.setPayloadSize(8)
        radio.setChannel(0x60)
        radio.setDataRate(NRF24.BR_250KBPS)
        radio.setPALevel(NRF24.PA_MAX)

        radio.setAutoAck(1)

        radio.openWritingPipe(pipes[0])
        radio.openReadingPipe(1, pipes[1])

        radio.startListening()
        radio.stopListening()

        radio.printDetails()

        radio.startListening()

    async def run(self):
        while True:
            #await asyncio.sleep(1)
            
            # Listens for updates on radio
            # self.main_server.set_room_state(states)

            pipe = [0]
            while not self.radio.available(pipe, True):
                await asyncio.sleep(1000/1000000.0)

            recv_buffer = []
            radio.read(recv_buffer)

            print(recv_buffer)


            A_layer_json = json.loads(recv_buffer)

            #A_layer_json = {"r" : 1, "c": randint(1,5), "n": randint(1,5)}

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
    		await asyncio.sleep(1)
    		fakeState = {randint(1,5): {
                "dynamic_props":{
                    "occupied" : randint(0,1)}
                }
            }
    		await self.main_server.set_room_state(fakeState)
