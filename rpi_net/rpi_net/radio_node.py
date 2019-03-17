import asyncio

from random import randint

class RadioNode():
    def __init__(self, main_server):
        self.main_server = main_server

        self.json_map = 
        {
            "c" : "occupied",
            "n" : "noiseLevel"
        }

    async def run(self):
        while True:
            pass
            # Listens for updates on radio
            # self.main_server.set_room_state(states)

            A_layer_json = {"r" : randint(1,5), "c": randint(1,5), "n": randint(1,5)}

            if "r" in A_layer_json.keys():
                dynamic_props = {}

                for A_layer_keyname in self.json_map.keys():
                    if A_layer_keyname in A_layer_json.keys():
                        dynamic_props[self.json_map[A_layer_keyname]] = A_layer_json[A_layer_keyname]

                state = {
                        A_layer_json[r]:
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
