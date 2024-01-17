import asyncio
from request_handler import process_request
import logging

logger = logging.getLogger(__name__)


HOST = "127.0.0.1"
PORT = 6379


async def handle_client(reader, writer):
    while True:
        data = await reader.read(1024)
        # print(f"received data {data}")
        if not data:
            break
        response = process_request(data)
        writer.write(response)
        await writer.drain()

    writer.close()


async def main():
    # Create a server and start listening on a specific address and port
    server = await asyncio.start_server(handle_client, HOST, PORT)

    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"[INFO] Server listening on {addrs}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
