import asyncio

class RadioNode():
    def __init__(self, main_server):
        self.main_server = main_server

    async def run(self):
        while True:
            pass
            # Listens for updates on radio
            # self.main_server.set_states(states)
