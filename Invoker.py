import time

from CheckStatus import check_status
from ENVAPI import ENVIRONMENT_URL, timeout
from ExportAPI import export_company_bean
from GenerateToken import generate_token
from ImportAPI import import_company_data
from JsonRead import getExportPayLoad, prepareImportPayLoad, getImportPayLoad

sourceEnvironment = "dc25_qacand"
sourceCompanyID = "ECLila"
targetEnvironment = "dc25_qacand"
targetCompanyId = "ECLilaaa"
targetCompanyName = "ECLilaaa"
targetPoolID = "dbPool1"

source_environment_url = ENVIRONMENT_URL[sourceEnvironment]
sourceToken = generate_token(source_environment_url)
exportCompanyResponse = export_company_bean(source_environment_url, sourceToken, sourceCompanyID, sourceEnvironment)
export_check_payload = getExportPayLoad(exportCompanyResponse[0])
full_dump_path = exportCompanyResponse[1]

t_end = time.time() + timeout
exportCheckFlag = False
while time.time() < t_end:
    print("Checking status.... ")
    status_code = check_status(source_environment_url, sourceToken, export_check_payload)
    if status_code == 200:
        exportCheckFlag = True
    time.sleep(10)
    if exportCheckFlag:
        break

if not exportCheckFlag:
    print("can't check status in 30 minutes.. exiting the export")
    exit(1)

# Export successful, prepare payLoad for import API and call it

payLoadForImport = prepareImportPayLoad(exportCompanyResponse[0], targetCompanyId, targetCompanyName, sourceCompanyID,
                                        targetPoolID, full_dump_path)
target_environment_url = ENVIRONMENT_URL[targetEnvironment]
targetToken = generate_token(target_environment_url)

importCompanyResponse = import_company_data(target_environment_url, targetToken, payLoadForImport)
import_check_payload = getImportPayLoad(importCompanyResponse)

t_end = time.time() + timeout
importCheckFlag = False
while time.time() < t_end:
    print("Checking status of import.... ")
    status_code = check_status(target_environment_url, targetToken, import_check_payload)
    if status_code == 200:
        importCheckFlag = True
    time.sleep(10)
    if importCheckFlag:
        break

if not importCheckFlag:
    print("can't check status in 30 minutes.. exiting the import")
    exit(1)
