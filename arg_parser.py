import argparse


def parse_arguments(default_host: str = "127.0.0.1", default_port: int = 65432):
    parser = argparse.ArgumentParser(
        description="Redis server with host and port options."
    )
    parser.add_argument(
        "-H", "--host", type=str, default=default_host, help="Host address"
    )
    parser.add_argument(
        "-p", "--port", type=int, default=default_port, help="Port number"
    )
    return parser.parse_args()
