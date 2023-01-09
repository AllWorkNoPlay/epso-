import os


settings = dict(
    connection_string= os.environ.get('CONNECTION_STRING', 'DefaultEndpointsProtocol=https;AccountName=jobdata;AccountKey=nTlCqhfrVghYwblcFjAeIG6C1WE4tPk/TXKABVYph9eRd2zNvZhzsqMEBUdnVXCFrmnpPW289ZOu+AStxBL+Ww==;EndpointSuffix=core.windows.net'),
    container_name = os.environ.get('CONTAINER_NAME', 'jobs'),
    blob_name = os.environ.get('BLOB_NAME', 'jobs-json-local')
    )