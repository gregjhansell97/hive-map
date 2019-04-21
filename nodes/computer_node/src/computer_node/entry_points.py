# -*- coding: utf-8 -*-
"""
All none private functions in ths module are tied to command line calls that can
be used once this module is installed. These entry points rely on a config file
located in the top level directory of computer_node
"""

# external modules
import asyncio
import os
import sys
import yaml

# internal modules
from computer_node.comms import SerialComm, SimulatedComm, ZMQComm
from computer_node.servers import HTTPServer

computer_node_dir = f"{os.environ['VIRTUAL_ENV']}/../nodes/computer_node/"
"""
(str): The top level directory of the computer_node
"""

config = yaml.safe_load(open(f"{computer_node_dir}/config.yaml"))
"""
(dict): the configuration information extracted from the yaml file
"""

def run_computer_node():
    """
    Creates the event loop, creates the state node, initializes all comm lines,
    and starts the server
    """
    loop = asyncio.get_event_loop()

    # lines of communication that send and receive messages
    comm_lines = [
        SimulatedComm(**config["sim_comm_line"]),
        ZMQComm(**config["zmq_comm_line"]),
        SerialComm(**config["serial_comm_line"])
    ]

    # provieds http requests
    server = HTTPServer(
        comm_lines=comm_lines,
        loop=loop,
        **config["http_server"]
    )
    server.run() # runs all the coroutines and starts server

if __name__ == "__main__":
    run_server()
