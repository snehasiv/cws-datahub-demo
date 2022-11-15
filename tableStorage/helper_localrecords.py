from azure.data.tables import TableServiceClient
from datetime import datetime
import json
from tableStorage import TABLE_SERVICE_CLIENT
from . import helpers
from azure.data.tables import UpdateMode

TABLE_CLIENT = TABLE_SERVICE_CLIENT.get_table_client(table_name="localrecords")


def submit_report(data):
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
    	u'Data': json.dumps(data.get('reportData'))
	}

	entity = TABLE_CLIENT.create_entity(entity=entity)
	return entity

def get_records(state = None, projectId = None):
	my_filter = ""
	if state != None and projectId != None:	
		my_filter = f"PartitionKey eq '{projectId}_{state}'"
	elif state != None:
		my_filter = f"State eq '{state}'"
	elif projectId != None:
		my_filter = f"ProjectId eq '{projectId}'"

	
	entities = TABLE_CLIENT.query_entities(my_filter)
	return helpers.generate_list_response(entities)

def get_all_records():
	entities= TABLE_CLIENT.list_entities()
	return helpers.generate_list_response(entities)

def get_record(partitionKey, rowKey):
	got_entity = TABLE_CLIENT.get_entity(partition_key=partitionKey, row_key=rowKey)
	return got_entity

def update_record(partitionKey, rowKey, data):
	old_entity = get_report(partitionKey, rowKey)
	
	entity = {
		u'PartitionKey': partitionKey,
		u'RowKey': rowKey,
		u'UpdatedBy': data['updatedBy'], 
		u'Data': json.dumps(data.get('reportData')),
		u'LastRecord': old_entity.get('Data')
	}
	new_entity = TABLE_CLIENT.update_entity(mode=UpdateMode.MERGE, entity=entity)
	return new_entity

