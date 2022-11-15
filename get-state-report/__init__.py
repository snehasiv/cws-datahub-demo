import logging
from tableStorage import helper_statereports
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    partitionKey = req.params.get('partitionKey')
    rowKey = req.params.get('rowKey')

    if not partitionKey or not rowKey:
        return func.HttpResponse(
                "Bad Request. Please provide all required filters.",
                status_code=400)   

    report = helper_statereports.get_report(partitionKey, rowKey)
    report_json = json.dumps(report, indent=4, sort_keys=True, default=str)
    return func.HttpResponse( report_json,status_code=200, 
        mimetype="application/json")   
