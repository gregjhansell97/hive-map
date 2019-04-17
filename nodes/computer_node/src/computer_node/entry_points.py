import asyncio
import yaml
import os

from computer_node.comms import SerialComm, SimulatedComm, ZMQComm
from computer_node.hive_map import HiveMap
from computer_node.servers import HTTPServer

import sys

def _get_config():
    computer_node_dir = f"{os.environ['VIRTUAL_ENV']}/../nodes/computer_node/"
    config = yaml.safe_load(open(f"{computer_node_dir}/config.yaml"))
    return config

def run_computer_node():
    """
    Creates the event loop, creates the state node, initializes all comm lines,
    and starts the server
    """
    config = _get_config()
    loop = asyncio.get_event_loop()

    coroutines = []
    comm_lines = []
    sim_comm_line = SimulatedComm(config["simulated_nodes"])
    zmq_comm_line = ZMQComm(**config["computer_node"])

    comm_lines.extend([
        sim_comm_line,
        zmq_comm_line
    ])
    # adds serial comm line
    if config["has_computer_proxy_node"]:
        serial_comm_line = SerialComm()
        comm_lines.append(serial_comm_line)
    hive_map = HiveMap(comm_lines=comm_lines)

    # coroutines that are run in the background
    coroutines = [("hive_map", hive_map.spin())]
    coroutines.extend([ (str(cl), cl.listen()) for cl in comm_lines ])

    server = HTTPServer(
        hive_map=hive_map,
        host=config["server"]["host"],
        port=config["server"]["port"],
        loop=loop,
        coroutines=coroutines
    )
    server.run()

if __name__ == "__main__":
    run_server()
