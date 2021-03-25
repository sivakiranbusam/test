import json

from ENVAPI import requestUserId


def getExportPayLoad(data):
    responseToJson = json.loads(data)
    print("Response from Export API:\n", json.dumps(responseToJson, indent=4))
    if responseToJson["responseCode"] == 500:
        exit(1)
    requestID = responseToJson["requestId"]
    exportCheckPayLoad = "[{\r\n\"requestId\":\"" + requestID + "\",\r\n\"companyId\": \"tmp\"\r\n}]"
    return exportCheckPayLoad


def getImportPayLoad(data):
    responseToJson = json.loads(data)
    print("Response from Import API:\n", json.dumps(responseToJson, indent=4))
    if responseToJson["responseCode"] == 500:
        print("Import has some issues, exiting")
        exit(1)
    requestID = responseToJson["requestId"]
    companyID = responseToJson["companyId"]
    importPayLoad = "[{\r\n\"requestId\":\"" + requestID + "\",\r\n\"companyId\":\"" + companyID + "\"\r\n}]"
    print("payload of import check", importPayLoad)
    return importPayLoad


def getCheckStatusResponseCode(data):
    responseToJson = json.loads(data)
    print(json.dumps(responseToJson, indent=4))
    return responseToJson[0]["responseCode"]


def prepareImportPayLoad(exportCompanyJson, targetCompanyID, targetCompanyName, sourceCompanyID, targetPoolID,
                         full_dump_path):
    exportJson = json.loads(exportCompanyJson)
    payLoadForImport = {}
    payLoadForImport['targetCompanyId'] = targetCompanyID
    payLoadForImport['companyName'] = targetCompanyName
    payLoadForImport['masterInstanceId'] = sourceCompanyID
    payLoadForImport['requestUserId'] = requestUserId
    payLoadForImport['companyStatus'] = exportJson["companyStatus"]
    payLoadForImport['companyFeatureSet'] = exportJson["companyFeatureSet"]  # responseToJson["responseCode"]
    payLoadForImport['companyLanguage'] = exportJson["companyLanguage"]
    payLoadForImport['companyCountry'] = exportJson["companyCountry"]
    payLoadForImport['companyTotalSeats'] = exportJson["companyTotalSeats"]
    payLoadForImport['companyProvisionerId'] = requestUserId
    payLoadForImport['companyImmutableId'] = exportJson["companyImmutableId"]
    payLoadForImport['globalSchemaTypeNameMap'] = exportJson["globalSchemaTypeNameMap"]
    payLoadForImport['originalCompanySchema'] = exportJson["companySchema"][:-1]
    payLoadForImport['oracleDbPoolId'] = targetPoolID
    payLoadForImport['hanaInstance'] = "true"
    payLoadForImport['hanaInstanceImportDirectory'] = full_dump_path
    payLoadForImport['maxRetries'] = "900"
    payLoadForImport['sleepTime'] = "100000"
    print(json.dumps(payLoadForImport, indent=4))
    return json.dumps(payLoadForImport)
