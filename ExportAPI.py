import requests

from ENVAPI import WEBSERVICE_PATHS, requestUserId, dumpPath
from datetime import datetime


def export_company_bean(environment_url, token, sourceCompanyID, sourceEnvironment):
    companyIDWithEnv = sourceEnvironment[5:] + "_" + sourceCompanyID
    dt_string = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    fullDumpPath = dumpPath + companyIDWithEnv.upper() + "_" + dt_string
    export_api_path = WEBSERVICE_PATHS["exportCompanyData"]
    bearer = "Bearer " + token
    export_api_url = environment_url + export_api_path
    headers = {
        "Content-Type": "application/json",
        "Authorization": bearer
    }
    body = {"masterInstanceId": sourceCompanyID, "targetCompanyId": "tmp",
            "companyName": "tmp", "requestUserId": requestUserId, "hanaInstanceExportDirectory": fullDumpPath}
    try:
        export_api_response = requests.post(export_api_url, json=body, headers=headers)
        if export_api_response.status_code == 200:
            print("Export Accepted")
        elif export_api_response.status_code == 403:
            print("forbidden during  export api")
            export_api_response = False
        elif export_api_response.status_code == 500:
            print("internal server error during export api")
            export_api_response = False
        else:
            print("Unknown response code", export_api_response.status_code)
    except Exception as generic_exception:
        print(generic_exception)

    return export_api_response.text, fullDumpPath
