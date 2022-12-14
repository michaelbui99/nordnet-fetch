from google.cloud import bigquery

project_name = "nordnetdata"
data_set = "dwh"


def insert_latest_performance_tick_date(client: bigquery.Client):
    truncate = "TRUNCATE TABLE `nordnetdata.dwh.etl_metadata`"
    query = "INSERT INTO `nordnetdata.dwh.etl_metadata` (latest_performance_tick_date) SELECT date FROM `nordnetdata.dwh.performance_graph` order by date DESC LIMIT 1"
    # TODO: Use GCP BigQuery client and target etl_metadata table
    truncate_job = client.query(truncate)
    truncate_job.add_done_callback(client.query(query))
