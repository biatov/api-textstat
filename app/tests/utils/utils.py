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


def get_default_text() -> str:
    return """Playing games has always been thought to be important to
            the development of well-balanced and creative children;
            however, what part, if any, they should play in the lives
            of adults has never been researched that deeply. I believe
            that playing games is every bit as important for adults
            as for children. Not only is taking time out to play games
            with our children and other adults valuable to building
            interpersonal relationships but is also a wonderful way
            to release built up tension."""


def random_text_id() -> str:
    return str(uuid.uuid4())


def random_content_type() -> str:
    content_types = settings.FILE_CONTENT_TYPES or ("text/plain",)
    return random.choice(content_types)


def random_extension() -> str:
    # let keep it like this
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
