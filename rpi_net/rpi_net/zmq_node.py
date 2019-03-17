from itertools import chain
from pprint import pprint

import asyncio
import zmq

class ZMQNode():
    """
    ZMQ Node Handling all updates going out over ZMQ
    """
    def __init__(self, main_server):
        self.main_server = main_server
        self.subscribers = []
        self.subscriptions = []
        self.poller = zmq.Poller()

        ctx = zmq.Context()

        # Iterate over all subscriptions to get data from - Add to Poller
        for subscription in main_server.config["subscriptions"]:
            s = ctx.socket(zmq.SUB)
            s.setsockopt_string(zmq.SUBSCRIBE, "")
            s.connect(f"tcp://{subscription['ip']}:{subscription['port']}")
            self.subscriptions.append(s)
            self.poller.register(s, zmq.POLLIN)

        # Iterate over all subscribers to publish data too - Add to Poller
        for subscriber in main_server.config["subscribers"]:
            s = ctx.socket(zmq.PUB)
            s.bind(f"tcp://{subscriber['ip']}:{subscriber['port']}")
            self.subscribers.append(s)
            self.poller.register(s, zmq.POLLIN)


    async def run(self):
        """
        Task that handles Pi-Layer updates over ZMQ and state synchronization
        """
        while True:
            await asyncio.sleep(0)
            # See if any sockets have anything
            try:
                socks, events = self.poller.poll(1000)
                for sock, event in zip(socks,events):
                    if sock in self.subscriptions:
                        states = sock.recv_json()
                        await self.main_server.sync_states(states)

            # Nothing to report - Poller did not find any sockets with updates
            except ValueError:
                pass
            # Exiting
            except KeyboardInterrupt:
                break

    async def publish(self):
        """
        Publishes updates the A-Layer to the rest of the Wifi-Layer
        """
        for sock in self.subscribers:
            sock.send_json(self.main_server.state)
            await asyncio.sleep(0)
