# -*- coding: utf-8 -*-

# external modules
import asyncio
import random

# internal modules
from computer_node.comms.abstract_comm import AbstractComm
from computer_node.hive_map import HiveMsg

class SimulatedComm(AbstractComm):
    """
    Communication line that generates random id messages to demo parts of the
    system that otherwise would be unavailable until hardware caught up.

    Attributes:
        nodes([int]): list of node ids that generate random messages
    """
    def __init__(self, nodes=[]):
        super().__init__()
        self.nodes = nodes # list of node id's to simulate

    async def listen(self):
        """
        Injects messages into message queue so there are messages available
        """
        while True:
            await asyncio.sleep(1) #picks a random node to send message
            try:
                if self.nodes:
                    msg = HiveMsg(
                        node_id=random.choice(self.nodes),
                        is_occupied=random.choice([True, False])
                    )
                    await self.add_msg(msg)
            except KeyboardInterrupt:
                # exits on ctrl-c
                return


    async def publish(self, msg:str):
        """
        Overrides AbstractComm.publish, doesn't really do anything right now
        """
        pass # doesn't need to do anything at the moment
