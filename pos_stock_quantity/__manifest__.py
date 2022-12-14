# -*- coding: utf-8 -*-
{
    'name': 'POS Stock',
    'version': '10.0.2',
    'category': 'Point Of Sale',
    'author': 'D.Jane',
    'sequence': 10,
    'summary': 'Show Stock(Product Quantity Available) in Configured Location. Real-Time Updates.',
    'description': "",
    'depends': ['point_of_sale'],
    'data': [
        'views/header.xml',
        'views/config.xml'
    ],
    'images': ['static/description/banner.png'],
    'qweb': ['static/src/xml/pos_stock.xml'],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
    'currency': 'EUR',
    'price': 99
}
