import uuid
import pytest
import requests

OAUTH_TOKEN = ""
BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"
HEADERS = {"Authorization": f"OAuth {OAUTH_TOKEN}"}


@pytest.fixture
def random_folder_path():
    folder_name = f"test_folder_{uuid.uuid4().hex[:8]}"
    path = f"/{folder_name}"

    yield path

    requests.delete(
        BASE_URL,
        headers=HEADERS,
        params={"path": path, "permanently": "true"}
    )


def test_create_folder_success(random_folder_path):
    response = requests.put(BASE_URL, headers=HEADERS, params={"path": random_folder_path})

    assert response.status_code in (200, 201), f"Ошибка создания: {response.text}"

    check_response = requests.get(BASE_URL, headers=HEADERS, params={"path": random_folder_path})
    assert check_response.status_code == 200, "Папка не найдена после создания"

    data = check_response.json()
    assert data["type"] == "dir"
    assert data["name"] == random_folder_path.strip("/")


def test_create_folder_already_exists(random_folder_path):
    requests.put(BASE_URL, headers=HEADERS, params={"path": random_folder_path})

    response = requests.put(BASE_URL, headers=HEADERS, params={"path": random_folder_path})

    assert response.status_code == 409, "Сервер должен вернуть ошибку конфликта"


def test_create_folder_unauthorized():
    bad_headers = {"Authorization": "OAuth invalid_token_12345"}
    path = "/some_test_folder"

    response = requests.put(BASE_URL, headers=bad_headers, params={"path": path})

    assert response.status_code == 401, "Сервер должен отклонить невалидный токен"