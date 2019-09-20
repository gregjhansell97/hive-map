# -*- coding: utf-8 -*-
"""
This module provide classes that help support a distributed state across
comm lines
"""

# external modules
import asyncio
import datetime
import struct

class HiveMsg:
    """
    Standard message recieved and sent by the HiveMap class

    Attributes:
        node_id(int): id of sender
        is_occupied(bool): whether or not node is detecting occupancy
        timestamp(int): when the message was created
        format(str): class variable specifying struct-parse style of message
    """

    format = "=BI?BB"

    def __init__(
        self,
        node_id:int=None,
        is_occupied:bool=None):
        self.node_id = node_id
        self.is_occupied = is_occupied
        self.timestamp = datetime.datetime.now().timestamp()

    def __str__(self):
        return f"{self.node_id}: {self.is_occupied}, {self.timestamp}"

    @classmethod
    def load(class_, raw_msg:str):
        """
        returns an instance of HiveMsg given raw bytes

        Args:
            raw_msg(str): raw bytes that still need to be parsed

        Returns:
            (HiveMsg): hive message instance based on raw bytes loaded
        """
        data = struct.unpack(class_.format, raw_msg)
        type, node_id, is_occupied, msg_number, distance = data
        return class_(
            node_id=node_id,
            is_occupied=is_occupied
        )

    @classmethod
    def size(class_):
        """
        Returns:
            (int): the size of raw messages
        """
        return struct.calcsize(class_.format)


class HiveMap:
    """
    Distributed state that changes based on messages it recieves on
    communication lines, an state change gets re-added to the communication line

    Attributes:
        state(dict): the state of all the subnodes (ex: rooms, parking spots)
        comm_lines([AbstractComm]): list of comm lines that the node obtains and
            sends messages with
    """
    def __init__(self, comm_lines:list=[]):
        # initially empty state, may want to "pull" information off comm lines
        self.state = {}
        self.comm_lines = comm_lines

    async def spin(self):
        """
        Collects a list of HiveMsgs from all communication lines and updates the
        state accordingly, it then publishes all the messages that caused a
        change in state
        """
        while True:
            await asyncio.sleep(0.3) # looks for messages every second
            try:
                # collects all the messages and puts them in a list called msgs
                msgs = []
                for comm in self.comm_lines:
                    comm_msgs = await comm.get_msgs()
                    msgs.extend(comm_msgs)
                # sort message by oldest message to newest
                msgs.sort(key=lambda m: m.timestamp)

                # goes through messages from oldest to newest
                for m in msgs:
                    # node id doesn't exist in state, create it
                    if m.node_id not in self.state:
                        self.state[m.node_id] = {
                            "timestamp": 0
                        }

                    # message is a newer time stamp, so update state with it
                    if m.timestamp > self.state[m.node_id]["timestamp"]:
                        # make the status dynamic to what the message is
                        self.state[m.node_id]["is_occupied"] = m.is_occupied
                        self.state[m.node_id]["timestamp"] = m.timestamp
                        # we could check if state changes too before publishing
                        await self.publish(m)
            except KeyboardInterrupt:
                # exits on ctrl-c
                return

    async def publish(self, msg:HiveMsg):
        """
        Publishes a message to all the comm lines available

        Args:
            msg(HiveMsg): node message being published through all comm lines
        """
        for comm in self.comm_lines:
            await comm.publish(msg)
