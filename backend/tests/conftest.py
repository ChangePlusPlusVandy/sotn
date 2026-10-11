import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.auth import get_current_staff
from app.core.db import engine, get_db
from app.main import app
from app.models.base import Base

TEST_STAFF_ID = "user_test_staff"


@pytest.fixture
def db():
    # Each test runs inside a transaction that is rolled back, so nothing persists.
    with engine.connect() as connection:
        transaction = connection.begin()
        session = Session(bind=connection, join_transaction_mode="create_savepoint")
        # Start every test from empty tables; the rollback restores any local dev data.
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        yield session
        session.close()
        transaction.rollback()


@pytest.fixture
def client(db):
    """Unauthenticated client, as a public visitor."""
    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def staff_client(client):
    """Client signed in as a staff member, without needing a real Clerk token."""
    app.dependency_overrides[get_current_staff] = lambda: TEST_STAFF_ID
    return client
