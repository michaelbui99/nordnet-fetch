import pandas as pd
import json
from google.cloud import bigquery
from abc import ABC, abstractmethod
from config import InvalidConfigException
from typing import Dict
from datetime import date
from datetime import datetime
from etl_sql import insert_latest_performance_tick_date, data_set, project_name


class SavePerformanceGraphStrategy(ABC):
    @abstractmethod
    def save(self, performance_graph: dict):
        pass


class FileSavePerformanceGraphStrategy(SavePerformanceGraphStrategy):
    def __init__(self, config: dict):
        self.config = config
        if ("performanceGraphOutputPath" not in config):
            raise InvalidConfigException("Invalid configuration file")

    def save(self, performance_graph: dict):
        today = date.today()
        df = pd.DataFrame.from_dict(performance_graph)

        performance_ticks_flattened = pd.json_normalize(
            df["performance_ticks"][0])
        performance_ticks_flattened["date"] = pd.to_datetime(
            performance_ticks_flattened["date"])

        performance_ticks_flattened.set_index("time", inplace=True)

        performance_ticks_flattened.to_csv("{}_{}.csv".format(
            self.config["performanceGraphOutputPath"], today), sep=";")
        performance_ticks_flattened.to_excel("{}_{}.xlsx".format(
            self.config["performanceGraphOutputPath"], today))
        with open("{}_{}.json".format(self.config["performanceGraphOutputPath"], today), "w") as performanceJsonFile:
            performanceJsonFile.write(json.dumps(performance_graph))


class BigQuerySavePerformanceGraphStrategy(SavePerformanceGraphStrategy):
    def __init__(self):
        self.client = bigquery.Client()

    def save(self, performance_graph: dict):
        df = pd.DataFrame.from_dict(performance_graph)
        performance_ticks_flattened = pd.json_normalize(
            df["performance_ticks"][0])
        performance_ticks_flattened["date"] = pd.to_datetime(
            performance_ticks_flattened["date"])
        # performance_ticks_flattened.set_index("time", inplace=True)
        insert_latest_performance_tick_date(self.client)

        latest_tick_date_job = self.client.query(
            "SELECT latest_performance_tick_date from `nordnetdata.dwh.etl_metadata` ORDER BY latest_performance_tick_date DESC LIMIT 1")
        latest_tick_date = None

        for row in latest_tick_date_job:
            latest_tick_date = pd.to_datetime(
                row["latest_performance_tick_date"])

        performance_ticks_to_add: pd.DataFrame = performance_ticks_flattened[(
            performance_ticks_flattened["date"] > datetime.strptime(str(latest_tick_date), "%Y-%m-%d %H:%M:%S"))]

        for index, row in performance_ticks_to_add.iterrows():
            sql = "INSERT INTO nordnetdata.dwh.performance_graph (time, date, accumulated_returns, returns, accumulated_result_currency, accumulated_result_value, result_currency) VALUES ({}, \"{}\", {}, {}, \"{}\", {}, \"{}\")".format(
                str(row["time"]), row["date"].date(), row["accumulated_returns"], row["returns"], str(row["accumulated_result.currency"]), row["accumulated_result.value"], str(row["result.currency"]))
            insert_job = self.client.query(sql)
            while (not insert_job.done()):
                print("Inserting...")


class PerformanceGraphRepository:
    def __init__(self, config):
        self.strategies: Dict[str, SavePerformanceGraphStrategy] = {
            "file": FileSavePerformanceGraphStrategy(config), "bigQuery": BigQuerySavePerformanceGraphStrategy()}

    def save_performance_graph(self, strategy: str, performance_graph: dict):
        self.strategies[strategy].save(performance_graph)
