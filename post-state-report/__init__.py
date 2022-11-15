import logging
import json
import traceback
import azure.functions as func
from tableStorage import helper_statereports

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
             "Bad Request.",
             status_code=400
        )
    else:
        #Validating body
        req_fields = ('state', 'projectId', 'reportName', 'createdBy', 'reportWindowStartDate', 'reportWindowEndDate', 'reportSubmissionDate','reportData')
        if not all(fields in req_body for fields in req_fields):
            return func.HttpResponse(
                "Bad Request.",
                status_code=400
            )          
        try:  
            helper_statereports.submit_report(req_body)
        except:
            traceback.print_exc()
            return func.HttpResponse(
             "Report could not be submitted, ensure report name is unique OR try after some time",
             status_code=500
            )
        else:
            return func.HttpResponse(
                status_code=204)

