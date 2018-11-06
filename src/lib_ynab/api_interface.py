"""
Class for connecting and retrieving data from the YNAB API

YNAB API Endpoints: https://api.youneedabudget.com/v1#/
"""

import os
import requests

# from ipdb import set_trace as db
# from pprint import pprint

API_ENDPOINT = "https://api.youneedabudget.com/v1"

# Make sure we have the YNAB token set as an environmental variable:
YNAB_TOKEN = os.environ.get('YNAB_TOKEN')
if not YNAB_TOKEN:
    raise ValueError("YNAB_TOKEN is not set as an environmental variable")


class YNAB(object):

    def __init__(self):
        """
        Constructor for YNAB API calls
        """

        # Save token:
        self.token = YNAB_TOKEN

        # Determine budget ID:
        budgets = self.api_call("budgets")['budgets']
        if len(budgets) != 1:
            raise ValueError(
                "Received zero or multiple budgets (len = {})".format(
                    len(budgets),
                )
            )
        budget = budgets[0]
        self.budget_id = budget['id']

        return

    def api_call(self, resource, query_params=""):
        """
        General interface to call the YNAB API.
        See the YNAB endpoints at:
            https://api.youneedabudget.com/v1#/


        :param resource: Resource string used for calling the YNAB API
        :param query_params: (optional) Query parameters for the API call

        :return data: Dictionary containing information from the API call
        """

        # Form URL:
        url = "{api_endpoint}/{resource}/{query_params}".format(
            api_endpoint=API_ENDPOINT,
            resource=resource,
            query_params=query_params,
        )

        # Make the request:
        headers = {
            "Authorization": "Bearer {}".format(self.token)
        }
        r = requests.get(
            url,
            headers=headers,
        )

        # Make sure we were succesful in making the request:
        if not r.ok:
            err = "[Status Code = {status_code}] " \
                  "Issue calling the YNAB API: {reason}".format(
                    status_code=r.status_code,
                    reason=r.reason,
                  )
            raise ValueError(err)

        # Form JSON output:
        data = r.json()['data']

        return data

    def get_transactions(self):
        """
        Retrieves transaction data from YNAB

        :return transactions: List of transaction information
        """

        # Call API:
        data = self.api_call(
            "budgets/{budget_id}/transactions".format(
                budget_id=self.budget_id,
            ),
        )

        # Parse for tranactions:
        transactions = data['transactions']

        return transactions
