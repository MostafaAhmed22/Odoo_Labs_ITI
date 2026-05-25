{
    'name': 'Hospital Management System',
    'version': '1.0',
    'summary': 'Hospital Management System',
    'depends': ['base', 'crm'],

    'data': [
        'security/sec_groups.xml',
        'security/rec_rules.xml',
        'security/ir.model.access.csv',
        'reports/patient_report.xml',
        'reports/patient_report_actions.xml',
        'views/patient_views.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/menu.xml',
        'views/res_partner_views.xml',
    ],

    'application': True,
}