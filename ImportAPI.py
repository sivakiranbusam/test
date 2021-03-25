import requests

from ENVAPI import WEBSERVICE_PATHS


def import_company_data(environment_url, token, payLoad):
    import_api_path = WEBSERVICE_PATHS["importCompanyData"]
    bearer = "Bearer " + token
    import_api_url = environment_url + import_api_path
    headers = {
        "Content-Type": "application/json",
        "Authorization": bearer
    }
    try:
        import_api_response = requests.post(import_api_url, json=payLoad, headers=headers)
        if import_api_response.status_code == 200:
            print("Import Accepted")
        elif import_api_response.status_code == 403:
            print("forbidden during  export api")
        elif import_api_response.status_code == 500:
            print("internal server error during import api")
        else:
            print("Unknown response code", import_api_response.status_code)
    except Exception as generic_exception:
        print(generic_exception)
    print(import_api_response.text)
    return import_api_response.text
