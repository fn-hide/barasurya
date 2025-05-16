import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.config import settings
from app.models import Customer
from app.tests.conftest import authentication_token_from_email
from app.tests.utils.customer import create_random_customer
from app.tests.utils.customer_type import create_random_customer_type
from app.tests.utils.user import create_random_user


def test_create_customer(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(
        client=client, email=user.email, db=db
    )
    customer_type = create_random_customer_type(db, user)
    data = {
        "name": "Foo",
        "phone": "+6281234567890",
        "address": "St. Groove",
        "customer_type_id": str(customer_type.id),
    }
    response = client.post(
        f"{settings.API_V1_STR}/customers/",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["phone"] == data["phone"]
    assert content["address"] == data["address"]
    assert content["customer_type_id"] == data["customer_type_id"]
    assert "id" in content
    assert "owner_id" in content


def test_create_customer_customer_type_not_found(
    client: TestClient, db: Session
) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(
        client=client, email=user.email, db=db
    )
    data = {
        "name": "Foo",
        "phone": "+6281234567890",
        "address": "St. Groove",
        "customer_type_id": str(uuid.uuid4()),
    }
    response = client.post(
        f"{settings.API_V1_STR}/customers/",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Customer type not found"


def test_read_customer(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(
        client=client, email=user.email, db=db
    )
    customer = create_random_customer(db, user)
    response = client.get(
        f"{settings.API_V1_STR}/customers/{customer.id}",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == customer.name
    assert content["phone"] == customer.phone
    assert content["address"] == customer.address
    assert content["id"] == str(customer.id)
    assert content["owner_id"] == str(customer.owner_id)


def test_read_customer_not_found(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(
        client=client, email=user.email, db=db
    )
    response = client.get(
        f"{settings.API_V1_STR}/customers/{uuid.uuid4()}",
        headers=user_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Customer not found"


def test_read_customer_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    customer = create_random_customer(db)
    response = client.get(
        f"{settings.API_V1_STR}/customers/{customer.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_customers(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(
        client=client, email=user.email, db=db
    )
    create_random_customer(db, user)
    create_random_customer(db, user)
    response = client.get(
        f"{settings.API_V1_STR}/customers/",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 2


def test_read_customers_superuser(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    statement = delete(Customer)
    db.exec(statement)
    db.commit()

    create_random_customer(db)
    create_random_customer(db)
    response = client.get(
        f"{settings.API_V1_STR}/customers/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 2


def test_update_customer(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(
        client=client, email=user.email, db=db
    )
    customer = create_random_customer(db, user)
    data = {
        "name": "Updated name",
        "phone": "Updated phone",
        "address": "Updated address",
    }
    response = client.put(
        f"{settings.API_V1_STR}/customers/{customer.id}",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["phone"] == data["phone"]
    assert content["address"] == data["address"]
    assert content["id"] == str(customer.id)
    assert content["owner_id"] == str(customer.owner_id)


def test_update_customer_not_found(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(
        client=client, email=user.email, db=db
    )
    data = {
        "name": "Updated name",
        "phone": "Updated phone",
        "address": "Updated address",
    }
    response = client.put(
        f"{settings.API_V1_STR}/customers/{uuid.uuid4()}",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Customer not found"


def test_update_customer_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    customer = create_random_customer(db)
    data = {
        "name": "Updated name",
        "phone": "Updated phone",
        "address": "Updated address",
    }
    response = client.put(
        f"{settings.API_V1_STR}/customers/{customer.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_update_customer_customer_type_not_found(
    client: TestClient, db: Session
) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(
        client=client, email=user.email, db=db
    )
    customer = create_random_customer(db, user)
    data = {
        "name": "Updated name",
        "phone": "Updated phone",
        "address": "Updated address",
        "customer_type_id": str(uuid.uuid4()),
    }
    response = client.put(
        f"{settings.API_V1_STR}/customers/{customer.id}",
        headers=user_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Customer type not found"


def test_delete_item_category(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(
        client=client, email=user.email, db=db
    )
    customer = create_random_customer(db, user)
    response = client.delete(
        f"{settings.API_V1_STR}/customers/{customer.id}",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Customer deleted successfully"


def test_delete_customer_not_found(client: TestClient, db: Session) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(
        client=client, email=user.email, db=db
    )
    response = client.delete(
        f"{settings.API_V1_STR}/customers/{uuid.uuid4()}",
        headers=user_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Customer not found"


def test_delete_customer_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    customer = create_random_customer(db)
    response = client.delete(
        f"{settings.API_V1_STR}/customers/{customer.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"
