import asyncio

import random

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
    		randint(1, 100)
    		fakeState = {"roomID" : randint(1, 5), "occupied" : randint(0,1)}
    		self.main_server.set_room_state(fakeState)