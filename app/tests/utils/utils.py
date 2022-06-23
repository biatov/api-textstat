import os
import random
import string
import uuid
from typing import Dict, BinaryIO

from fastapi.testclient import TestClient

from app.core.config import settings


def file_data() -> BinaryIO:
    path = os.path.dirname(os.path.abspath(__file__))
    return open(f"{path}/scratch.txt", "rb")


def random_text_id() -> str:
    return str(uuid.uuid4())


def random_content_type() -> str:
    content_types = settings.FILE_CONTENT_TYPES or ("text/plain",)
    return random.choice(content_types)


def random_extension() -> str:
    # let's keep it like this
    return "txt"


def random_filename() -> str:
    name = random_lower_string()
    extension = random_extension()
    return f"{name}.{extension}"


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post("/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
