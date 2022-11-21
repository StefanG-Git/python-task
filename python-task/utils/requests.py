import requests


def get_access_token(url, json, headers):
    response = requests.request("POST", url=url, json=json, headers=headers)

    return response.json()["oauth"]["access_token"]


def get_request_resource(url, headers, json=None):
    response = requests.request("GET", url=url, json=json, headers=headers)

    return response.json()