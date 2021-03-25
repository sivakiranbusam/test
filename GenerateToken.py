import requests

from ENVAPI import WEBSERVICE_PATHS


def generate_token(environment_url):
    body = {"grant_type": "client_credentials", "scope": "userId=SPCPROV,resourceType=sfprovisioning"}

    generate_token_path = WEBSERVICE_PATHS["generatetoken"]

    generate_token_url = environment_url + generate_token_path
    resp = requests.post(generate_token_url, json=body,
                         headers={"Content-Type": "application/json",
                                  "Authorization": "Basic "
                                                   "c3BjOjQ0YWE4MjBlOTVmMTQwYTlhOTViNDY2MDUyYTZiMGM0YTFjODY5ODRlNjFkNDJhY2E4YzE0NzQyZmQzZDc4NmE="})
    full_token = resp.text
    start_index = full_token.index(':') + 2
    end_index = full_token.index(",") - 1
    formatted_token = full_token[start_index:end_index]
    return formatted_token
