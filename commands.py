from resp.parsers import deserialize


def parse_request(request: bytes) -> str:
    return deserialize(request.decode("utf-8"))


def handle_request(data: bytes) -> list:
    command, *arguments = parse_request(request=data)
    if command == "PING":
        return ["PONG"]
    if command == "ECHO":
        return arguments
    if command.upper() == "GET":
        return handle_get(arguments[0])
    if command.upper() == "SET":
        return handle_set(arguments[0], arguments[1])
    raise ValueError(f"Unknown command {command}")


store = {}


def handle_get(key: str) -> str | None:
    return store.get(key)


def handle_set(key: str, value: str) -> str:
    "Set key to hold the string value. If key already holds a value, it is overwritten, regardless of its type."
    store[key] = str(value)
    return "OK"
