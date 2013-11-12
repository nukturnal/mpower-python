import unittest
from mpower.invoice import Invoice as MPInvoice

class Invoice(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self._invoice = MPInvoice()

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self._invoice = None

    def test_create_invoice(self):
        pass

    def test_add_items(self):
        pass

    def test_add_taxes(self):
        pass

    def test_add_custom_data(self):
        pass

