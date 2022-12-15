import json
from sys import argv
from datetime import date
from session_handler import SessionHandler
from nordnet_api import get_transactions
from nordnet_api import get_performance_graph
from transactions_repository import TransactionsRepository
from performance_graph_repository import PerformanceGraphRepository
from dotenv import DotEnv

dotenv = DotEnv()
dotenv.load()

# Use credentials from environment variables
sessionHandler = SessionHandler()
sessionHandler.login()

# Tranactions returned as Pandas DataFrame
transactions = get_transactions(session=sessionHandler.get_session())
# Performance graph returned as dictionary
performance_graph = get_performance_graph(
    session=sessionHandler.get_session())

if (argv[1] is None or argv[1] == "local" or argv[1] == "file"):
    # TODO: Move configuration to .env / Environment variables
    with open("config.json", "r") as configFile:
        config = json.load(configFile)

        # Store newest transactions page as both CSV and Excel file
        transactions_repository = TransactionsRepository(config)
        transactions_repository.save_transactions(
            "file", transactions)

        # Store Performance Graph
        performance_graph_repository = PerformanceGraphRepository(config)
        performance_graph_repository.save_performance_graph(
            "file", performance_graph)

if (argv[1].lower() == "gcp"):
    # TODO: Use GCP strategy in both repositories
    print("GCP")
