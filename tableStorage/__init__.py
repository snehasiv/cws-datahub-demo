import os
from azure.data.tables import TableServiceClient
from azure.data.tables import TableClient

account_key = os.environ['STORAGE_ACCOUNT_KEY']
connection_string = "DefaultEndpointsProtocol=https;AccountName=cwsdatahub1;AccountKey=" + account_key + ";EndpointSuffix=core.windows.net;BlobEndpoint=https://cwsdatahub1.blob.core.windows.net/;FileEndpoint=https://cwsdatahub1.file.core.windows.net/;QueueEndpoint=https://cwsdatahub1.queue.core.windows.net/;TableEndpoint=https://cwsdatahub1.table.core.windows.net/"

TABLE_SERVICE_CLIENT = TableServiceClient.from_connection_string(conn_str=connection_string)

