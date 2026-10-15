from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Connection, Engine, create_engine
from sqlalchemy.orm import Session

from app.database import database_url, get_session
from app.main import app


@pytest.fixture(scope="session")
def db_engine() -> Iterator[Engine]:
    test_url = database_url.set(database="aeropulse_test")
    engine = create_engine(url=test_url)
    yield engine
    engine.dispose()


@pytest.fixture()
def db_connection(db_engine: Engine) -> Iterator[Connection]:
    with db_engine.connect() as connection:
        transaction = connection.begin()
        yield connection
        transaction.rollback()


@pytest.fixture()
def db_session(db_connection: Connection) -> Iterator[Session]:
    with Session(
        bind=db_connection, join_transaction_mode="create_savepoint"
    ) as session:
        yield session


@pytest.fixture
def client(db_session: Session) -> Iterator[TestClient]:
    def test_get_session() -> Iterator[Session]:
        try:
            yield db_session
        finally:
            db_session.rollback()

    app.dependency_overrides[get_session] = test_get_session

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_session, None)
