import logging
import json
import traceback
from jsondiff import diff
import azure.functions as func
from tableStorage import helper_statereports
from tableStorage import helper_statereportlogs


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
        req_fields = ('updatedBy', 'partitionKey', 'rowKey', 'reportData')
        not_allowed_fields = ('state', 'projectId', 'createdBy', 'reportName', 'reportSubmissionDate')

        if not all(fields in req_body for fields in req_fields):
            return func.HttpResponse(
                f"Bad Request. Required fields {req_fields} not present.",
                status_code=400
            )
        if any(fields in req_body for fields in not_allowed_fields):
            return func.HttpResponse(
                f"Bad Request. Cannot edit following properties: {not_allowed_fields}",
                status_code=400
            )  
        try:  
            report = helper_statereports.get_record(req_body['partitionKey'], req_body['rowKey'])
            helper_statereports.update_record(req_body['partitionKey'], req_body['rowKey'],req_body)
            #add trace event
            changed = diff(req_body.get('data'), report.get('Data'))

            helper_statereportlogs.submit_record(req_body, str(changed))
        except:
            traceback.print_exc()
            return func.HttpResponse(
             "Report update could not be submitted.",
             status_code=500
            )
        else:
            return func.HttpResponse(
                status_code=204)

