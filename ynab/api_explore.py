"""
Class for connecting and retrieving data from the YNAB API

YNAB API Endpoints: https://api.youneedabudget.com/v1#/
"""

import os
import requests

from ipdb import set_trace as db
from pprint import pprint

API_ENDPOINT = "https://api.youneedabudget.com/v1"

YNAB_TOKEN = os.environ.get('YNAB_TOKEN')
# Make sure we have the YNAB token set as an environmental variable:
if not YNAB_TOKEN:
    raise ValueError("YNAB_TOKEN is not set as an enviornmental variable")


class Category(object):
    def __init__(self, name, id):
        self.name = name
        self.id = id

        return


class YNAB(object):

    def __init__(self):

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

        # Define categories:
        self.categories = self.get_categories()

        # Find category_names:
        self.category_names = sorted(
            [category.name for category in self.categories]
        )

        return

    def api_call(self, resource, query_params=""):
        """


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

    def get_categories(self):
        """

        """

        data = self.api_call(
            "budgets/{budget_id}/categories".format(
                budget_id=self.budget_id,
            )
        )

        category_groups = data['category_groups']

        my_categories = []
        for category_group in category_groups:

            hidden = category_group['hidden']
            deleted = category_group['deleted']

            if not hidden and not deleted:
                categories = category_group['categories']

                for category in categories:
                    my_categories.append(
                        Category(
                            category['name'],
                            category['id'],
                        )
                    )
        return my_categories

    def get_category_id_by_name(self, name):
        """

        """

        for category in self.categories:
            if category.name == name:
                return category.id

        return None

    def get_category_transactions(self, name):
        """

        """

        id = self.get_category_id_by_name(name)

        data = self.api_call(
            "budgets/{budget_id}/categories/{category_id}/transactions".format(
                budget_id=self.budget_id,
                category_id=id,
            )
        )

        transactions = data['transactions']

        for transaction in transactions:
            date = transaction['date']
            payee_name = transaction['payee_name']
            amount = transaction['amount']

            print(
                "[{date}]: {payee_name:>50s}: ${amount:3.2f}".format(
                    date=date,
                    payee_name=payee_name,
                    amount=float(-1*amount)/1e3,
                )
            )


if __name__ == "__main__":

    ynab = YNAB()

    ynab.get_category_transactions('Dining')
