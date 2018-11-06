#!/usr/bin/env python3
""" Example program that utilizes the YNAB interface library """

import pandas as pd

# from ipdb import set_trace as db
# from pprint import pprint

import lib_ynab

if __name__ == "__main__":

    # Instantiate YNAB interface
    ynab = lib_ynab.api_interface.YNAB()

    # Grab the transactions:
    transactions = ynab.get_transactions()

    # Form a Panda DataFrame:
    df = pd.DataFrame(transactions)

    # Report some basic spending information:
    print("Here's our spending data:")
    print(df[['date', 'category_name', 'amount']])
