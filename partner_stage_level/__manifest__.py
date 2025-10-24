
{
    'name': 'Customer Stage Field',
    'version': '13.0.1.0',
    'depends': ['base', 'contacts'],
    'data': [
        'data/res_partner_stage_data.xml',
        'views/res_partner_stage_view.xml',
        'views/res_partner_view.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': False,
}
