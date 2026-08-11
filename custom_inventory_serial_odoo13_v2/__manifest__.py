# -*- coding: utf-8 -*-
{
    'name': 'Custom Inventory Serial Prefix',
    'version': '13.0.2.0.0',
    'category': 'Inventory',
    'summary': 'Location hierarchy prefixes and automatic serial generation',
    'depends': ['stock', 'purchase', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/product_views.xml',
        'views/stock_location_views.xml',
        'views/stock_picking_views.xml',
        'views/server_action.xml',
        'wizard/po_excel_import_views.xml',
    ],
    'external_dependencies': {'python': ['openpyxl']},
    'installable': True,
    'application': False,
}
