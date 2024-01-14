import pytest
import subprocess
import time
import redis
import pathlib


@pytest.fixture(autouse=True, scope="session")
def redis_server():
    server_entrypoint = pathlib.Path().parent.parent.resolve() / "server.py"
    # Start the Redis server
    redis_process = subprocess.Popen(["python", server_entrypoint])
    time.sleep(1)  # Allow some time for the server to start
    yield
    redis_process.terminate()


@pytest.fixture(scope='module')
def redis_client():
    # Connect to the Redis server
    return redis.Redis(host='localhost', port=6379, db=0)
