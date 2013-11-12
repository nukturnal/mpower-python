"""MPower Payments Invoice"""
from .core import Payment
from .store import Store

class Invoice(Payment): 
    def __init__(self, store=None,configs={}):
        """Create an invoice

        Accepts list of store object as initial parameter and a dictionary of tokens
        for accessing the MPower Payments API
        """
        self.cancel_url = None
        self.return_url = None
        self.description = None
        self.store = store or Store()
        self.items = []
        self.custom_data = {}
        self.taxes = {}
        super(Invoice, self).__init__(configs)

    def create(self, items=[], taxes=[], custom_data=[]):
        """Adds the items to the invoice

        Format of 'items': [{"name": "VIP Ticket", "quantity": 2,
                       "unit_price": "35.0", "total_price": "70.0", 
                        "description": "VIP Tickets for the MPower Event"},...]
        See the MPower Payments APi for more information on the format of the 'items'
        """
        self.add_items(items)
        self.add_taxes(taxes)
        self.add_custom_data(custom_data)
        return self._process('checkout-invoice/create', self._prepare_data())

    def confirm(self, token):
        """Returns the status of the invoice
        
        STATUSES: pending, completed, cancelled
        """
        return self._process('checkout-invoice/confirm/' + str(token))
        
    def add_taxes(self, taxes=[]):
        """Appends the data to the 'taxes' key in the request object
        
        'taxes' should be in format: [("tax_name", "tax_amount")]
        For example:
        [("NHIs TAX", 23.8), ("VAT", 5)]
        """
        for idx, tax in enumerate(taxes):
          self._taxes.update({"tax_" + str(idx):{"name": tax[0], "amount": tax[1]}})        

    def add_custom_data(self, data=[]):
        """Adds the data to teh custom data sent to the server

        Format of custom data: [("phone_brand", Motorola V3"), ("model", "65456AH23")]
        """
        self._custom_data.update(dict(data))

    def add_items(self, items=[]):
        """Updates the list of items in the current transaction"""
        for idx, item in enumerate(items):
            self.items.update({"item_" + str(idx): item})

    def _prepare_data(self):
        """Formats the data in the current transaction for processing"""
        self._data = {"items": self.items, "taxes": self.taxes, 
                     "total_amount": self.total_amount, "description": self.description,
                     "store": self.store.info, "custom_data": self.custom_data,
                     "actions": {"cancel_url": self.cancel_url, "return_url": self.return_url}
                     }
        return self._data
