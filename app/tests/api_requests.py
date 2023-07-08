import requests
import json
from typing import Literal

import json
from typing import Literal
from urllib.parse import urljoin

import requests

from app.validate import raise_http_error


session = requests.Session()


def base_request(http_method: Literal["get", "post", "delete", "patch"], path: "str", *args, **kwargs) -> dict:
    method = getattr(session, http_method)
    response = method(urljoin('http//:127.0.0.1:8080', path), *args, **kwargs)
    if response.status_code >= 400:
        try:
            message = response.json()
        except json.JSONDecodeError:
            message = response.text
        raise raise_http_error(response.status_code, message)
    return response.json()


def register(email: str, password: str) -> int:
    return base_request("post", "users", json={"email": email, "password": password})["id"]


def login(email: str, password: str) -> dict:
    return base_request("post", "login", json={"email": email, "password": password})


def logout(email: str, password: str) -> str:
    return base_request("post", "logout", json={"email": email, "password": password})["status"]


def get_user(user_id: int) -> dict:
    return base_request("get", f"users/{user_id}")


def post_adv(title: str, description: str) -> dict:
    return base_request("post", "adv", json={"title": title, "description": description})


def get_adv(adv_id: int) -> dict:
    return base_request("get", f"adv/{adv_id}")


def patch_adv(adv_id: int, new_description: str) -> dict:
    return base_request("patch", f"adv/{adv_id}", json={"description": new_description})


def delete_adv(adv_id: int) -> str:
    return base_request("delete", f"adv/{adv_id}")["status"]
