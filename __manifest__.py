# -*- coding: utf-8 -*-
{
    "name": "Multi Invoice Reconciliation | Invoice Partial Payment Reconcile Reconciliation",
    'version': '1.0',
    'author': 'Preway IT Solutions',
    'category': 'Point of Sale',
    'depends': ['account'],
    'summary': 'This module is allow you to reconcile payment partial/full with multiple invoice/bills on payment | Invoice Partial Payment Reconciliation | Partial Invoice Payment and Reconciliation | Invoice Reconciliation with Partial Payment | Invoice Bill Partial Payment Reconciliation | Batch Payment Reconcile',
    'description': """
This module is allow you to partial/full reconcile multiple invoice/bills on payment
    """,
    "data" : [
        'security/ir.model.access.csv',
        'views/account_payment_view.xml',
    ],
    'price': 60.0,
    'currency': "EUR",
    'application': True,
    'installable': True,
    'live_test_url': 'https://youtu.be/M9UioY72xko',
    "license": "LGPL-3",
    "images":["static/description/Banner.png"],
}
