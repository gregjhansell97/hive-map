# -*- coding: utf-8 -*-
"""
This module provides the lines of communication that are used in hive map. Each
line of communication sends and recieves messages.
"""

# internal modules
from computer_node.comms.serial_comm import SerialComm
from computer_node.comms.simulated_comm import SimulatedComm
from computer_node.comms.zmq_comm import ZMQComm

__all__ = ["SerialComm", "SimulatedComm", "ZMQComm"]
