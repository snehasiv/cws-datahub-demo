from azure.data.tables import TableServiceClient
from datetime import datetime
import json
from tableStorage import TABLE_SERVICE_CLIENT
from . import helpers
from azure.data.tables import UpdateMode

TABLE_CLIENT = TABLE_SERVICE_CLIENT.get_table_client(table_name="statereports")


def submit_record(data):
	entity = {
    	u'PartitionKey': f"{data.get('projectId')}_{data.get('state')}",
    	u'RowKey': f"{data.get('reportName')}_{data.get('reportSubmissionDate')}",
    	u'State': f"{data.get('state')}",
    	u'ReportName': f"{data.get('reportName')}",
    	u'ProjectId': f"{data.get('projectId')}",
    	u'CreatedBy': f"{data.get('createdBy')}",
    	u'ReportWindowStartDate': datetime.strptime(data.get('reportWindowStartDate'), '%Y-%m-%d'),
    	u'ReportWindowEndDate': datetime.strptime(data.get('reportWindowEndDate'), '%Y-%m-%d'),
    	u'ReportSubmissionDate': datetime.strptime(data.get('reportSubmissionDate'), '%Y-%m-%d'),
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
		u'LastRecord': old_entity.get('data')
	}
	new_entity = TABLE_CLIENT.update_entity(mode=UpdateMode.MERGE, entity=entity)
	return new_entity

