
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
        subscribers=[],
        subscriptions=[]):

        super().__init__()
        self.subscribers = subscribers
        self.subscriptions = subscriptions
        self.poller = zmq.Poller()

        context = zmq.Context()

        # sets up subscriptions and adds them to the poller
        for ip, port in self.subscriptions:
            s = context.socket(zmq.SUB)
            s.setsockopt_string(smq.SUBSCRIBE, "")
            s.connect(f"tcp://{ip}:{port}")
            self.poller.register(s, zmq.POLLIN)

        # sets up subscribers and adds them to the poller
        for ip, port in self.subscribers:
            s = context.socket(zmq.PUB)
            s.connect(f"tcp://{ip}:{port}")
            self.poller.register(s, zmq.POLLIN) # should this be here?

    async def listen(self):
        """
        Task that listens for zmq messages from subscriptions
        """
        while True:
            await asyncio.sleep(1) # allow other tasks to run

            try:
                # poll for 1 second and collect all messages
                socks, events = self.poller.poll(1000)
                for s, e in zip(socks, events):
                    if s in self.subscriptions:
                        msg = s.recv_pyobj()
                        await self.add_msg(msg)
            except ValueError:
                pass
            except zmq.ZMQError:
                print("ZMQ ERROR")
            except KeyboardInterrupt:
                # exits on ctrl-c
                return

    async def publish(self, msg):
        """
        Publishes messages out to all subscribers

        Args:
            msg(dict): dictionary of message
        """
        print(msg)
        for s in self.subscribers:
            s.send(msg)
            await asyncio.sleep(0) # allow other tasks to run
