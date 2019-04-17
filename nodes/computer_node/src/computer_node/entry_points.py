import asyncio

from computer_node.comms import SerialComm, ZMQComm
from computer_node.hive_map import HiveMap
from computer_node.servers import HTTPServer


def run_computer_node():
    """
    Creates the event loop, creates the state node, initializes all comm lines,
    and starts the server
    """
    loop = asyncio.get_event_loop()

    zmq_comm_line = ZMQComm()
    serial_comm_line = SerialComm()

    hive_map = HiveMap(comm_lines=[zmq_comm_line, serial_comm_line])

    server = HTTPServer(
        hive_map=hive_map,
        host="127.0.0.1",
        port=8080,
        loop=loop,
        coroutines=[
           ("hive_map", hive_map.spin()),
           ("serial_comm_line", serial_comm_line.listen())
        ]
    )
    server.run()

if __name__ == "__main__":
    run_server()
