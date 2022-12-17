from google.cloud import bigquery
from google.oauth2 import service_account
from os import environ


class BigQueryClientFactory:
    def __init__(self):
        self.KEY_PATH_ENV = "GCP_KEY_PATH"
        self.key_path = ""

    def create(self) -> bigquery.Client:
        if (self.KEY_PATH_ENV in environ):
            self.key_path = environ[self.KEY_PATH_ENV]
            credentials = service_account.Credentials.from_service_account_file(
                self.key_path, scopes=[
                    "https://www.googleapis.com/auth/cloud-platform"],
            )
            return bigquery.Client(credentials=credentials, project=credentials.project_id)
        else:
            # If no GCP service account key path, assume Application Default Credentials are provided
            return bigquery.Client()
