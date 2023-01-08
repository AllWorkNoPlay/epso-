
settings = {
    'host': os.environ.get('ACCOUNT_HOST', 'https://wr-epso.documents.azure.com:443/'),
    'master_key': os.environ.get('ACCOUNT_KEY', '2QSLJRiHCarFJm5duZaoXhxS4fNdrP641IUyQnAbPkc4mwBGktvEvmOMWAuXnZ25S00bZMoyJ09kACDbfRLaQQ=='),
    'database_id': os.environ.get('COSMOS_DATABASE', 'wr-epso'),
    'container_id': os.environ.get('COSMOS_CONTAINER', 'jobs'),
}

HOST = settings['host']
MASTER_KEY = settings['master_key']
DATABASE_ID = settings['database_id']
CONTAINER_ID = settings['container_id']

def update_db(job_rows):
    # Connect to the Cosmos DB account
    client = azure.cosmos.CosmosClient(url_connection=HOST, auth={
        'masterKey': MASTER_KEY
    })

    # Get the database and collection
    database = client.get_database_client(DATABASE_ID)
    container = database.get_container_client(CONTAINER_ID)


    # Iterate over the job-row items
    for job_row in job_rows:
        # Create a JobRow object for the job-row item
        job_row_obj = JobRow(job_row)

        # Extract the desired information from the JobRow object
        title = job_row_obj.title
        domain = job_row_obj.domain
        institution = job_row_obj.institution
        location = job_row_obj.location
        deadline = job_row_obj.deadline

        # Create a dictionary to store the data
        data = {
            'title': title,
            'domain': domain,
            'institution': institution,
            'location': location,
            'deadline': deadline
        }

        # Upsert the data into the Cosmos DB collection
        container.create_item(data, if_exists='replace')
