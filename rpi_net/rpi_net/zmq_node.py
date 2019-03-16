import asyncio
import zmq
import zmq.asyncio as zmqio

async def test(time=1):
    while True:
        print("Hello")
        await asyncio.sleep(time)

class ZMQNode():
    def __init__(self, main_server):
        self.main_server = main_server

    async def run(self):
        while True:
            pass
            # Listens for updates - states
            # self.main_server.sync_states(states)
