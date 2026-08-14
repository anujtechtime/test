# -*- coding: utf-8 -*-
{
    'name': 'Custom Inventory Serial Prefix',
    'version': '13.0.1.0.0',
    'summary': 'Generate serial numbers from destination location and product prefixes',
    'description': '''
Custom Inventory Serial Prefix
==============================

Features:
- Prefix Code on products and stock locations.
- Builds a location prefix from the complete parent location path.
- Automatically generates unique serial/lot numbers for tracked products when an
  internal transfer is validated.
- Generates serials in the form LOCATION_PREFIX + PRODUCT_PREFIX + 4 digit sequence.
  Example: NF5x0001.
- Includes a Purchase Order Excel import wizard and downloadable XLSX template.
- Includes a server action for completed pickings to repair/assign missing serials.

Designed for Odoo 13.
''',
    'author': 'Custom Development',
    'license': 'LGPL-3',
    'category': 'Inventory',
    'depends': [
        'stock',
        'purchase',
    ],
    'external_dependencies': {
        'python': ['openpyxl'],
    },
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/server_action.xml',
        'views/product_views.xml',
        'views/stock_location_views.xml',
        'views/stock_picking_views.xml',
        'views/purchase_order_views.xml',
        'wizard/po_excel_import_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
