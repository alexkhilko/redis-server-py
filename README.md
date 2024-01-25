# Redis Server in Python

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

This is a simple implementation of a Redis server written in Python.
Inspired by John Crickett Coding Chanllenges https://codingchallenges.fyi/challenges/challenge-redis

## Features

- Basic implementation of Redis server functionality.
- Support for the RESP2 protocol.
- Support for common Redis commands.
- Two server implementations to handle multiple concurrent clients:
  - Classic server using threads (`server.py`).
  - Async server using Python asyncio (`async_server.py`).
- Easy to use and extend.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/alexkhilko/redis-server-py.git
    cd redis-server-py
    ```

2. Install dependencies using [Poetry](https://python-poetry.org/):

    ```bash
    poetry install
    ```

## Usage

### Classic Server (using threads)

1. Run the Redis server:

    ```bash
    python server.py -H localhost -p 6379
    ```

   To run on default host (`localhost`) and port (`6379`), omit the `-H` and `-p` options.

### Async Server (using Python asyncio)

1. Run the Redis server:

    ```bash
    python async_server.py -H localhost -p 6379
    ```

   To run on default host (`localhost`) and port (`6379`), omit the `-H` and `-p` options.

### Interacting with Server
1. Connect to the server using a Redis client.

    ```bash
    # Example using redis-cli
    redis-cli -h localhost -p 6379
    ```

## Supported Commands

- `PING`: Ping the server.
- `ECHO`: Echo the input string.
- `GET`: Get the value of a key.
- `SET`: Set the value of a key.
- `CLIENT`: Various client-related commands.
- `COMMAND`: Get information about Redis commands.
- `EXISTS`: Check if a key exists.
- `DEL`: Delete one or more keys.
- `INCRBY`: Increment the value of a key by a specified amount.
- `INCR`: Increment the value of a key by 1.
- `DECR`: Decrement the value of a key by 1.
- `DECRBY`: Decrement the value of a key by a specified amount.
- `LPUSH`: Add an element to the left end of a list.
- `RPUSH`: Add an element to the right end of a list.
- `SAVE`: Save the dataset to disk.

## Running Tests

To run tests, use [pytest](https://docs.pytest.org/en/stable/):

```bash
pytest
```

## Acknowledgments
The Redis project for inspiration.
John Crickett's coding challenges for sparking the idea behind this project.
