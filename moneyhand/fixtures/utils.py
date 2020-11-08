import socket
import uuid

import docker
import pytest


@pytest.fixture(scope="session")
def session_id():
    return str(uuid.uuid4().hex)


@pytest.fixture(scope="session")
def unused_port():
    def get(type_="TCP"):
        conntypes = {"TCP": socket.SOCK_STREAM, "UDP": socket.SOCK_DGRAM}
        s = socket.socket(socket.AF_INET, conntypes[type_])
        s.bind(("", 0))
        port = s.getsockname()[1]
        s.close()
        return port

    return get


@pytest.fixture(scope="session")
def docker_client():
    return docker.from_env()
