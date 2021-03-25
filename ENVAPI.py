# Add any new environment here, no need to add slash at the end..
ENVIRONMENT_URL = {
    "dc25_qaautocand": "https://qaautocand.hcm.ondemand.com",
    "dc25_qacand": "https://qacand.hcm.ondemand.com",
    "dc25_qademouxr": "https://qademouxr.hcm.ondemand.com",
    "dc25_qavies": "https://qavies.hcm.ondemand.com",
    "dc25_qavdemosac": "https://qademosac.hcm.ondemand.com",
    "dc25_qacandies": "https://qacandies.hcm.ondemand.com"
}
WEBSERVICE_PATHS = {
    "generatetoken": "/api/oauth/rest/v1/token",
    "exportCompanyData": "/provisioningapi/provisioning/rest/v1/company/getCompanyBeanAndExportCompanyData",
    "checkstatus": "/provisioningapi/provisioning/rest/v1/company/status",
    "importCompanyData": "/provisioningapi/provisioning/rest/v1/company/importCompanyData",
}

requestUserId="SPCPROV"
dumpPath="/tenantrefresh_trg/i336121/"
timeout=1800