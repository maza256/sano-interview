from unittest.mock import MagicMock
from ..endpoints.endpoints import set_db_handler
from pydantic import BaseModel
from fastapi.testclient import TestClient
from ..main import app


client = TestClient(app)


def test_read_all_users():
    mock_db_handler = MagicMock()
    mock_db_handler.get_all_users.return_value = ["user1", "user2", "user3"]
    set_db_handler(mock_db_handler)

    response = client.get("/individuals")
    assert response.status_code == 200
    assert response.json() == ["user1", "user2", "user3"]


def test_read_individual():
    mock_db_handler = MagicMock()
    mock_db_handler.get_individual_data.return_value = {"variant": "rs123", "value": "A"}
    set_db_handler(mock_db_handler)

    response = client.get("/individuals/user1/genetic-data?variants=rs123")
    assert response.status_code == 200
    assert response.json() == {"variant": "rs123", "value": "A"}


def test_create_individual():
    mock_db_handler = MagicMock()
    set_db_handler(mock_db_handler)

    payload = {"individual_id": "user123"}
    response = client.post("/individuals", json=payload)

    assert response.status_code == 200
    assert response.text == "\"Succesfully added new individual\""
    mock_db_handler.insert_new_individual.assert_called_once_with("user123")


def test_insert_individual_data():
    mock_db_handler = MagicMock()
    set_db_handler(mock_db_handler)

    file_content = open("tests/individual123.sano").read()

    response = client.post(
        "/individuals/user123/genetic_data",
        files={"file": ("test_file.txt", file_content)}
    )

    assert response.status_code == 200
    assert response.text == "\"Successfully uploaded data\""