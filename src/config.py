from os import environ


class InvalidConfigException(Exception):
    def __init__(self, message):
        super().__init__(message)
        print(message)


class Config:
    def __init__(self):
        if ("PERFORMANCE_GRAPH_OUTPUT_PATH" in environ):
            self.performance_graph_output_path = environ["PERFORMANCE_GRAPH_OUTPUT_PATH"]
        else:
            raise InvalidConfigException(
                "Missing performance graph output path")

        if ("TRANSACTIONS_OUTPUT_PATH" in environ):
            self.transactions_output_path = environ["TRANSACTIONS_OUTPUT_PATH"]
        else:
            raise InvalidConfigException(
                "Missing transactions output path")

    def load(self) -> dict:
        return {"performanceGraphOutputPath": self.performance_graph_output_path,
                "transactionsOutputPath": self.transactions_output_path}
