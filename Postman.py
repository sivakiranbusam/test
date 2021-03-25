import requests

url = "https://qacand.hcm.ondemand.com/provisioningapi/provisioning/rest/v1/company/importCompanyData"

payload="{\"targetCompanyId\": \"I336121T001\", \"companyName\": \"I336121T001\", \"masterInstanceId\": \"ECLila\", \"requestUserId\": \"SPCPROV\", \"companyStatus\": \"2067\", \"companyFeatureSet\": \"{1, 2, 3, 4, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 19, 21, 22, 23, 24, 26, 27, 30, 33, 37, 39, 41, 42, 43, 44, 45, 50, 51, 54, 57, 58, 59, 61, 63, 64, 66, 69, 72, 75, 76, 78, 86, 93, 94, 95, 96, 98, 101, 105, 106, 107, 108, 200, 201, 203, 204, 207, 208, 220, 221, 222, 225, 226, 229, 299, 301, 303, 304, 306, 308, 309, 310, 312, 315, 317, 319, 321, 322, 324, 325, 326, 327, 328, 330, 332, 333, 340, 341, 342, 344, 345, 346, 348, 351, 354, 360, 367, 386, 393, 394, 395, 396, 400, 402, 413, 414, 415, 418, 420, 421, 422, 424, 427, 428, 429, 435, 440, 442, 448, 456, 457, 482, 499, 505, 511, 559, 564, 568, 585, 592, 601, 605, 608, 612, 622, 707, 737, 738, 751, 753, 758, 964, 999}\", \"companyLanguage\": \"en\", \"companyCountry\": \"US\", \"companyTotalSeats\": \"0\", \"companyProvisionerId\": \"SPCPROV\", \"companyImmutableId\": \"4237e1df_f969_4a48_8bb8_13d7ebc14ac9\", \"globalSchemaTypeNameMap\": {\"MESSAGESTORE\": \"QACANDMESSAGESTORE\"}, \"originalCompanySchema\": \"QACAND_ECLila\", \"oracleDbPoolId\": \"dbPool1\", \"hanaInstance\": \"true\", \"hanaInstanceImportDirectory\": \"/tenantrefresh_trg/i336121/QACAND_ECLILA_14-03-2021-18-40-52\", \"maxRetries\": \"900\", \"sleepTime\": \"100000\"}"
headers = {
  'Authorization': 'Bearer eyJ0b2tlbkNvbnRlbnQiOiJ7XCJ1c2VySWRcIjpcIkkzMzYxMjFcIixcImNvbXBhbnlJZFwiOlwiXCIsXCJjbGllbnRJZFwiOlwic3BjXCIsXCJpc3N1ZWRBdFwiOjE2MTU3MzA5Njc4OTMsXCJleHBpcmVzSW5cIjoxODAwLFwiaXNzdWVkRm9yXCI6XCJzZnByb3Zpc2lvbmluZ1wifSIsInNpZ25hdHVyZSI6Img0N3BLeFoxamtmLzM5dGNraVA3U2x2R1p4UnJCL3NwZ1M2SnlROTdla2xReDNYV2tRaC8xRFgrTzFsakRYMHJRdmVtcGRRWVZkNXB1QW84Qno1RUllSk1FWGZCVUVDNk4wR1pqNHltN3NXK3FtVWpGaFM2N0hOZUhhWVNBcVZlaFdiWWN5eG5KcUl5QzlwTTVveG1HWC9XekxOVjJ6bmNleVZuRXpwQnR0MD0ifQ==',
  'Content-Type': 'application/json',
  'Cookie': 'JSESSIONID=A04BE979A5C47E587CEE8ECC72AAF9BF.mc25bcf03; route=8c3993038beeb160f071c039d084762837229a27'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
