import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.config import settings
from app.models import Item
from app.tests.conftest import authentication_token_from_email
from app.tests.utils.user import create_random_user
from app.tests.utils.item import create_random_item
from app.tests.utils.item_category import create_random_item_category
from app.tests.utils.item_unit import create_random_item_unit


def test_create_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item_category = create_random_item_category(db)
    item_unit = create_random_item_unit(db)
    data = {"title": "Foo", "description": "Fighters", "item_category_id": str(item_category.id), "item_unit_id": str(item_unit.id)}
    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_create_item_not_found_category(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item_unit = create_random_item_unit(db)
    data = {"title": "Foo", "description": "Fighters", "item_category_id": str(uuid.uuid4()), "item_unit_id": str(item_unit.id)}
    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item category not found"


def test_create_item_not_found_unit(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item_category = create_random_item_category(db)
    data = {"title": "Foo", "description": "Fighters", "item_category_id": str(item_category.id), "item_unit_id": str(uuid.uuid4())}
    response = client.post(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item unit not found"


def test_read_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    response = client.get(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == item.title
    assert content["description"] == item.description
    assert content["id"] == str(item.id)
    assert content["owner_id"] == str(item.owner_id)


def test_read_item_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/items/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_read_item_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    response = client.get(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_items(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    statement = delete(Item)
    db.exec(statement)
    db.commit()
    create_random_item(db)
    create_random_item(db)
    response = client.get(
        f"{settings.API_V1_STR}/items/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 2


def test_read_items_with_owner(
    client: TestClient, db: Session
) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    create_random_item(db, user)
    create_random_item(db, user)
    response = client.get(
        f"{settings.API_V1_STR}/items/",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 2


def test_update_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content["id"] == str(item.id)
    assert content["owner_id"] == str(item.owner_id)


def test_update_item_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/items/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_update_item_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_update_item_not_found_category(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    data = {"title": "Updated title", "description": "Updated description", "item_category_id": str(uuid.uuid4())}
    response = client.put(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item category not found"


def test_update_item_not_found_unit(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    data = {"title": "Updated title", "description": "Updated description", "item_unit_id": str(uuid.uuid4())}
    response = client.put(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item unit not found"


def test_update_by_increase_stock_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    current_stock = 100
    new_stock = 50
    item = create_random_item(db, stock=current_stock)
    data = {"quantity": new_stock}
    response = client.put(
        f"{settings.API_V1_STR}/items/{item.id}/stock",
        headers=superuser_token_headers,
        params=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["stock"] == current_stock + new_stock
    assert content["id"] == str(item.id)
    assert content["owner_id"] == str(item.owner_id)


def test_update_by_decrease_stock_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    current_stock = 100
    sold_stock = 50
    item = create_random_item(db, stock=current_stock)
    data = {"quantity": -sold_stock}
    response = client.put(
        f"{settings.API_V1_STR}/items/{item.id}/stock",
        headers=superuser_token_headers,
        params=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["stock"] == current_stock - sold_stock
    assert content["id"] == str(item.id)
    assert content["owner_id"] == str(item.owner_id)


def test_update_stock_item_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"quantity": 100}
    response = client.put(
        f"{settings.API_V1_STR}/items/{str(uuid.uuid4())}/stock",
        headers=superuser_token_headers,
        params=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_update_stock_item_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    data = {"quantity": 100}
    response = client.put(
        f"{settings.API_V1_STR}/items/{item.id}/stock",
        headers=normal_user_token_headers,
        params=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_low_stock_items(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    statement = delete(Item)
    db.exec(statement)
    db.commit()
    item_1 = create_random_item(db, stock_minimum=10)
    item_2 = create_random_item(db, stock_minimum=10, stock=15)
    response = client.get(
        f"{settings.API_V1_STR}/items/low_stock/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 1
    

def test_read_low_stock_items_with_owner(
    client: TestClient, db: Session
) -> None:
    user = create_random_user(db=db)
    user_token_headers = authentication_token_from_email(client=client, email=user.email, db=db)
    create_random_item(db, user, stock_minimum=10)
    create_random_item(db, user, stock_minimum=10)
    response = client.get(
        f"{settings.API_V1_STR}/items/low_stock/",
        headers=user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) == 2


def test_activate_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db, is_active=False)
    assert item.is_active == False
    
    response = client.put(
        f"{settings.API_V1_STR}/items/{item.id}/activate/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["is_active"] == True
    assert "id" in content
    assert "owner_id" in content


def test_activate_item_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db, is_active=False)
    assert item.is_active == False
    response = client.put(
        f"{settings.API_V1_STR}/items/{str(uuid.uuid4())}/activate/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_activate_item_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db, is_active=False)
    assert item.is_active == False
    response = client.put(
        f"{settings.API_V1_STR}/items/{item.id}/activate/",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_deactivate_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db, is_active=True)
    assert item.is_active == True
    response = client.put(
        f"{settings.API_V1_STR}/items/{item.id}/deactivate/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["is_active"] == False
    assert "id" in content
    assert "owner_id" in content


def test_deactivate_item_not_found(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db, is_active=True)
    assert item.is_active == True
    response = client.put(
        f"{settings.API_V1_STR}/items/{str(uuid.uuid4())}/deactivate/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_deactivate_item_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db, is_active=True)
    assert item.is_active == True
    response = client.put(
        f"{settings.API_V1_STR}/items/{item.id}/deactivate/",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_item(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    response = client.delete(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Item deleted successfully"


def test_delete_item_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/items/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


def test_delete_item_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    item = create_random_item(db)
    response = client.delete(
        f"{settings.API_V1_STR}/items/{item.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"
