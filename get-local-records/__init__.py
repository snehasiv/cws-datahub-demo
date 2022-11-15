import logging
from tableStorage import helper_localrecords
import json
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    state = ''
    projectId = ''
    pincode=''
    activityName= ''
    submittedBefore =''
    submittedAfter = ''
    try:
         state = req.params.get('state')
         projectId = req.params.get('projectId')
         pincode = req.params.get('pincode')
         activityName = req.params.get('activityName')
         submittedBefore = req.params.get('submittedBefore')
         submittedAfter = req.params.get('submittedAfter')
    except:
        pass
    records = []
    if state!='' or projectId !='' or pincode!='' or activityName!='' or submittedBefore!='' or submittedAfter!='':
        records = helper_localrecords.get_records(state, projectId, pincode, activityName, submittedBefore, submittedAfter)
    else:
        records = helper_localrecords.get_all_records()
    
    records_json = json.dumps(records, indent=4, sort_keys=True, default=str)
    return func.HttpResponse( records_json,status_code=200, 
        mimetype="application/json")   
