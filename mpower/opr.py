"""MPower Payments Onsite Payments Request"""
from .core import Payment
from .store import Store

class OPR(Payment):
    """Onsite Payment Request"""
    def __init__(self, store=None, configs={}):
        self.store = store or Store()
        super(OPR,self).__init__(configs)

    def create(self, data, store=None):
        """Initiazes an OPR

        First step in the OPR process is to create the OPR request.
        Returns the OPR token
        """
        _store = store or self.store 
        _data = {"invoice_data" : {"invoice": 
                                   {"total_amount": data.get("total_amt"),
                                    "description": data.get("description")}, 
                                   "store": _store.info},
                 "opr_data" :{"account_alias" : data.get("account_alias")}}
        return self._process('opr/create', _data)

    def charge(self, data):
        """Second stage of an OPR request"""
        token =  data.get("token", self._response["token"])
        data = {"token": token, "confirm_token": data.get("confirm_token")}
        return self._process('opr/charge', data)
