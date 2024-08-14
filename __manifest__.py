# -*- coding: utf-8 -*-

{
    'name' : "OpenEducat Custom Estudiantes",
    'summary': "Modificacion y campos agregados en modulo estudiantes",
    'autor': "ISEP",
    "version": "16.0.0.0",
    'sequence': 101,
    'depends': [
        'base',
        'base_setup',
        'openeducat_core',
        'openeducat_admission',
        'isep_record_request'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/op_university_view.xml',
        'views/op_study_type_view.xml',
        'views/student_view.xml',
        'views/op_document_type_view.xml',
        'views/res_partner_views.xml',
        'views/op_course_views.xml',
        'views/op_batch_views.xml'
    ],
    'demo': [],
    'qweb': [],
    'application': True,
    'installable': True,
    'auto_install': False,
}
