MPower Python Client Library
============================

This is a python library for accessing the MPower Payments HTTP API


Installation
------------

.. code-block:: bash

    $ sudo pip install mpower
    $ OR git clone https://github.com/nukturnal/mpower-python
    $ cd mpower-python; python setup.py install`
    $ python setup.py test # run unit tests

Usage
-----

.. code-block:: python

    from mpower import (Invoice, OPR, DirectPay,
                           DirectCard, Store)

    # Invoice
    store = Store({'name':'FooBar Shop'})
    items = [{"name": "VIP Ticket", "quantity": 2,
         "unit_price": "35.0", "total_price": "70.0",
         "description": "VIP Tickets for the MPower Event"}]
    invoice = Invoice(self.store, MP_ACCESS_TOKENS, True)
    invoice.add_items(self.items * 10)
    # taxes are (key,value) pairs
    invoice.add_taxes([("NHIS TAX", 23.8), ("VAT", 5)])
    invoice.add_custom_data([("phone_brand", "Motorola V3"),
                ("model", "65456AH23")])

    # you can also pass the items, taxes, custom to the `create` method
    successful, response = invoice.create()
    if successful:
        do_something_with_resp(response)

    # confirm invoice
    invoice.confirm(response['token'])


    # OPR
    opr_data = {'account_alias': '0266636984',
                'description': 'Hello World',
                 'total_amount': 345}
    store = Store({"name":"FooBar Shop"})
    opr = OPR(self.opr_data, store, MP_ACCESS_TOKENS, True)
    # You can also pass the data to the `create` function
    successful, response = opr.create()
    if successful:
       do_something_with_response(response)
    status, _ = opr.charge({'token': token,
                    'confirm_token': user_submitted_token})


    # Direct card
    card_info = {"card_name" : "Alfred Robert Rowe",
        "card_number" : "4242424242424242", "card_cvc" : "123",
        "exp_month" : "06", "exp_year" : "2010", "amount" : "300"
    }
    direct_card = DirectCard(card_info, MP_ACCESS_TOKENS, True)
    # this request should fail since the card_info data is invalid
    successful, response = direct_card.process()


    # Direct Pay
    account_alias =  "0266636984"
    amount =  30.50
    # toggle debug switch to True
    direct_pay = DirectPay(account_alias, amount, MP_ACCESS_TOKENS, True)
    status, response = direct_pay.process()


License
-------
see LICENSE.txt


Contributing
------------
Issues, forks, and pull requests are welcome!


Note
----
- You can also set the following system/shell variables for use with library:
  MP_Master_Key, MP_Public_Key, MP_Token
- OR, use *MP_ACCESS_TOKENS* as the variable name that holds your
  MPower Payments Access Tokens.
  For example: MP_ACCESS_TOKENS = {"MP-Master-key": "ATGHJIUTF", ...}.
  This variable is picked up at runtime as a measure of last resort
- This is a proof of concept, and the API will suffer major changes
- Some of the API calls require formal approval from MPower Payments
- This library has not being used in any production environment, yet.
- For more information, please read the  `MPower Payments HTTP API`_

.. _MPower Payments HTTP API: http://mpowerpayments.com/developers/docs/http.html
