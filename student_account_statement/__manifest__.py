{
    'name': 'Student Account Statement',
    'version': '13.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Account Statement for Students (Invoices & Payments)',
    'description': 'Generates account statement with invoices and payments for students.',
    'author': 'ChatGPT',
    'depends': ['account', 'sale'],
    'data': [
        'wizard/account_statement_wizard_view.xml',
        'report/account_statement_report.xml',
        'report/account_statement_template.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
}
