def insert_latest_performance_tick_date():
    query = "INSERT INTO `nordnetdata.dwh.etl_metadata` (latest_performance_tick_date) SELECT date FROM `nordnetdata.dwh.performance_graph` order by date DESC LIMIT 1"
    # TODO: Use GCP BigQuery client and target etl_metadata table
    print(query)
