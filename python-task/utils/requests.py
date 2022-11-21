import requests


def get_access_token():
    url = "https://api.baubuddy.de/index.php/login"

    payload = {
        "username": "365",
        "password": "1"
    }

    headers = {
        "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
        "Content-Type": "application/json"
    }

    response = requests.request("Post", url=url, json=payload, headers=headers)

    return response.json()["oauth"]["access_token"]
