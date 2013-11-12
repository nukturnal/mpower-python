import unittest
from mpower.opr import OPR
from mpower.store import Store
from . import MP_ACCESS_TOKENS


class TestOPR(unittest.TestCase):
    def setUp(self):
        self.opr_data = {'account_alias': '0266636984',
                    'description': 'Hello World',
                    'total_amount': 345}
        store = Store({"name":"FooBar Shop"})
        self.opr = OPR(self.opr_data, store, MP_ACCESS_TOKENS, True)

    def tearDown(self):
        self.opr = None

    def test_opr_create(self):
        status, resp = self.opr.create()
        self.assertTrue(status)

        status, resp = self.opr.create(self.opr_data)
        self.assertTrue(status)

    def test_opr_charge(self):
        status, response = self.opr.create()
        token = response['token']
        status, _ = self.opr.charge({'token':token, 
                                     'confirm_token': "56Y8"})
        # request should because the token and 
        # comfirm_token combination are wrong
        self.assertFalse(status)

if __name__ == '__main__':
    unittest.main()
    
