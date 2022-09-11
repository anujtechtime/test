# -*- coding: utf-8 -*-
{
    'name': "fxTheme",
    'summary': """fxTheme for odoo 13 community edition""",

    'description': """
        fx theme for odoo 13 community edition, the beautiful UI yu want!
    """,

    'author': "fxOdoo",

    "category": "Themes/Backend",
    "website": "http://jingedl.com:8069",
    'live_test_url': 'http://jingedl.com:8069',

    'version': '1.0.8',
    'license': 'OPL-1',
    'images': ['static/description/banner.png', 'static/description/fx_screenshot.png'],

    'depends': ['base'],
    "application": False,
    "installable": True,
    "auto_install": False,

    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/fx_web.xml',
        'views/fx_login.xml'
    ],

    'qweb': [
        'static/xml/fx_web.xml',
        'static/xml/fx_menu.xml',
        'static/xml/fx_header.xml',
        'static/xml/fx_user_menu.xml',
        'static/xml/fx_page_header.xml',
        'static/xml/fx_page_footer.xml',
        'static/xml/fx_action_manager.xml',
        'static/xml/fx_pager.xml',
        'static/xml/fx_switch_buttons.xml',
        'static/xml/fx_theme_setting.xml',
        'static/xml/fx_menu_board.xml',
        'static/xml/fx_misc.xml'
    ],
    'price': 399,
    'currency': 'USD'
}
