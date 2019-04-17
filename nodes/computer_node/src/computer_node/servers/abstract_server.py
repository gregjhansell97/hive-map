from abc import ABC, abstractmethod
import asyncio

class AbstractServer(ABC):
    """
    The base class that acts as a server that can handle additional tasks

    Attributes:
        host(str): server host (likely an ip address)
        port(int): port the requests are made on
        loop(asyncio.EventLoop): used to create tasks
    """

    def __init__(
        self,
        host:str="*",
        port:str=8080,
        loop=None,
        coroutines=[]):
        """
        """
        self.host = host
        self.port = port
        self.loop = loop
        for n, c in coroutines:
            self.add_task(n, self.loop.create_task(c))

    @abstractmethod
    def add_task(self, name:str, task):
        """
        Adds asyncio task to the server

        Args:
            name(str): keyword name for task (must be unique)
            task(asyncio.Task): task being added
        """
        pass

    @abstractmethod
    def run(self):
        """
        Starts running the server
        """
        pass
