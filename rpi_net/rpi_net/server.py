import json
import aiohttp_cors

from aiohttp import web
from radio_node import RadioNode
from zmq_node import ZMQNode


class MainServer():
    """
    Simple HTTP Server to handle information requests from the frontend
    """

    state = {}

    def __init__(self, host="127.0.0.0", port="8080", loop=None):
        """
        Creates the Main Server that collects updates from zmq task and handles
        http GET requests.
        :param host: Host IP Address
        :param port: Server Port Number
        :param loop: Asyncio Event Loop to run on
        """
        self.host = host
        self.port = port
        self.loop = loop

    def setup(self):
        """
        Sets up the web application function routes
        """
        self.app = web.Application()
        self.z_node = ZMQNode(self)
        self.r_node = RadioNode(self)
        # Setup for cross referencing objects over the web
        cors = aiohttp_cors.setup(self.app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                )
        })
        self.app.add_routes([web.get('/full_update', self.send_full_map)])

        # https://github.com/aio-libs/aiohttp-cors/issues/151
        for resource in list(self.app.router.resources()):
            cors.add(resource)
        self.app["tasks"] = {}

        print("Web Server: Setup")

    async def sync_states(self, new_state):
        # set's state changes
        pass

    async def set_state(self, state):
        # set's state changes
        #invoke z_node publish
        pass

    async def send_full_map(self, request):
        """
        Sends the full hivemap to the frontend
        """
        return web.Response(text=json.dumps(state))

    def add_async_task(self, name, fn, kwargs={}):
        """
        Adds asyncio tasks to the server
        :param name: Keyword name for the task.
        :param fn: Function reference to run
        :param kwargs: Arguments for the function
        :notes: Keyword must be unique or else the existing pointer will be overwritten
        """
        self.app["tasks"][name] = self.loop.create_task(fn(**kwargs))

    async def remove_async_task(self, name):
        """
        Removes asyncio task from the Server
        :param name: Keyword name of the task to cancel
        """
        self.app["tasks"][name].cancel()
        await app["tasks"][name]

    async def remove_all_async_tasks(self):
        """
        Iterates over all the tasks and cancels them
        """
        for name in self.app["tasks"]:
            await self.remove_async_task(name)

    def run(self):
        """
        Starts running the app
        """
        print("Web Server: Running")
        web.run_app(self.app)
