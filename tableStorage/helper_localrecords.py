from azure.data.tables import TableServiceClient
from datetime import datetime
import json
from tableStorage import TABLE_SERVICE_CLIENT
from . import helpers

TABLE_CLIENT = TABLE_SERVICE_CLIENT.get_table_client(table_name="localrecords")


def submit_record(data):
	entity = {
    	u'PartitionKey': f"{data.get('projectId')}_{data.get('state')}",
    	u'RowKey': f"{data.get('pincode')}_{data.get('recordId')}",
    	u'State': f"{data.get('state')}",
    	u'Pincode': f"{data.get('pincode')}",
    	u'ActivityName': f"{data.get('activityName')}",
    	u'ProjectId': f"{data.get('projectId')}",
    	u'RecordId': f"{data.get('recordId')}",
    	u'SubmittedBy': f"{data.get('submittedBy')}",
    	u'SubmissionDate': datetime.strptime(data.get('submissionDate'), '%Y-%m-%d'),
    	u'Data': json.dumps(data.get('data'))
	}

	entity = TABLE_CLIENT.create_entity(entity=entity)
	return entity

def get_records(state, projectId, pincode, activityName, submittedBefore, submittedAfter):
	my_filter = ""
	if state !='' and projectId !='':	
		my_filter = f" PartitionKey eq '{projectId}_{state}'"
	elif state !='':
		my_filter = f" State eq '{state}'"
	elif projectId !='':
		my_filter = f" ProjectId eq '{projectId}'"

	if pincode!=None and pincode != '':
		my_filter += f" and Pincode eq '{pincode}'"
	if activityName!=None and activityName != '':
		my_filter += f" and ActivityName eq '{activityName}'"
	if submittedBefore!=None and submittedBefore != '':
		my_filter += f" and SubmissionDate le '{datetime.strptime(submittedBefore, '%Y-%m-%d')}'"
	if submittedAfter!=None and submittedAfter != '':
		my_filter += f" and SubmissionDate ge '{datetime.strptime(submittedAfter, '%Y-%m-%d')}'"

	if my_filter.startswith(" and"):
		my_filter = my_filter.removeprefix(" and")
		
	
	entities = TABLE_CLIENT.query_entities(my_filter)
	return helpers.generate_list_response(entities)


def get_all_records():
	entities= TABLE_CLIENT.list_entities()
	return helpers.generate_list_response(entities)

def get_record(partitionKey, rowKey):
	got_entity = TABLE_CLIENT.get_entity(partition_key=partitionKey, row_key=rowKey)
	return got_entity

