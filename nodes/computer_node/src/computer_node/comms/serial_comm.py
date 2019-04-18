
import asyncio
from collections import namedtuple
import serial
from serial.tools import list_ports
import struct

from computer_node.comms.abstract_comm import AbstractComm
from computer_node.hive_map import HiveMsg

class SerialComm(AbstractComm):
    """
    Communication line that handles communication with radio comm units
    connected to the laptop serially

    Attributes:
        baud_rate(int): the bit rate the serial communication has
        radio_comm_unit(serial.Serial): serial comm line that can talk to radio
            comm unit
        msg_size(int): size of message coming from radio comm unit
    """
    def __init__(self):
        super().__init__()
        self.baud_rate = 9600
        self.radio_comm_unit = None
        self.msg_size = HiveMsg.size()
        self.connect_radio_comm_unit()

    def connect_radio_comm_unit(self):
        """
        Attempts to make a serial connection to a radio comm unit plugged in to
        the computer. If successful, self.radio_comm_module is no longer None
        """
        ports = list(list_ports.comports())

        # searches for aruino name on windows system
        for p in ports:
            if "Arduino" in p.description:
                device = p.device
                self.radio_comm_unit = serial.Serial(device, self.baud_rate)
                break

        # "probably not connected or it's running a real OS" - Chris
        if self.radio_comm_unit is None and ports:
            device = ports[0].device
            self.radio_comm_unit = serial.Serial(device, self.baud_rate)
        if self.radio_comm_unit:
            print("computer proxy node connected")
        else:
            print("computer proxy node not connected")

    async def listen(self):
        """
        Task which collects messages from the radio_comm_unit and puts them on
        the message_queue
        """
        while True:
            await asyncio.sleep(0)
            try:
                if self.radio_comm_unit is not None:
                    # should do checks that make is modulus size (otherwise
                    # smash the buffer)
                    # verifies more than 6 bytes waiting
                    if self.radio_comm_unit.in_waiting >= self.msg_size:
                        raw_msg = self.radio_comm_unit.read(self.msg_size)
                        msg = HiveMsg(raw_msg=raw_msg)
                        await self.add_msg(msg)
            except KeyboardInterrupt:
                # exits on ctrl-c
                return


    async def publish(self, msg:str):
        """
        Task which sends messages back to the radio comm unit connected serially
        """
        pass # doesn't need to do anything at the moment
