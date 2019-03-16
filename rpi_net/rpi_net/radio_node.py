import asyncio

from random import randint

class RadioNode():
    def __init__(self, main_server):
        self.main_server = main_server

    async def run(self):
        while True:
            pass
            # Listens for updates on radio
            # self.main_server.set_room_state(states)

    async def run_stubbed(self):
    	while True:
    		await asyncio.sleep(1)
    		fakeState = {randint(1,5): {
                "dynamic_props":{
                    "occupied" : randint(0,1)}
                }
            }
    		await self.main_server.set_room_state(fakeState)
