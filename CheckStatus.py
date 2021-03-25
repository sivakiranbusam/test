import requests

from ENVAPI import WEBSERVICE_PATHS
from JsonRead import getCheckStatusResponseCode


def check_status(environment_url, token, payload):
    check_status = WEBSERVICE_PATHS["checkstatus"]

    bearer = "Bearer " + token
    check_status_url = environment_url + check_status
    headers = {
        "Content-Type": "application/json",
        "Authorization": bearer
    }
    response = requests.request("POST", check_status_url, headers=headers, data=payload)
    return getCheckStatusResponseCode(response.text);
