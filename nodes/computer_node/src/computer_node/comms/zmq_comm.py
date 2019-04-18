
import asyncio
import zmq

from computer_node.comms.abstract_comm import AbstractComm



class ZMQComm(AbstractComm):
    """
    Communication line that handles pub-sub communication offered by zmq

    Attributes:
    """

    def __init__(
        self,
        host="127.0.0.1",
        port=5000,
        neighbors=[]):

        super().__init__()

        self.context = zmq.Context()

        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind(f"tcp://{host}:{port}")

        self.neighbors = []

        self.poller = zmq.Poller()
        for n in neighbors:
            self.add_neighbor(**n)

    def add_neighbor(self, host="127.0.0.1", port=5000):
        nbr = self.context.socket(zmq.SUB)
        nbr.setsockopt_string(zmq.SUBSCRIBE, "")
        nbr.connect(f"tcp://{host}:{port}")
        self.neighbors.append(nbr)
        self.poller.register(nbr, zmq.POLLIN)

    async def listen(self):
        """
        Task that listens for zmq messages from subscriptions
        """
        while True:
            await asyncio.sleep(0) # allow other tasks to run
            try:
                # poll for 1 second and collect all messages
                for nbr in self.neighbors:
                    await asyncio.sleep(0)
                    try:
                        msg = nbr.recv_pyobj(flags=zmq.NOBLOCK)
                        await self.add_msg(msg)
                    except zmq.ZMQError:
                        pass
            except KeyboardInterrupt:
                # exits on ctrl-c
                return

    async def publish(self, msg):
        """
        Publishes messages out to all subscribers

        Args:
            msg(dict): dictionary of message
        """
        #print(msg)
        #print(self.publishers)
        #print("publishing")
        try:
            self.publisher.send_pyobj(msg)
        except zmq.ZMQError:
            print("ZMQ Error")
        await asyncio.sleep(0) # allow other tasks to run
