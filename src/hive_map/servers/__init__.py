# -*- coding: utf-8 -*-
"""
This module provides server classes that are used to serve data to clients
whether via http, https, tcp, udp, or ipc!
"""

# internal modules
from computer_node.servers.http_server import HTTPServer

__all__ = [
    "HTTPServer"
]
