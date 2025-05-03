import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.conftest import authentication_token_from_email
from app.tests.utils.user import create_random_user
from app.tests.utils.item_unit import create_random_item_unit


def test_create_item_unit(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"name": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/item_units/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_read_item_unit(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item_unit = create_random_item_unit(db)
    response = client.get(
        f"{settings.API_V1_STR}/item_units/{item_unit.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == item_unit.name
    assert content["description"] == item_unit.description
    assert content["id"] == str(item_unit.id)
    assert content["owner_id"] == str(item_unit.owner_id)


def test_read_item_unit_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/item_units/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item unit not found"


def test_read_item_unit_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item_unit = create_random_item_unit(db)
    response = client.get(
        f"{settings.API_V1_STR}/item_units/{item_unit.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_item_units(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_item_unit(db)
    create_random_item_unit(db)
    response = client.get(
        f"{settings.API_V1_STR}/item_units/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_read_item_units_with_owner(
    client: TestClient, db: Session
) -> None:
    user = create_random_user(db=db)
    create_random_item_unit(db, user)
    create_random_item_unit(db, user)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    response = client.get(
        f"{settings.API_V1_STR}/item_units/",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_item_unit(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item_unit = create_random_item_unit(db)
    data = {"name": "Updated name", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/item_units/{item_unit.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["id"] == str(item_unit.id)
    assert content["owner_id"] == str(item_unit.owner_id)


def test_update_item_unit_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"name": "Updated name", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/item_units/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item unit not found"


def test_update_item_unit_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item_unit = create_random_item_unit(db)
    data = {"name": "Updated name", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/item_units/{item_unit.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_item_unit(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item_unit = create_random_item_unit(db)
    response = client.delete(
        f"{settings.API_V1_STR}/item_units/{item_unit.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Item unit deleted successfully"


def test_delete_item_unit_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/item_units/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item unit not found"


def test_delete_item_unit_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item_unit = create_random_item_unit(db)
    response = client.delete(
        f"{settings.API_V1_STR}/item_units/{item_unit.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"
