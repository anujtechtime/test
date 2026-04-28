{
    'name': 'Invoice Year of Acceptance Filter (Many2one)',
    'version': '13.0.1.0.1',
    'summary': 'Filter invoices by partner Year of Acceptance (Many2one)',
    'category': 'Accounting',
    'author': 'Custom',
    'depends': ['account'],
    'data': [
        'views/account_move_view.xml',
    ],
    'installable': True,
    'application': False,
}