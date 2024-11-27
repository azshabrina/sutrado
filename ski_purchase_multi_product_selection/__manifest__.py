# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

{
    'name': "Purchase Order Multi Product PR Selection",
    'version': "17.0.0.1",
    'summary': "This module allows you to select Multiple product PR in purchase order at a time on single click.",
    'category': 'Purchases',
    'description': """
        This module allows you to select Multiple product in purchase order on single click.
         Purchase order add multi product
    """,
    'author': "Fathoni Anwar - Quality Assurance",
    'website': "https://sutrakabel.com",
    'depends': ['base', 'purchase', 'approvals'],
    'data': [
                'security/ir.model.access.csv',
        'views/purchase.xml',
    ],
    'demo': [],
    "license": "OPL-1",
    'images': ['static/description/banner.png'],
    'sequence': 0,
    'installable': True,
    'application': True,
    'auto_install': False,
}
