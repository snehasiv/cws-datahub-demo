from azure.data.tables import TableServiceClient
from datetime import datetime
import json
from tableStorage import TABLE_SERVICE_CLIENT
from . import helpers
from azure.data.tables import UpdateMode

TABLE_CLIENT = TABLE_SERVICE_CLIENT.get_table_client(table_name="statereportslog")


def submit_report(data, diff):
	entity = {
    	u'PartitionKey': f"{data.get('reportName')}_{data.get('reportSubmissionDate')}",
    	u'RowKey': datetime.today().strftime('%Y-%m-%d'),
    	u'ModifiedBy': f"{data.get('createdBy')}",
    	u'ChangesMade': diff
	}

	entity = TABLE_CLIENT.create_entity(entity=entity)
	return entity

def get_records(partitionKey):
	my_filter = f"PartitionKey eq '{partitionKey}'"
	
	entities = TABLE_CLIENT.query_entities(my_filter)
	return helpers.generate_list_response(entities)

def get_all_records():
	entities= TABLE_CLIENT.list_entities()
	return helpers.generate_list_response(entities)

def get_record(partitionKey, rowKey):
	got_entity = TABLE_CLIENT.get_entity(partition_key=partitionKey, row_key=rowKey)
	return got_entity


