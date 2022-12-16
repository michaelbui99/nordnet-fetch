from google.cloud import bigquery

project_name = "nordnetdata"
data_set = "dwh"


def insert_latest_performance_tick_date(client: bigquery.Client):
    query = "INSERT INTO `nordnetdata.dwh.etl_metadata` (latest_performance_tick_date) SELECT date FROM `nordnetdata.dwh.performance_graph` order by date DESC LIMIT 1"
    # TODO: Use GCP BigQuery client and target etl_metadata table
    insert_job = client.query(query)
    return insert_job
