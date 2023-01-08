from azure.storage.blob import BlobClient
from HttpTrigger1.config import settings

class blobstorage:
    def __init__(self):
        self.data = []

    def store(self, json):
        CONNECTION_STRING = settings['connection_string']
        CONTAINER_NAME = settings['container_name']
        BLOB_NAME = settings['blob_name']

        blob_client = BlobClient.from_connection_string(conn_str=CONNECTION_STRING, container_name=CONTAINER_NAME, blob_name=BLOB_NAME)
        blob_client.upload_blob(json)
