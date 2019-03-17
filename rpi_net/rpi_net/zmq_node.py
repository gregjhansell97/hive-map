from itertools import chain
from pprint import pprint

import asyncio
import zmq
import zmq.asyncio as zmqio

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
        # Iterate over all subscriptions to get data from
        for subscription in main_server.config["subscriptions"]:
            s = ctx.socket(zmq.SUB)
            s.connect(f"tcp://{subscription['ip']}:{subscription['port']}")
            self.subscriptions.append(s)

            # TODO: Add in support for topical filtering
            # if not subscription["topics"]:
            #     s.setsockopt_string(zmq.SUBSCRIBE, "")
            # else:
            #     for t in subscription["topics"]:
            #         s.setsockopt_string(zmq.SUBSCRIBE, t)

        # Iterate over all subscribers to publish data too
        for subscriber in main_server.config["subscribers"]:
            s = ctx.socket(zmq.PUB)
            s.connect(f"tcp://{subscriber['ip']}:{subscriber['port']}")
            self.subscribers.append(s)

        for sock in chain(self.subscribers, self.subscriptions):
            self.poller.register(sock, zmq.POLLIN)


    async def run(self):
        while True:
            await asyncio.sleep(0.1)
            # See if any sockets have anything
            try:
                socks, events = self.poller.poll()
                for sock, event in zip(socks,events):
                    if sock in self.subscriptions:
                        states = sock.recv_json()
                        self.main_server.sync_states(states)

            # Nothing to report sir
            except ValueError:
                pass
            # Exiting
            except KeyboardInterrupt:
                break

    async def publish(self):
        """
        Publishes updates the A-Layer to the rest of the Wifi-Layer
        """
        await asyncio.sleep(0.1)
        print(self.subscribers)
        for sock in self.subscribers:
            print('try')
            sock.send_json(self.main_server.state)
            await asyncio.sleep(0.1)
            print("send")
