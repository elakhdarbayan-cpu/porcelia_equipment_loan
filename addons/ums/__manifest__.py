{
    'name': 'University Management System',
    'version': '18.0.1.0',
    'summary': 'Manage university students and operations',
    'description': 'Module to manage studentss in university',
    'author': 'Bayan Elakhdar',
    'category': 'Education',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/university_student_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    }