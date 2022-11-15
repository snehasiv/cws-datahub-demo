import logging
import json
import traceback
import azure.functions as func
from tableStorage import helper_statereports

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    state = ''
    projectId = ''
    try:
         state = req.params.get('state')
         projectId = req.params.get('projectId')
    except:
        pass
    records = []
    if state!='' or projectId !='' :
        records = helper_statereports.get_records(state, projectId)
    else:
        records = helper_statereports.get_all_records()
    
    records_json = json.dumps(records, indent=4, sort_keys=True, default=str)
    return func.HttpResponse( records_json,status_code=200, 
        mimetype="application/json")   


