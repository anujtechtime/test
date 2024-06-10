# -*- coding: utf-8 -*-
{
    'name': "almaaqal_template",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','base_accounting_kit'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/report.xml',
        'report/report_trial_balance_new_page_eight.xml',
        'report/report_trial_balance_new_page_five.xml',
        'report/report_trial_balance_new_page_four.xml',
        'report/report_trial_balance_new_page_nine.xml',
        'report/report_trial_balance_new_page_one.xml',
        'report/report_trial_balance_new_page_seven.xml',
        'report/report_trial_balance_new_page_six.xml',
        'report/report_trial_balance_new_page_three.xml',
        'report/report_trial_balance_new_page_two.xml',
        'wizard/trial_balance_new_page_3.xml',

        'wizard/trial_balance_new_page_4.xml',

        'wizard/trial_balance_new_page_5.xml',

        'wizard/trial_balance_new_page_6.xml',

        'wizard/trial_balance_new_page_7.xml',

        'wizard/trial_balance_new_page_8.xml',

        'wizard/trial_balance_new_page_9.xml',


        'wizard/trial_balance_new_page_one.xml',

        'wizard/trial_balance_new_page_two.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
