import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.config import settings
from app.tests.conftest import authentication_token_from_email
from app.tests.utils.user import create_random_user
from app.tests.utils.supplier import create_random_supplier
from app.models import Supplier


def test_create_supplier(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    data = {"name": "Foo", "phone": "+6281234567890", "address": "St. Groove"}
    response = client.post(
        f"{settings.API_V1_STR}/suppliers/",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["address"] == data["address"]
    assert content["phone"] == data["phone"]
    assert "id" in content
    assert "owner_id" in content


def test_read_supplier(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    supplier = create_random_supplier(db, user)
    response = client.get(
        f"{settings.API_V1_STR}/suppliers/{supplier.id}",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == supplier.name
    assert content["address"] == supplier.address
    assert content["id"] == str(supplier.id)
    assert content["owner_id"] == str(supplier.owner_id)


def test_read_supplier_not_found(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    response = client.get(
        f"{settings.API_V1_STR}/suppliers/{uuid.uuid4()}",
        headers=user_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Supplier not found"


def test_read_supplier_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    supplier = create_random_supplier(db)
    response = client.get(
        f"{settings.API_V1_STR}/suppliers/{supplier.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_suppliers(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    create_random_supplier(db, user)
    create_random_supplier(db, user)
    response = client.get(
        f"{settings.API_V1_STR}/suppliers/",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 2


def test_read_suppliers_superuser(client: TestClient, superuser_token_headers: dict[str, str], db: Session) -> None:
    statement = delete(Supplier)
    db.exec(statement)
    db.commit()
    
    create_random_supplier(db)
    create_random_supplier(db)
    response = client.get(
        f"{settings.API_V1_STR}/suppliers/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 2


def test_update_supplier(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    supplier = create_random_supplier(db, user)
    data = {"name": "Updated name", "phone": "+6281234567890", "address": "Updated address"}
    response = client.put(
        f"{settings.API_V1_STR}/suppliers/{supplier.id}",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["address"] == data["address"]
    assert content["id"] == str(supplier.id)
    assert content["owner_id"] == str(supplier.owner_id)


def test_update_supplier_not_found(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    data = {"name": "Updated name", "phone": "+6281234567890", "address": "Updated address"}
    response = client.put(
        f"{settings.API_V1_STR}/suppliers/{uuid.uuid4()}",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Supplier not found"


def test_update_supplier_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    supplier = create_random_supplier(db)
    data = {"name": "Updated name", "phone": "+6281234567890", "address": "Updated address"}
    response = client.put(
        f"{settings.API_V1_STR}/suppliers/{supplier.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_item_category(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    supplier = create_random_supplier(db, user)
    response = client.delete(
        f"{settings.API_V1_STR}/suppliers/{supplier.id}",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Supplier deleted successfully"


def test_delete_supplier_not_found(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    response = client.delete(
        f"{settings.API_V1_STR}/suppliers/{uuid.uuid4()}",
        headers=user_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Supplier not found"


def test_delete_supplier_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    supplier = create_random_supplier(db)
    response = client.delete(
        f"{settings.API_V1_STR}/suppliers/{supplier.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"
