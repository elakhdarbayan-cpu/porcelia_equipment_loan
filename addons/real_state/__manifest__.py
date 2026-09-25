{
    'name': 'Real State',
    'version': '18.0.1.0',
    'summary': 'Real State Management',
    'description': 'A module to manage real estate properties, including property listings, sales, and rentals.',
    'author': 'Bayan Elakhdar',
    'website': 'https://www.yourwebsite.com',
    'category': 'base',
    'depends': ['base', 'sale', 'mail'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/real_state_views.xml',
        
    ],
    'installable': True,
    'application': True,
    'auto_install': True,
    'license': 'LGPL-3',

}
