import os
from azure.data.tables import TableServiceClient
from azure.data.tables import TableClient

account_key = os.environ['STORAGE_ACCOUNT_KEY']
account_name = os.environ['STORAGE_ACCOUNT_NAME']
connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name}AccountKey={account_key};EndpointSuffix=core.windows.net;BlobEndpoint=https://{account_name}.blob.core.windows.net/;FileEndpoint=https://{account_name}.file.core.windows.net/;QueueEndpoint=https://{account_name}.queue.core.windows.net/;TableEndpoint=https://{account_name}.table.core.windows.net/"

TABLE_SERVICE_CLIENT = TableServiceClient.from_connection_string(conn_str=connection_string)

