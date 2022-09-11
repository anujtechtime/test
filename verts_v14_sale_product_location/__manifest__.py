# -*- coding: utf-8 -*-

{
    'name': 'Verts V14 Sale Product Location',
    'version': '1.0',
    'author': 'VERTS Services India Pvt. Ltd.',
    'description': """ * Add Prot Location In sale order Line""",

    'website': 'http://www.verts.co.in',
    'depends': ['sale','account'],
    'category': 'Sale ',
    'init_xml': [],
    'demo_xml': [],
    'data': [
        'views/sale_order_view.xml',
        'security/ir.model.access.csv'
    ],
    'test': [],
    "qweb": [],
    'installable': True,
    'active': False,
    'certificate': '',
}
