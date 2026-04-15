from pathlib import Path
import sys

import pytest
from tinydb import TinyDB

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app


def _get_todo_db(flask_app):
    return flask_app.extensions["tinydb"]


def _close_tinydb(db):
    storage = getattr(db, "storage", None)
    if storage and hasattr(storage, "close"):
        storage.close()


@pytest.fixture()
def client(tmp_path):
    """Create a test client with an isolated TinyDB database file."""
    db_path = tmp_path / "test_db.json"
    original_db = app.extensions["tinydb"]
    test_db = TinyDB(db_path)

    app.config.update(TESTING=True)
    app.extensions["tinydb"] = test_db

    try:
        with app.test_client() as test_client:
            yield test_client
    finally:
        _close_tinydb(test_db)
        app.extensions["tinydb"] = original_db


def test_main_page_loads_successfully(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"To Do List" in response.data


def test_add_new_task(client):
    response = client.post("/add", data={"title": "Write pytest tests"}, follow_redirects=True)

    assert response.status_code == 200
    assert b"Write pytest tests" in response.data

    saved_tasks = _get_todo_db(app).all()
    assert len(saved_tasks) == 1
    assert saved_tasks[0]["title"] == "Write pytest tests"
    assert saved_tasks[0]["complete"] is False


def test_delete_existing_task(client):
    todo_db = _get_todo_db(app)
    todo_db.insert({"id": 1, "title": "Task to remove", "complete": False})

    response = client.post("/delete/1", follow_redirects=True)

    assert response.status_code == 200
    assert b"Task to remove" not in response.data
    assert todo_db.all() == []
