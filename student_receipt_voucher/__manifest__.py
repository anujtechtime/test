# student_receipt_voucher/__manifest__.py
{
    'name': 'Student Receipt Voucher',
    'version': '13.0.1.0.0',
    'summary': 'وصل طالب جديد - Payment Receipt Report',
    'description': """
Student Payment Receipt Voucher
===============================
Custom QWeb PDF report titled "وصل طالب جديد" for account.payment.
    """,
    'author': 'Your Company',
    'category': 'Accounting',
    'license': 'LGPL-3',
    'depends': ['base', 'account'],
    'data': [
        'report/report_payment_receipt.xml',
        'report/payment_receipt_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}