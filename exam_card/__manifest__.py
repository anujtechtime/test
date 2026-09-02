{
    'name': 'Exam Card',
    'version': '13.0.1.0.0',
    'category': 'Education',
    'summary': 'Print Exam Cards for Students',
    'description': """
        Print exam cards with variable selection for exam type and academic year.
        Card size: 9.1cm x 5.5cm
    """,
    'author': 'Your Company',
    'website': 'http://www.yourcompany.com',
    'depends': ['base', 'web', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'data/exam_card_data.xml',
        'views/res_partner_views.xml',
        'views/exam_card_views.xml',
        'views/exam_card_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'exam_card/static/src/js/exam_card.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}