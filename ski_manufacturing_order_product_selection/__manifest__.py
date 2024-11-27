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
    'name': "Manufacturing Order By SO Product Selection",
    'version': "17.0.0.1",
    'summary': "This module allows you to select product SO in Manufacturing order at a time on single click.",
    'category': 'Manufacturing',
    'description': """
        This module allows you to select product in manufacturing order on single click.
         Manufacturing order add product SO
    """,
    'author': "Fathoni Anwar - Quality Assurance",
    'website': "https://sutrakabel.com",
    'depends': ['base', 'mrp', 'sale', 'sale_management'],
    'data': [
                # 'security/ir.model.access.csv',
        'views/manufacturing.xml',
    ],
    'demo': [],
    "license": "OPL-1",
    'images': ['static/description/banner.png'],
    'sequence': 0,
    'installable': True,
    'application': True,
    'auto_install': False,
}
