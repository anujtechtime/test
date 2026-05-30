{
    'name': 'Custom Contact Search',
    'version': '13.0.1.0.0',
    'category': 'Tools',
    'summary': 'Custom contact search box with autocomplete',
    'depends': ['web', 'contacts'],
    'qweb': [
        'static/src/xml/custom_contact_search.xml',
    ],
    'data': [
        'views/assets.xml',
    ],
    'installable': True,
    'application': False,
}
