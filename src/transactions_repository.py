from pandas import DataFrame
from abc import ABC, abstractmethod
from config import InvalidConfigException
from typing import Dict
from datetime import date


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
        print(transactions)
        today = date.today()
        transactions.to_csv("{}_{}.csv".format(
            self.config["transactionsOutputPath"], today), sep=";")

        transactions.to_excel("{}_{}.xlsx".format(
            self.config["transactionsOutputPath"], today))


class TransactionsRepository:
    def __init__(self, config):
        self.strategies: Dict[str, SaveTransactionsStrategy] = {
            "file": FileSaveTransactionsStrategy(config)}

    def save_transactions(self, strategy: str, transactions: DataFrame):
        strategy_to_use = self.strategies[strategy]
        strategy_to_use.save(transactions)
