from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.tests.utils.text import create_random_text, get_text_db
from app.tests.utils.utils import file_data, random_content_type, random_filename


def test_upload_text(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    content_type = random_content_type()
    file = file_data()
    filename = random_filename()
    data = {"Text": (filename, file, content_type)}
    response = client.post(
        "Text/", files=data, headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content


def test_read_texts(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    text = create_random_text(db)
    response = client.get(
        "Text/", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 1
    text_resp = content[0]
    assert text_resp["id"] == text.id
    assert text_resp["name"] == text.name
    assert text_resp["content_type"] == text.content_type
    assert text_resp["extension"] == text.extension


def test_read_text(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    text = create_random_text(db)
    response = client.get(
        f"Text/{text.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["stats"] == []


def test_delete_text(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    text = create_random_text(db)
    response = client.delete(
        f"Text/{text.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200

    response = client.get(
        f"Text/{text.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 404


def test_save_text_stats(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    text = create_random_text(db)
    data = [{
        "name": "syllable_count"
    }]
    response = client.post(
        f"Text/{text.id}", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == text.id

    response = client.post(
        f"Text/{text.id}", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == text.id


def test_save_text_stats_in_db(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    content_type = random_content_type()
    file = file_data()
    filename = random_filename()
    data = {"Text": (filename, file, content_type)}
    response = client.post(
        "Text/", files=data, headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()

    text_id = content["id"]
    attribute = {
        "name": "wiener_sachtextformel",
        "lang": "en",
        "argument": {
            "name": "variant",
            "value": 1
        }
    }
    data = [attribute]
    response = client.post(
        f"Text/{text_id}", headers=superuser_token_headers, json=data
    )
    assert response.status_code == 200

    response = client.get(
        f"Text/{text_id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    content = response.json()
    text = get_text_db(db=db, text_id=text_id)

    assert len(content["stats"]), 1
    assert content["id"] == text_id
    assert content["name"] == text.name
    assert content["content_type"] == text.content_type
    assert content["extension"] == text.extension
    assert content["created_at"].replace("T", " ") == str(text.created_at)
    assert content["updated_at"].replace("T", " ") == str(text.updated_at)
    assert len(text.stats), 1
    stat = text.stats[0]
    assert stat.name, attribute["name"]
    assert stat.lang, attribute["lang"]
    assert type(stat.value), float
    assert stat.argument, attribute["argument"]
