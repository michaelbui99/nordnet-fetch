import json
from abc import ABC, abstractmethod
from config import InvalidConfigException
from typing import Dict
from datetime import date


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
        with open("{}_{}.json".format(self.config["performanceGraphOutputPath"], today), "w") as performanceJsonFile:
            performanceJsonFile.write(json.dumps(performance_graph))


class PerformanceGraphRepository:
    def __init__(self, config):
        self.strategies: Dict[str, SavePerformanceGraphStrategy] = {
            "file": FileSavePerformanceGraphStrategy(config)}

    def save_performance_graph(self, strategy: str, performance_graph: dict):
        self.strategies[strategy].save(performance_graph)
