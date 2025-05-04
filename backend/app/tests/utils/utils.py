import random
import string

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_latitude() -> float:
    return random.uniform(-11.0, 6.0)


def random_longitude() -> float:
    return random.uniform(95.0, 141.0)


def random_coordinate() -> tuple[float, float]:
    # Indonesia: Latitude ~ -11.0 to 6.0, Longitude ~ 95.0 to 141.0
    return random_latitude(), random_longitude()


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
