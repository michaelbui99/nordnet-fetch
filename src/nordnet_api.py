import pandas as pd
from io import StringIO
from datetime import datetime
from datetime import date
from requests import Session


def get_transactions(session: Session) -> pd.DataFrame:
    url = "https://www.nordnet.dk/mediaapi/transaction/csv/filtered"

    start_date = '2013-01-01'
    today = date.today()
    end_date = datetime.strftime(today, '%Y-%m-%d')

    params = {
        "locale": "da-DK",
        "from": start_date,
        "to": end_date,
        "account_id": 1
    }

    res = session.get(url=url, params=params)
    content_decoded = res.content.decode("utf-16")
    processed_content = content_decoded.replace("\t", ";")
    transactions_csv_list = processed_content.splitlines()

    transactions_csv = ""

    for row in transactions_csv_list:
        transactions_csv += "{}\n".format(row)

    transactions = pd.read_csv(
        StringIO(transactions_csv), sep=";", header=0)

    transactions["Bogføringsdag"] = pd.to_datetime(
        transactions["Bogføringsdag"])
    transactions["Handelsdag"] = pd.to_datetime(transactions["Handelsdag"])
    transactions["Valørdag"] = pd.to_datetime(transactions["Valørdag"])
    return transactions


def get_performance_graph(session: Session) -> dict:
    url = 'https://www.nordnet.dk/api/2/accounts/1/returns/performance'
    start_date = '2013-01-01'
    today = date.today()
    end_date = datetime.strftime(today, '%Y-%m-%d')

    params = {
        "from": start_date,
        "to": end_date
    }

    return session.get(url=url, params=params).json()
