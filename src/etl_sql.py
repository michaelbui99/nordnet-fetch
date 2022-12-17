import pandas as pd
from google.cloud import bigquery

project_name = "nordnetdata"
data_set = "dwh"


def insert_latest_performance_tick_date(client: bigquery.Client):
    query = "INSERT INTO `nordnetdata.dwh.etl_metadata` (latest_performance_tick_date) SELECT date FROM `nordnetdata.dwh.performance_graph` order by date DESC LIMIT 1"
    insert_job = client.query(query)
    return insert_job


def insert_performance_graph_data(client: bigquery.Client, performance_graph: pd.DataFrame):
    for index, row in performance_graph.iterrows():
        sql = "INSERT INTO nordnetdata.dwh.performance_graph (time, date, accumulated_returns, returns, accumulated_result_currency, accumulated_result_value, result_currency) VALUES ({}, \"{}\", {}, {}, \"{}\", {}, \"{}\")".format(
            str(row["time"]), row["date"].date(), row["accumulated_returns"], row["returns"], str(row["accumulated_result.currency"]), row["accumulated_result.value"], str(row["result.currency"]))
        insert_job = client.query(sql)
        while (not insert_job.done()):
            print("Waiting for insert...")
    print(f"Inserted {performance_graph.shape[0]} rows")


def select_latest_performance_tick_date(client: bigquery.Client) -> str:
    latest_tick_date_job = client.query(
        "SELECT latest_performance_tick_date from `nordnetdata.dwh.etl_metadata` ORDER BY latest_performance_tick_date DESC LIMIT 1")
    latest_tick_date = None

    for row in latest_tick_date_job:
        latest_tick_date = pd.to_datetime(
            row["latest_performance_tick_date"])
    return latest_tick_date
