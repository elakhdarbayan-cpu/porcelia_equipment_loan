{
    'name': 'Library Management',
    'version': '18.0.1.0',
    'summary': 'Manage library books and borrowing',
    'description': 'A complete library management system',
    'author': 'Bayan Elakhdar',
    'category': 'Education',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/library_book_views.xml',
        'data/sequence.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}