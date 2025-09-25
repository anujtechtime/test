{
    'name': 'Student Account Statement',
    'version': '13.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Account Statement Report for Students',
    'author': 'Custom',
    'depends': ['account', 'sale'],
    'data': [
        'report/account_statement_report.xml',
        'report/account_statement_template.xml',
    ],
    'installable': True,
    'application': False,
}
