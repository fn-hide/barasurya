import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.config import settings
from app.tests.conftest import authentication_token_from_email
from app.tests.utils.user import create_random_user
from app.tests.utils.customer_type import create_random_customer_type
from app.models import CustomerType


def test_create_customer_type(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    data = {"name": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/customer_types/",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_read_customer_type(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    customer_type = create_random_customer_type(db, user)
    response = client.get(
        f"{settings.API_V1_STR}/customer_types/{customer_type.id}",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == customer_type.name
    assert content["description"] == customer_type.description
    assert content["id"] == str(customer_type.id)
    assert content["owner_id"] == str(customer_type.owner_id)


def test_read_customer_type_not_found(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    response = client.get(
        f"{settings.API_V1_STR}/customer_types/{uuid.uuid4()}",
        headers=user_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "CustomerType not found"


def test_read_customer_type_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    customer_type = create_random_customer_type(db)
    response = client.get(
        f"{settings.API_V1_STR}/customer_types/{customer_type.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_customer_types(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    create_random_customer_type(db, user)
    create_random_customer_type(db, user)
    response = client.get(
        f"{settings.API_V1_STR}/customer_types/",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 2


def test_read_customer_types_superuser(client: TestClient, superuser_token_headers: dict[str, str], db: Session) -> None:
    statement = delete(CustomerType)
    db.exec(statement)
    db.commit()
    
    create_random_customer_type(db)
    create_random_customer_type(db)
    response = client.get(
        f"{settings.API_V1_STR}/customer_types/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 2


def test_update_customer_type(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    customer_type = create_random_customer_type(db, user)
    data = {"name": "Updated name", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/customer_types/{customer_type.id}",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["id"] == str(customer_type.id)
    assert content["owner_id"] == str(customer_type.owner_id)


def test_update_customer_type_not_found(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    data = {"name": "Updated name", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/customer_types/{uuid.uuid4()}",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "CustomerType not found"


def test_update_customer_type_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    customer_type = create_random_customer_type(db)
    data = {"name": "Updated name", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/customer_types/{customer_type.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_item_category(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    customer_type = create_random_customer_type(db, user)
    response = client.delete(
        f"{settings.API_V1_STR}/customer_types/{customer_type.id}",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "CustomerType deleted successfully"


def test_delete_customer_type_not_found(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    response = client.delete(
        f"{settings.API_V1_STR}/customer_types/{uuid.uuid4()}",
        headers=user_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "CustomerType not found"


def test_delete_customer_type_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    customer_type = create_random_customer_type(db)
    response = client.delete(
        f"{settings.API_V1_STR}/customer_types/{customer_type.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"
