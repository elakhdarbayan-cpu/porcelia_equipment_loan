{
    'name': 'Porcelia Equipment Loan',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Manage equipment loans to employees',
    'description': """
        Equipment Loan Manager for Porcelia.
        Manage the full lifecycle of equipment loans.
    """,
    'author': 'Bayan Elakhdar',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/equipment_groups.xml',
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/equipment_category_views.xml',
        'views/equipment_item_views.xml',
        'views/equipment_loan_views.xml',
        'views/equipment_menus.xml',
        'wizard/loan_return_wizard_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}