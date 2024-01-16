import asyncio
from resp.parsers import serialize
from commands import handle_request
from exceptions import RedisServerException
import logging

logger = logging.getLogger(__name__)


HOST = "127.0.0.1"
PORT = 6379


def _encode_response(response: list) -> bytes:
    return serialize(response).encode("utf-8")

def _encode_error_response(error) -> bytes:
    return serialize([error], is_error=True).encode("utf-8")


async def handle_client(reader, writer):
    while True:
        data = await reader.read(1024)
        print(f"received data {data}")
        if not data:
            break
        try:
            response = handle_request(data)
        except RedisServerException as exc:
            logger.exception("Redis exception - %s", exc)
            response = _encode_error_response(str(exc))
        else:
            response = _encode_response(response)
        writer.write(response)
        await writer.drain()
    
    writer.close()


async def main():
    # Create a server and start listening on a specific address and port
    server = await asyncio.start_server(handle_client, HOST, PORT)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'[INFO] Server listening on {addrs}')

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
