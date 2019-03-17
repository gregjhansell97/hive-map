import json

from pprint import pprint

import aiohttp_cors

from aiohttp import web
from radio_node import RadioNode
from zmq_node import ZMQNode


class MainServer():
    """
    Simple HTTP Server to handle information requests from the frontend
    
    """
    def __init__(self, host:str="*", port:str="8080", loop=None):
        """
        Creates the Main Server that collects updates from zmq task and handles
        http GET requests.

        Args:
            host: Host IP Address
            port: Server Port Number
            loop: Asyncio Event Loop to run on

        """
        self.host = host
        self.port = port
        self.loop = loop
        with open("./config.json", "r") as f:
            self.config = json.load(f)
        self.state = self.config['state']

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
        self.app.add_routes([web.get('/full_update', self.route_full_map)])

        # https://github.com/aio-libs/aiohttp-cors/issues/151
        for resource in list(self.app.router.resources()):
            cors.add(resource)
        self.app["tasks"] = {}

        # Add background tasks to listen for state updates
        self.add_async_task("r_node", self.r_node.run_stubbed)
        self.add_async_task("z_node", self.z_node.run)

        print("Web Server: Setup")

    async def sync_states(self, new_state:dict):
        """
        Sets the overall state of the system when R-Pi sharing

        Args:
            new_state: Full State Update

        """
        self.state = new_state

    async def set_room_state(self, room_state:str):
        '''
        sets the state of one specific room

        Args:
            room_state: state changes for room where one field in the room id

        '''
        room_id = list(room_state.keys())[0]
        for i,room in enumerate(self.state["rooms"]):
            if int(room["name"]) == room_id:
                self.state["rooms"][i]["dynamic_props"] = room_state[room_id]["dynamic_props"]
                await self.z_node.publish()

    async def route_full_map(self, request):
        """
        Sends the full hivemap to the frontend

        Args:
            request: Typically a dictionary containing request parameters

        """
        return web.Response(text=json.dumps(self.state))

    def add_async_task(self, name:str, coro, kwargs:dict={}):
        """
        Adds asyncio tasks to the server

        Args:
            name: Keyword name for the task.
            coro: Coroutine function reference to run
            kwargs: Arguments for the function

        Notes:
            Keyword must be unique or else the existing pointer will be overwritten

        """
        self.app["tasks"][name] = self.loop.create_task(coro(**kwargs))

    async def remove_async_task(self, name:str):
        """
        Removes asyncio task from the Server

        Args:
            name: Keyword name of the task to cancel

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
