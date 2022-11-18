import logging
import json
import traceback
import azure.functions as func
from tableStorage import helper_statereportlogs

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    reportName = req.params.get('reportName')
    reportSubmissionDate = req.params.get('reportSubmissionDate')

    if not reportName or not reportSubmissionDate:
        return func.HttpResponse(
                "Bad Request. Please provide all required filters.",
                status_code=400)   

    report = helper_statereportlogs.get_records(f"{reportName}_{reportSubmissionDate}")
    report_json = json.dumps(report, indent=4, sort_keys=True, default=str)
    return func.HttpResponse( report_json,status_code=200, 
        mimetype="application/json")   


