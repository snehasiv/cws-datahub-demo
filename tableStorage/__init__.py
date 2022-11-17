import os
from azure.data.tables import TableServiceClient
from azure.data.tables import TableClient


connection_string = os.environ['STORAGE_ACCOUNT_CONNECTION_STRING']

TABLE_SERVICE_CLIENT = TableServiceClient.from_connection_string(conn_str=connection_string)

