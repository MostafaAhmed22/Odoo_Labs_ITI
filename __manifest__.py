{
    'name': 'Hospital Management System',
    'version': '1.0',
    'summary': 'Hospital Management System',
    'depends': ['base', 'crm'],

    'data': [
        'security/ir.model.access.csv',
        'views/patient_views.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/menu.xml',
        'views/res_partner_views.xml',
    ],

    'application': True,
}