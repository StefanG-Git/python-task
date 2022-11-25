from typing import List, Dict

import requests


def get_access_token(url: str, json: dict, headers: Dict[str, str]) -> dict:
    response = requests.request("POST", url=url, json=json, headers=headers)

    return response.json()["oauth"]["access_token"]


def get_request_resource(url: str, headers: Dict[str, str], json: Dict[str, str] = None) -> List[dict]:
    response = requests.request("GET", url=url, json=json, headers=headers)

    return response.json()
