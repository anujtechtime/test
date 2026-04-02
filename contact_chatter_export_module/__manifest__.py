
{
    'name': 'Contact Chatter Export',
    'version': '1.0',
    'summary': 'Export chatter history of contacts to Excel',
    'depends': ['contacts', 'mail'],
    'data': [
        'wizard/export_chatter_wizard_view.xml',
        'views/partner_action.xml'
    ],
    'installable': True,
    'application': False
}
