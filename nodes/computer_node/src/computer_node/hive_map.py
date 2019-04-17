
import asyncio
import datetime
import struct

class HiveMsg:
    """
    Standard message recieved and sent by the node

    Attributes:
        node_id(integer): id of sender
        level(integer): level of sender in node hierarchy
        is_occupied(bool): whether or not node is detecting occupancy
        timestamp(int): when the message was created
    """
    format = "@IB?"
    def __init__(
        self,
        raw_msg=None,
        node_id=None,
        level=None,
        is_occupied=None):
        """
        Args:
            raw_msg(str): byte string that gets initialized to a node message
        """
        if raw_msg is not None:
            node_id, level, is_occupied = HiveMsg.unpack(raw_msg)
        self.node_id = node_id
        self.level = level
        self.is_occupied = is_occupied
        self.timestamp = datetime.datetime.now().timestamp()

    def __str__(self):
        return f"{self.node_id}: {self.is_occupied}, {self.timestamp}"

    @classmethod
    def unpack(class_, msg):
        return struct.unpack(class_.format, msg)

    @classmethod
    def size(class_):
        return struct.calcsize(class_.format)


class HiveMap:
    """
    Keeps track of the state based on comm line messages

    Attributes:
        state(dict): the state of all the subnodes
        comm_lines([AbstractComm]): list of comm lines that the node obtains and
            sends messages with
    """
    def __init__(self, comm_lines=[]):
        self.state = {}
        self.comm_lines = comm_lines

    async def spin(self):
        """
        gets messages from the comm_lines and updates the state accordingly, it
        then publishes all the messages that caused a change in state
        """
        #TODO: add decorator to do this
        while True:
            await asyncio.sleep(1) #looks for messages every second
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
                    # node id doesn't exist, create it
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

    async def publish(self, msg):
        """
        Publishes a message to all the comm lines available

        Args:
            msg(HiveMsg): node message being published through all comm lines
        """
        for comm in self.comm_lines:
            await comm.publish(msg)
