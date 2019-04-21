# -*- coding: utf-8 -*-

# external modules
import asyncio
import zmq

# internal modules
from computer_node.comms.abstract_comm import AbstractComm

class ZMQComm(AbstractComm):
    """
    Communication line that handles pub-sub communication offered by zmq

    Attributes:
        context(zmq.Context): zmq context used to create sockets
        self.publisher(zmq.Socket): publisher in zmq pub-sub network
        self.neighbors([zmq.Socket]): list of zmq pub-sub subscriptions
    """

    def __init__(
        self,
        host:str="127.0.0.1",
        port:int=5000,
        neighbors:list=[]):
        """
        Args:
            host(str): host name of this comm line
            port(int): port of this comm line
            neighbors([dict]): host and ports of neighboring comm lines
        """
        super().__init__()

        self.context = zmq.Context()

        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind(f"tcp://{host}:{port}")

        self.neighbors = []
        for n in neighbors:
            self.add_neighbor(**n)

    def add_neighbor(self, host="127.0.0.1", port=5000):
        nbr = self.context.socket(zmq.SUB)
        nbr.setsockopt_string(zmq.SUBSCRIBE, "")
        nbr.connect(f"tcp://{host}:{port}")
        self.neighbors.append(nbr)

    async def listen(self):
        """
        Task that listens for zmq messages from subscriptions
        """
        while True:
            await asyncio.sleep(0) # allow other tasks to run
            try:
                for nbr in self.neighbors:
                    await asyncio.sleep(0)
                    try:
                        # non bloccking recieve
                        msg = nbr.recv_pyobj(flags=zmq.NOBLOCK)
                        await self.add_msg(msg)
                    except zmq.ZMQError:
                        pass # no message recieved
            except KeyboardInterrupt:
                # exits on ctrl-c
                return

    async def publish(self, msg):
        """
        Publishes messages out to all subscribers

        Args:
            msg(HiveMsg): message to be published on address
        """
        try:
            self.publisher.send_pyobj(msg)
        except zmq.ZMQError:
            print("ZMQ Error")
        await asyncio.sleep(0) # allow other tasks to run
