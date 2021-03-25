import json

requestID = "123"
companyID = "EC"
payload = "[{\r\n\"requestId\":\"" + requestID + "\",\r\n\"companyId\":\"" + companyID + "\"\r\n}]"
print(payload)
name = 'QACAND_ECLila.'
name = name[:-1]
print(name)


def prepareImportPayLoadTest(targetCompanyName, targetCompanyID, sourceCompanyID, targetPoolID, full_dump_path):
    payLoadForImport = {}
    payLoadForImport['targetCompanyId'] = targetCompanyID
    payLoadForImport['companyName'] = targetCompanyName
    payLoadForImport['masterInstanceId'] = sourceCompanyID
    payLoadForImport['requestUserId'] = "SPCPROV"
    payLoadForImport['companyStatus'] = "2067"
    payLoadForImport[
        'companyFeatureSet'] = "{1, 2, 3, 4, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 19, 21, 22, 23, 24, 26, 27, 30, 33, 37, 39, 41, 42, 43, 44, 45, 50, 51, 54, 57, 58, 59, 61, 63, 64, 66, 69, 72, 75, 76, 78, 86, 93, 94, 95, 96, 98, 101, 105, 106, 107, 108, 200, 201, 203, 204, 207, 208, 220, 221, 222, 225, 226, 229, 299, 301, 303, 304, 306, 308, 309, 310, 312, 315, 317, 319, 321, 322, 324, 325, 326, 327, 328, 330, 332, 333, 340, 341, 342, 344, 345, 346, 348, 351, 354, 360, 367, 386, 393, 394, 395, 396, 400, 402, 413, 414, 415, 418, 420, 421, 422, 424, 427, 428, 429, 435, 440, 442, 448, 456, 457, 482, 499, 505, 511, 559, 564, 568, 585, 592, 601, 605, 608, 612, 622, 707, 737, 738, 751, 753, 758, 964, 999}"
    payLoadForImport['companyLanguage'] = "en"
    payLoadForImport['companyCountry'] = "US"
    payLoadForImport['companyTotalSeats'] = "0"
    payLoadForImport['companyProvisionerId'] = "SPCPROV"
    payLoadForImport['companyImmutableId'] = "4237e1df_f969_4a48_8bb8_13d7ebc14ac9"
    payLoadForImport['globalSchemaTypeNameMap'] = "{\"MESSAGESTORE\":\"QACANDMESSAGESTORE\"}"
    payLoadForImport['originalCompanySchema'] = "QACAND_ECLila"
    payLoadForImport['companyProvisionerId'] = "SPCPROV"
    payLoadForImport['oracleDbPoolId'] = targetPoolID
    payLoadForImport['hanaInstance'] = "true"
    payLoadForImport['hanaInstanceImportDirectory'] = full_dump_path
    payLoadForImport['maxRetries'] = "900"
    payLoadForImport['sleepTime'] = "100000"
    print(json.dumps(payLoadForImport, indent=4))
    return json.dumps(payLoadForImport)


prepareImportPayLoadTest("ECLilaaa", "ECLilaaa", "ECLila","dbPool1", "/tenantrefresh_trg/i336121/QACAND_ECLILA_14-03-2021-18-40-52")
