import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.conftest import authentication_token_from_email
from app.tests.utils.user import create_random_user
from app.tests.utils.item import create_random_item
from app.tests.utils.item_category import create_random_item_category
from app.tests.utils.item_unit import create_random_item_unit


def test_create_item_category(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"name": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/item_categories/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_read_item_category(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item_category = create_random_item_category(db)
    response = client.get(
        f"{settings.API_V1_STR}/item_categories/{item_category.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == item_category.name
    assert content["description"] == item_category.description
    assert content["id"] == str(item_category.id)
    assert content["owner_id"] == str(item_category.owner_id)


def test_read_item_category_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/item_categories/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item category not found"


def test_read_item_category_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item_category = create_random_item_category(db)
    response = client.get(
        f"{settings.API_V1_STR}/item_categories/{item_category.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_item_categories(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_item_category(db)
    create_random_item_category(db)
    response = client.get(
        f"{settings.API_V1_STR}/item_categories/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_read_item_categories_with_owner(
    client: TestClient, db: Session
) -> None:
    user = create_random_user(db=db)
    create_random_item_category(db, user)
    create_random_item_category(db, user)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    response = client.get(
        f"{settings.API_V1_STR}/item_categories/",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_item_category(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item_category = create_random_item_category(db)
    data = {"name": "Updated name", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/item_categories/{item_category.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["id"] == str(item_category.id)
    assert content["owner_id"] == str(item_category.owner_id)


def test_update_item_category_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"name": "Updated name", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/item_categories/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item category not found"


def test_update_item_category_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item_category = create_random_item_category(db)
    data = {"name": "Updated name", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/item_categories/{item_category.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_item_category(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item_category = create_random_item_category(db)
    response = client.delete(
        f"{settings.API_V1_STR}/item_categories/{item_category.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Item category deleted successfully"


def test_delete_item_category_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/item_categories/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item category not found"


def test_delete_item_category_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item_category = create_random_item_category(db)
    response = client.delete(
        f"{settings.API_V1_STR}/item_categories/{item_category.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"
