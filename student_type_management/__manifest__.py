# -*- coding: utf-8 -*-
{
    'name': 'Student Type Management',
    'version': '13.0.1.0.0',
    'category': 'Education',
    'summary': 'Manage student types with official letter attachment for non-general channels',
    'description': """
        This module manages student types with the following features:
        - Student type field linked to level.level
        - Required official letter attachment for non-general channel changes
        - Validation on create and update
        - Pending change tracking
        - Search filters for easy management
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'mail', 'contacts','sale'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'data/student_type_data.xml',
        'views/partner_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}