MPower Python Client Library
============================

This is a python library for accessing the MPower Payments HTTP API

Installation
------------

.. code-block:: bash

    $ sudo pip install mpower`
    $ OR git clone https://github.com/mawuli-ypa/mpower-python
    $ cd mpower-python; python setup.py install`

Usage
-----

.. code-block:: python

    from mpower import (Invoice, OPR, DirectPay,
                           DirectCard, Store)

    # Your MPower developer tokens
    MP_CONFIGS = {
    'MP-Master-Key': "5b9f531a-fbb8-487a-8045-3b4c7ac5acee",
    'MP-Private-Key': "test_private_oGslgmzSNL3RSkjlsnPOsZZg9IA",
    'MP-Token': "ff1d576409b2587cc1c2",
    }

    store = Store()
    items =  [{"name": "VIP Ticket", "quantity": 2,
                       "unit_price": "35.0", "total_price": "70.0",
                        "description": "VIP Tickets for the MPower Event"}]
    invoice = Invoice(store, MP_CONFIGS)
    invoice.add_items(items)
    # taxes are (key,value) pairs
    invoice.add_taxes([("NHIS TAX", 23.8), ("VAT", 5)])
    invoice.add_custom_data([("phone_brand", Motorola V3"),
                ("model", "65456AH23")])
    successful, response = invoice.process()
    if successful:
        do_something_with_resp(response)


    successful, response = DirectPay("0246XXXXXX", 230.40,
                MP_CONFIGS).process()
    if successful:
       do_something_with_resp(resp)

    card_info = { "card_name" : "Alfred Robert Rowe",
          "card_number" : "4242424242424242", "card_cvc" : "123",
          "exp_month" : "06", "exp_year" : "2010", "amount" : "300"
        }

    direct_card = DirectCard(card_info, MP_CONFIGS)
    successful, response = direct_card.process()
    if successful:
        do_something_with_resp(response)

    # OPR is a two-step process: create OPR and then charge OPR
    opr = OPR(store, MP_CONFIGS)
    successful, response = opr.create({"account_alias": "0246XXXXXX",
    "description": "Sample OPR transaction", "total_amount": 120})
    if successful:
        # token returned from server
        token = response["token"]
        ok, resp = charge_opr({"token": token, "confirm_token": confirm_token})
        if ok:
           do_something_with_response(resp)

        else:
           # take action

LICENSE
-------
see LICENSE.txt


Contributing
------------
Issues, forks, and pull requests are welcome!


NOTE
----
- This is a proof of concept, and the API will suffer major changes
- For more information, please read the  `MPower Payments HTTP API`_

.. _MPower Payments HTTP API: http://mpowerpayments.com/developers/docs/http.html

TODO
----
- Add unitests for both sandbox and live endpoints
- Add code examples
- Remove repeated passing of CONFIGS around functions calls. Ideally, this configs should be passed only once
