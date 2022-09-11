{
    'name': "Current Inventory Valuation Report",
    'version': "1.0",
    'author': "ASAS",
    'category': "Tools",
    'depends': ['base', 'sale', 'account', 'stock'],
    'data': [
    	'wizard/curr_inv_report.xml',
        'wizard/product_inv_report.xml',
        'views/internal_layout_2.xml',
        'views/curr_inv_report_pdf.xml',
        'curr_inv_report_10_report.xml'
    ],
    'installable': True
}
