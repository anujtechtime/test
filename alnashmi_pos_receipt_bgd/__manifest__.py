{
    'name': "Alnashmi Receipt",
    'summary': """Alnashmi Print Receipt""",
    'description': """
    	Alnashmi Print Receipt (A5 dimensions)
    """,

    'author': "ASAS Telecom and IT Solutions",
    'website': "https://www.asas.net",

    'category': "Point of Sale",
    'version': "1.0",

    'depends': ['base', 'web', 'website', 'point_of_sale','stock'],
    'data': [
        'views/alnashmi_pos_receipt.xml',
        'views/alnashmi_customer_update.xml'
    ],
    'qweb': ['static/src/xml/pos_extend.xml', 'static/src/xml/base.xml'],
    'installable': True
}
