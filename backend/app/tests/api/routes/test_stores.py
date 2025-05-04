import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.config import settings
from app.tests.conftest import authentication_token_from_email
from app.tests.utils.user import create_random_user
from app.tests.utils.store import create_random_store
from app.models import Store


def test_create_store(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    data = {"name": "Foo", "address": "St. Groove", "latitude": 7.534, "longitude": 112.8347}
    response = client.post(
        f"{settings.API_V1_STR}/stores/",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["address"] == data["address"]
    assert content["latitude"] == data["latitude"]
    assert content["longitude"] == data["longitude"]
    assert "id" in content
    assert "owner_id" in content


def test_read_store(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    store = create_random_store(db, user)
    response = client.get(
        f"{settings.API_V1_STR}/stores/{store.id}",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == store.name
    assert content["address"] == store.address
    assert content["id"] == str(store.id)
    assert content["owner_id"] == str(store.owner_id)


def test_read_store_not_found(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    response = client.get(
        f"{settings.API_V1_STR}/stores/{uuid.uuid4()}",
        headers=user_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Store not found"


def test_read_store_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    store = create_random_store(db)
    response = client.get(
        f"{settings.API_V1_STR}/stores/{store.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_stores(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    create_random_store(db, user)
    create_random_store(db, user)
    response = client.get(
        f"{settings.API_V1_STR}/stores/",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 2


def test_read_stores_superuser(client: TestClient, superuser_token_headers: dict[str, str], db: Session) -> None:
    statement = delete(Store)
    db.exec(statement)
    db.commit()
    
    create_random_store(db)
    create_random_store(db)
    response = client.get(
        f"{settings.API_V1_STR}/stores/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 2


def test_update_store(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    store = create_random_store(db, user)
    data = {"name": "Updated name", "address": "Updated address", "latitude": 8.324, "longitude": 113.324}
    response = client.put(
        f"{settings.API_V1_STR}/stores/{store.id}",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["address"] == data["address"]
    assert content["latitude"] == data["latitude"]
    assert content["longitude"] == data["longitude"]
    assert content["id"] == str(store.id)
    assert content["owner_id"] == str(store.owner_id)


def test_update_store_not_found(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    data = {"name": "Updated name", "address": "Updated address", "latitude": 8.324, "longitude": 113.324}
    response = client.put(
        f"{settings.API_V1_STR}/stores/{uuid.uuid4()}",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Store not found"


def test_update_store_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    store = create_random_store(db)
    data = {"name": "Updated name", "address": "Updated address", "latitude": 8.324, "longitude": 113.324}
    response = client.put(
        f"{settings.API_V1_STR}/stores/{store.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_item_category(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    store = create_random_store(db, user)
    response = client.delete(
        f"{settings.API_V1_STR}/stores/{store.id}",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Store deleted successfully"


def test_delete_store_not_found(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    response = client.delete(
        f"{settings.API_V1_STR}/stores/{uuid.uuid4()}",
        headers=user_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Store not found"


def test_delete_store_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    store = create_random_store(db)
    response = client.delete(
        f"{settings.API_V1_STR}/stores/{store.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"
