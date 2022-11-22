from typing import List

import requests


def get_access_token(url: str, json: dict, headers: dict) -> dict:
    response = requests.request("POST", url=url, json=json, headers=headers)

    return response.json()["oauth"]["access_token"]


def get_request_resource(url: str, headers: dict, json: dict = None) -> List[dict]:
    response = requests.request("GET", url=url, json=json, headers=headers)

    return response.json()
