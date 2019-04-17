
import asyncio
import random

from computer_node.comms.abstract_comm import AbstractComm
from computer_node.hive_map import HiveMsg

class SimulatedComm(AbstractComm):
    """
    """
    def __init__(self, node_ids=[]):
        super().__init__()
        self.node_ids = node_ids # list of node id's to simulate
        #@loop(delay) decorator?
    async def listen(self):
        """
        Injects messages into message queue so there are messages available
        """
        while True:
            await asyncio.sleep(1) #picks a random node to send message
            try:
                if self.node_ids:
                    msg = HiveMsg(
                        node_id=random.choice(self.node_ids),
                        level=1,
                        is_occupied=random.choice([True, False])
                    )
                    await self.add_msg(msg)
            except KeyboardInterrupt:
                # exits on ctrl-c
                return


    async def publish(self, msg:str):
        """
        Doesn't really do anything right now
        """
        pass # doesn't need to do anything at the moment
