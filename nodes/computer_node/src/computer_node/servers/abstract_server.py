# -*- coding: utf-8 -*-

# external modules
from abc import ABC, abstractmethod

# internal modules
from computer_node.hive_map import HiveMap

class AbstractServer(ABC):
    """
    The base class that acts as a server that uses communication lines to keep
    track of a distributed state (dictionary) that it then can serve to clients

    Attributes:
        host(str): server host (likely an ip address)
        port(int): port the requests are made on
        hive_map(HiveMap): distributed state that still needs to be started
        loop(asyncio.EventLoop): event loop for asyncio concurrency
    """
    def __init__(
        self,
        host:str="*",
        port:int=8080,
        comm_lines:list=[],
        coroutines:list=[],
        loop=None):
        """
        Args:
            host(str): server host
            port(int): port requests are made on
            comm_lines([comms.AbstractComm]): communication lines to other
                computer nodes, used to update distributed state
            coroutines([Coroutines]): asyncio coroutines that need to be run
        """
        self.host = host
        self.port = port
        self.hive_map = HiveMap(comm_lines=comm_lines)
        self.loop = loop

        # runs background tasks
        for n, c in coroutines:
            self.add_task(n, self.loop.create_task(c))

        # gets comm_lines listening
        for cl in comm_lines:
            self.add_task(str(cl), self.loop.create_task(cl.listen()))

        # starts up hive map
        self.add_task("hive_map", self.loop.create_task(self.hive_map.spin()))

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
        Starts running the server and all background tasks
        """
        pass
