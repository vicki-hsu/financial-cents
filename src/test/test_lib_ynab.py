"""
Unit tests for lib_ynab

Run with:
    $ python -m unittest -v test.test_lib_ynab
"""

import unittest

# from ipdb import set_trace as db
# from pprint import pprint

from lib_ynab.api_interface import YNAB


class TestInstantiation(unittest.TestCase):

    def test_is_instance(self):
        """Test basic instantiation"""
        a = YNAB()
        self.assertIsInstance(a, YNAB)

    def test_is_initialized(self):
        """Test YNAB class constructor sets attributes"""
        a = YNAB()

        # We should have a token and budget ID associated with the instance:
        self.assertIsNotNone(a.token)
        self.assertIsNotNone(a.budget_id)


class TestApiInterface(unittest.TestCase):

    def setUp(self):

        # Initialize:
        self.ynab = YNAB()

        # Expected transaction keys from API
        self.transaction_keys = [
            'account_id',
            'account_name',
            'amount',
            'approved',
            'category_id',
            'category_name',
            'cleared',
            'date',
            'deleted',
            'flag_color',
            'id',
            'import_id',
            'memo',
            'payee_id',
            'payee_name',
            'subtransactions',
            'transfer_account_id',
            'transfer_transaction_id',
        ]

    def tearDown(self):
        pass

    def test_get_transactions(self):

        # Find the transactions:
        transactions = self.ynab.get_transactions()

        # We should have transactions available:
        self.assertTrue(transactions)

        # We should have all the transaction keys for each transaction:
        for transaction in transactions:
            for transaction_key in self.transaction_keys:
                self.assertIn(transaction_key, transaction)
