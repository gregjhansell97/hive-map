# -*- coding: utf-8 -*-

# external modules
from aiohttp import web
import aiohttp_cors
import json

# internal modules
from computer_node.servers.abstract_server import AbstractServer

class HTTPServer(AbstractServer):
    """
    Servers up http accessable information regarding the state of all the nodes
    in the distributed map

    Attributes:
        self.app(web.Application): the web app that starts the http server
    """
    def __init__(self, **kwargs):
        # creates app first before invoking super constructor because super
        # constructor calls add_task (which needs app)
        self.app = web.Application()
        self.app["tasks"] = {}
        super().__init__(**kwargs)
        self.add_routes()

        # setup for cross referencing objects over the web
        cors = aiohttp_cors.setup(self.app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*"
            )
        })

        # https://github.com/aio-libs/aiohttp-cors/issues/151
        for resource in list(self.app.router.resources()):
            cors.add(resource)

    def add_routes(self):
        """
        Used in constructor to create a routing table that gets added as routes
        """
        routes = [
            web.get("/get_hive_map", self.route_hive_map)
        ]
        self.app.add_routes(routes)


    def add_task(self, name:str, task):
        """
        Overrides AbstractServer.add_task
        """
        self.app["tasks"][name] = task

    def run(self):
        """
        Overrides AbstractServer.run
        """
        web.run_app(self.app, host=self.host, port=self.port)

    async def route_hive_map(self, request):
        """
        Sends full state to requestor

        Args:
            request(dict); dictionary containing request parameters
        """
        return web.Response(text=json.dumps(self.hive_map.state))
