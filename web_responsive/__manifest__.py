# Copyright 2016-2017 LasLabs Inc.
# Copyright 2018 Alexandre Díaz
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Web Responsive",
    "summary": "Responsive web client, community-supported",
    "version": "12.0.2.2.1",
    "category": "Website",
    "website": "https://github.com/OCA/web",
    "author": "LasLabs, Tecnativa, Alexandre Díaz, "
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": [
        'base','web',
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/res_users.xml',
        'views/web.xml',
        'data/database_schedule.xml',
    ],
    'qweb': [
        'static/src/xml/apps.xml',
        'static/src/xml/form_view.xml',
        'static/src/xml/navbar.xml',
        'static/src/xml/document_viewer.xml',
    ],
}
