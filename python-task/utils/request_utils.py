from typing import List, Dict

import requests


def get_access_token(url: str, json: dict, headers: Dict[str, str]) -> str:
    """
    Extracts access token for authorization in API via request.

    Parameters
    ----------
    url : str
        URL of the access token.
    json : str
        JSON object to send in the body.
    headers: Any
        Headers to send with the request.

    Returns
    -------
    token : str
        Access token for API.
    """
    response = requests.request("POST", url=url, json=json, headers=headers)
    token = response.json()["oauth"]["access_token"]
    return token


def get_request_resource_as_json(url: str, headers: Dict[str, str], json: Dict[str, str] = None) -> List[dict]:
    """
    Extracts data from API via request.

    Parameters
    ----------
    url : str
        URL of the data.
    json : str
        JSON object to send in the body.
    headers: Any
        Headers to send with the request.

    Returns
    -------
    data : List[dict]
        Required data.
    """
    response = requests.request("GET", url=url, json=json, headers=headers)
    data = response.json()
    return data
