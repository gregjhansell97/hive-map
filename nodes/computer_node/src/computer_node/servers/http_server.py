
from aiohttp import web
import aiohttp_cors
import json

from computer_node.servers.abstract_server import AbstractServer

class HTTPServer(AbstractServer):
    """
    Servers up information regarding the state of the node (computer_node.HiveMap)

    Attributes:

    """
    def __init__(self, hive_map=None, **kwargs):
        self.app = web.Application()
        self.app["tasks"] = {}
        super().__init__(**kwargs)

        self.hive_map = hive_map
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
        self.app["tasks"] = {}

    def add_task(self, name:str, task):
        self.app["tasks"][name] = task

    def run(self):
        web.run_app(self.app, host=self.host, port=self.port)

    def add_routes(self):
        routes = [
            web.get("/get_hive_map", self.route_hive_map)
        ]
        self.app.add_routes(routes)

    async def route_hive_map(self, request):
        """
        Sends full state to requestor

        Args:
            request(dict); dictionary containing request parameters
        """
        return web.Response(text=json.dumps(self.hive_map.state))
