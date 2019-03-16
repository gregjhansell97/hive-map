import asyncio
from server import MainServer

def main():
    """
    Creates the Event Loop, Start the Server and Messaging Networks, and runs forver
    """
    loop = asyncio.get_event_loop()

    # Start the aiohttp server
    main_server = MainServer(loop=loop)
    main_server.setup()

    # Run Forever
    try:
        print("Completed all startup tasks")
        main_server.run()
    except KeyboardInterrupt as e:
        print("Recieved an interrupt")
        loop.run_until_complete(loop.shutdown_asyncgens())
        print("Shutdown all generators/tasks")
    finally:
        loop.close()


if __name__ == "__main__":
    main()
