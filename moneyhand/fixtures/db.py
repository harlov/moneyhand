import time
from typing import Any, Callable, Generator

import pytest
import psycopg2

from moneyhand import config
from moneyhand.adapters.postgresql_storage import helpers


POSTGRESQL_VERSION = "13.0"


def pytest_addoption(parser):
    parser.addoption(
        "--postgres",
        action="store",
        default="",
        help="PostgreSQL URI (e.g. user:pswd@localhost:5432/)",
    )


@pytest.fixture(scope="session")
def db_name(session_id):
    return "test-db-{}".format(session_id)


def wait_server_up(uri):
    retry_counter = 0

    while retry_counter < 60:
        try:
            psycopg2.connect(dsn=f"postgresql://{uri}")
            return
        except psycopg2.OperationalError as e:
            print(e)
            retry_counter += 1
            time.sleep(0.5)
    exit(f"Fail establish connect to postgres with {uri}")


@pytest.fixture(scope="session")
def postgres_uri(
    request: Any, docker_client_factory: Any, unused_port: Callable, db_name: str
) -> Generator[str, None, None]:
    uri = request.config.getoption("postgres")

    if not uri:
        docker_client = docker_client_factory()
        image = f"postgres:{POSTGRESQL_VERSION}"
        if not docker_client.images.list(image):
            docker_client.images.pull(image)
        port = unused_port()
        container = docker_client.containers.create(
            image=image,
            name=db_name,
            ports={"5432/tcp": port},
            command="-c fsync=off",
            environment={"POSTGRES_PASSWORD": "postgres"},
        )
        container.start()
        uri = f"postgres:postgres@127.0.0.1:{port}/"
        wait_server_up(uri)
        yield uri
        container.stop(timeout=10)
        container.remove()
    else:
        yield uri.strip()


@pytest.fixture
def test_db(postgres_uri):
    config.STORAGE_URI = postgres_uri
    helpers.migrate(only_structure=True)
    yield

    conn = psycopg2.connect(dsn=f"postgresql://{postgres_uri}")
    cursor = conn.cursor()
    cursor.execute(
        """
                DROP SCHEMA public CASCADE;
                CREATE SCHEMA public;
                GRANT ALL ON SCHEMA public TO postgres;
                GRANT ALL ON SCHEMA public TO public;
        """
    )

    conn.commit()
    conn.close()
