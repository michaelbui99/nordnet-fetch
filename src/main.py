import json
from datetime import date
from session_handler import SessionHandler
from nordnet_api import get_transactions
from nordnet_api import get_performance_graph


with open("config.json", "r") as configFile:
    config = json.load(configFile)

    # Use credentials from environment variables
    sessionHandler = SessionHandler()
    sessionHandler.login()

    # Tranactions returned as Pandas DataFrame
    transactions = get_transactions(session=sessionHandler.get_session())

    # Performance graph returned as dictionary
    performance_graph = get_performance_graph(
        session=sessionHandler.get_session())

    today = date.today()

    # Store newest transactions page as both CSV and Excel file
    transactions.to_csv("{}_{}.csv".format(
        config["transactionsOutputPath"], today), sep=";")

    transactions.to_excel("{}_{}.xlsx".format(
        config["transactionsOutputPath"], today))

    # Store Performance Graph
    with open("{}_{}.json".format(config["performanceGraphOutputPath"], today), "w") as performanceJsonFile:
        performanceJsonFile.write(json.dumps(performance_graph))
