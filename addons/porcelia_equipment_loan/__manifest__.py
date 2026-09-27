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
        'wizard/loan_return_wizard_views.xml',   
        'views/equipment_category_views.xml',
        'views/equipment_item_views.xml',
        'views/equipment_loan_views.xml',       
        'views/equipment_menus.xml',
        'views/res_users_views.xml',
        'report/loan_report.xml',
        'data/ir_cron.xml',
    ],
    'demo': [
    'data/demo_data.xml',
],
    'installable': True,
    'application': True,
    'auto_install': False,
}