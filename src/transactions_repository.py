from pandas import DataFrame
from abc import ABC, abstractmethod
from config import InvalidConfigException
from typing import Dict
from datetime import date
from bigquery_client_factory import BigQueryClientFactory


class SaveTransactionsStrategy(ABC):
    @abstractmethod
    def save(self, transactions: DataFrame):
        pass


class FileSaveTransactionsStrategy(SaveTransactionsStrategy):
    def __init__(self, config: dict):
        self.config = config
        if ("transactionsOutputPath" not in config):
            raise InvalidConfigException("Invalid configuration file")

    def save(self, transactions: DataFrame):
        today = date.today()
        transactions.set_index("Id", inplace=True)
        transactions.to_csv("{}_{}.csv".format(
            self.config["transactionsOutputPath"], today), sep=";")

        transactions.to_excel("{}_{}.xlsx".format(
            self.config["transactionsOutputPath"], today))


class BigQuerySaveTransactionsStrategy(SaveTransactionsStrategy):
    def __init__(self):
        self.client = BigQueryClientFactory().create()

    def save(self, transactions: DataFrame):
        # TODO: Clean nulls before inserting


class TransactionsRepository:
    def __init__(self, config):
        self.strategies: Dict[str, SaveTransactionsStrategy] = {
            "file": FileSaveTransactionsStrategy(config)}

    def save_transactions(self, strategy: str, transactions: DataFrame):
        strategy_to_use = self.strategies[strategy]
        strategy_to_use.save(transactions)
