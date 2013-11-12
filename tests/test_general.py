import os
import unittest
from mpower.opr import OPR
from mpower.store import Store
from . import MP_ACCESS_TOKENS


class TestGeneral(unittest.TestCase):
    """General/Miscellaneous tests"""
    def setUp(self):
        # Your MPower developer tokens
        self.store = Store({"name":"FooBar store"})
        self.opr_data = {'total_amount': 345, 'description': "Hello World", 
                    "account_alias":"0266636984"}
        self.opr = OPR(self.opr_data, self.store)

    def tearDown(self):
        self.opr = None
        self.store = None
        self.opr_data = None

    def test_runtime_configs(self):
        self.assertEqual(MP_ACCESS_TOKENS, 
                         self.opr.runtime_configs)

    def test_system_configs_env(self):
        os.environ['MP-Master-Key'] = "5b9f531a-fbb8-487a-8045-3b4c7ac5acee"
        os.environ['MP-Private-Key'] = "test_private_oGslgmzSNL3RSkjlsnPOsZZg9IA"
        os.environ['MP-Token'] = "ff1d576409b2587cc1c2"
        self.assertTrue(self.opr.config)
        

    def test_rsc_endpoints(self):
        endpoint = 'checkout-invoice/confirm/test_98567JGF'
        url= self.opr.get_rsc_endpoint(endpoint)
        self.assertTrue(url.startswith('https') and url.endswith(endpoint))

    def test_add_headers(self):
        header = {'Foo':'Bar'}
        self.opr.add_header(header)
        self.assertTrue("Foo" in self.opr.headers.keys())
        self.assertFalse('FooBar' in self.opr.headers.keys())


if __name__ == '__main__':
    unittest.main()
