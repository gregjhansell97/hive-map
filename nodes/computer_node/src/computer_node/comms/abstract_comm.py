from abc import ABC, abstractmethod
import asyncio

class AbstractComm(ABC):
    """
    The base class that handles communication lines

    Attributes:
        msg_queue([str]): queue of messages that were recieved
        lock(asyncio.Lock): used when modifiying the message_queue
    """

    def __init__(self):
        self.msg_queue = []
        self.lock = asyncio.Lock()

    async def get_msgs(self):
        """
        Handles the retrival of messages from the message_queue, once data is
        extracted, the message queue is wiped (hence the lock)

        Returns:
            [str]: bytes of the message queue
        """
        async with self.lock:
            msgs = self.msg_queue
            # clears the queue, that's why lock is needed
            self.msg_queue = []
        return msgs

    async def add_msg(self, msg:str):
        """
        Atomic means to add message to the message queue

        Args:
            msg(str): bytes of the message being added
        """
        async with self.lock:
            self.msg_queue.append(msg)

    @abstractmethod
    async def listen(self):
        """
        Listens for information to recieve and adds it to the message_queue
        """
        pass

    @abstractmethod
    async def publish(self, msg:str):
        """
        Publishes information based on message

        Args:
            msg(str): byte string message that needs to be published
        """
        pass
