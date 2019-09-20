# -*- coding: utf-8 -*-

# external modules
import asyncio
from collections import namedtuple
import serial
from serial.tools import list_ports
import struct

# internal modules
from computer_node.comms.abstract_comm import AbstractComm
from computer_node.hive_map import HiveMsg

class SerialComm(AbstractComm):
    """
    Communication line that handles communication with a computer proxy node
    connected to the laptop serially

    Attributes:
        baud_rate(int): the bit rate the serial communication has
        computer_proxy_node(serial.Serial): serial communication line to the
            computer proxy node
        msg_size(int): size of message coming from computer proxy node
    """
    def __init__(self, plugged_in:bool=True, baud_rate:int=9600):
        """
        Args:
            plugged_in(bool): if the computer proxy node is plugged in to the
                computer (future iterations will give the exact port)
            baud_rate(int); the bit rate the serial communication has
        """
        super().__init__()
        self.baud_rate = baud_rate
        self.computer_proxy_node = None
        self.msg_size = HiveMsg.size()
        if plugged_in:
            self.connect_computer_proxy_node()

    def connect_computer_proxy_node(self):
        """
        Attempts to make a serial connection to a computer proxy node plugged
        into the computer. If successful, computer_proxy_node is no longer None
        """
        ports = list(list_ports.comports())

        # searches for aruino name on windows system
        for p in ports:
            if "Arduino" in p.description:
                device = p.device
                self.computer_proxy_node = serial.Serial(device, self.baud_rate)
                break

        # "probably not connected or it's running a real OS" - Chris
        if self.computer_proxy_node is None and ports:
            device = ports[0].device
            self.computer_proxy_node = serial.Serial(device, self.baud_rate)
        if self.computer_proxy_node:
            print("computer proxy node connected")
        else:
            print("computer proxy node not connected")

    async def listen(self):
        """
        Task which collects messages from the computer_proxy_node and puts them
        on the message_queue
        """
        while True:
            await asyncio.sleep(0)
            try:
                if self.computer_proxy_node is not None:
                    # should do checks that make is modulus size (otherwise
                    # smash the buffer)
                    # verifies more than 6 bytes waiting
                    if self.computer_proxy_node.in_waiting >= self.msg_size:
                        raw_msg = self.computer_proxy_node.read(self.msg_size)
                        msg = HiveMsg.load(raw_msg=raw_msg)
                        await self.add_msg(msg)
            except KeyboardInterrupt:
                # exits on ctrl-c
                return


    async def publish(self, msg:HiveMsg):
        """
        Task which sends messages back to the computer proxy node connected

        Args:
            msg(HiveMsg): the message being published on comm line
        """
        pass # doesn't need to do anything at the moment
