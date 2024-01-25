import asyncio
import logging

from arg_parser import parse_arguments
from request_handler import process_request

logger = logging.getLogger(__name__)

args = parse_arguments()

HOST = args.host
PORT = args.port


async def handle_client(reader, writer):
    while True:
        data = await reader.read(1024)
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
