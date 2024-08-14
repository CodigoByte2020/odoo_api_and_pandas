import xmlrpc.client
import pandas as pd

# CONNECTION DATA ODOO 12
URL_ODOO12 = 'https://odoo12migracion.universidadisep.com'
DB_ODOO12 = 'final'
USER_NAME_ODOO12 = 'admin_miguel'
PASSWORD_ODOO12 = '12345678'

# # CONNECTION DATA ODOO 16
# URL_ODOO16 = 'https://odoo16migracion.universidadisep.com'
# DB_ODOO16 = 'UniversidadISep2'
# USER_NAME_ODOO16 = 'admin_miguel'
# PASSWORD_ODOO16 = '12345678'
# API_KEY_ODOO16 = 'aa73c825128ec71f64e4594a649a34ccd8f58d0f'

# # CONNECTION DATA ODOO 16 - DEV
# URL_ODOO16 = 'https://dev.odoo.universidadisep.com/'
# DB_ODOO16 = 'UniversidadISep'
# USER_NAME_ODOO16 = 'admin_copia'
# API_KEY_ODOO16 = '47bd7099eb31149dd8aa6de2d348f4381a46403f'
# PASSWORD_ODOO16 = '12345678'

# CONNECTION DATA ODOO 16 - PRODUCTION
URL_ODOO16 = 'https://app.universidadisep.com/'
DB_ODOO16 = 'UniversidadISep2'
USER_NAME_ODOO16 = 'admin_copia'
API_KEY_ODOO16 = '47bd7099eb31149dd8aa6de2d348f4381a46403f'
PASSWORD_ODOO16 = '12345678'


def connect_to_odoo(url, db, user_name, password):
    try:
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/common', allow_none=True)
        uid = common.authenticate(db, user_name, password, {})
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', allow_none=True)
        return uid, models
    except Exception as exception:
        print(f'********** EXCEPTION ********** {exception = }')


uid_odoo12, models_odoo12 = connect_to_odoo(URL_ODOO12, DB_ODOO12, USER_NAME_ODOO12, PASSWORD_ODOO12)
uid_odoo16, models_odoo16 = connect_to_odoo(URL_ODOO16, DB_ODOO16, USER_NAME_ODOO16, API_KEY_ODOO16)

try:
    # ********************************** BATCHES ***********************************************************************
    # I CREATE A DATAFRAME OF INACTIVE BATCHES OF ODOO 12
    field_batches = [
        'student_count', 'name', 'course_id', 'start_date', 'coordinator', 'campus_id', 'uvic_program', 'code',
        'company_id', 'end_date', 'modality_id', 'students_limit', 'sepyc_program', 'expiration_days', 'date_diplomas',
        'academic_year', 'generation', 'hours', 'credits', 'ects', 'practical_hours_total', 'independent_hours_total',
        'theoretical_hours_total', 'hours_total', 'practical_hours_credits', 'independent_hours_credits',
        'theoretical_hours_credits', 'credits_total', 'days_week', 'schedule', 'contact_class', 'type_practices',
        'acknowledgments', 'reconeixements'
    ]
    batches_odoo12 = models_odoo12.execute_kw(DB_ODOO12, uid_odoo12, PASSWORD_ODOO12, 'op.batch', 'search_read',
                                              [[['active', '=', False]]], {'fields': field_batches})
    df_batches_odoo12 = pd.DataFrame(batches_odoo12)
    df_batches_odoo12 = df_batches_odoo12[df_batches_odoo12['student_count'] > 0]
    df_batches_odoo12['name'] = df_batches_odoo12['name'].str.upper()
    df_batches_odoo12.drop_duplicates(subset=['name'], inplace=True)
    df_batches_odoo12.drop_duplicates(subset=['code'], inplace=True)
    # ************************** ODOO 16 *******************************************************************************
    # I CONSULT ACTIVE AND INACTIVE BATCHES OF ODOO 16
    batches_odoo16 = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'op.batch', 'search_read', [[]],
                                              {'fields': ['name', 'code']})
    codes_batches_odoo16 = list(set([x['code'] for x in batches_odoo16]))
    names_batches_odoo16 = list(set([x['name'] for x in batches_odoo16]))
    names_batches_odoo16 = list(map(lambda x: x.upper(), names_batches_odoo16))
    # ************************** COMPARE DATA **************************************************************************
    # I COMPARE ALL BATCHES OF ODOO 12 AND ODOO 16
    df_batches_odoo12 = df_batches_odoo12[df_batches_odoo12['code'].apply(lambda x: x not in codes_batches_odoo16)]
    df_batches_odoo12 = df_batches_odoo12[df_batches_odoo12['name'].apply(lambda x: x not in names_batches_odoo16)]
    # ************************** COURSES *******************************************************************************
    # I AM CONSULTING ALL INACTIVE COURSES IN ODOO 12 OF ALL PROCESSED BATCHES
    field_courses = ['name', 'course_type_id', 'area_id', 'code', 'fees_term_id', 'company_id']
    course_ids_odoo12 = list(df_batches_odoo12['course_id'].apply(lambda x: x[0]))
    courses_odoo12 = models_odoo12.execute_kw(DB_ODOO12, uid_odoo12, PASSWORD_ODOO12, 'op.course', 'search_read',
                                              [[['active', '=', False], ['id', 'in', course_ids_odoo12]]],
                                              {'fields': field_courses})
    df_courses_odoo12 = pd.DataFrame(courses_odoo12)
    df_courses_odoo12['name'] = df_courses_odoo12['name'].str.upper()
    df_courses_odoo12.drop_duplicates(subset=['name'], inplace=True)
    df_courses_odoo12.drop_duplicates(subset=['code'], inplace=True)
    # *************************************** ODOO 16 ******************************************************************
    # I CONSULT ALL COURSES OF ODOO 16, BECAUSE I WILL PROCESS THIS
    courses_odoo16 = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'op.course', 'search_read', [[]],
                                              {'fields': ['name', 'code']})
    codes_courses_odoo16 = list(set([x['code'] for x in courses_odoo16]))
    names_courses_odoo16 = list(set([x['name'] for x in courses_odoo16]))
    names_courses_odoo16 = list(map(lambda x: x.upper(), names_courses_odoo16))
    # ************************** COMPARE DATA **************************************************************************
    # I DELETE COURSES OF df_courses_odoo12 THAT HAVE SAME CODE IN ODOO 16
    df_courses_odoo12 = df_courses_odoo12[df_courses_odoo12['code'].apply(lambda x: x not in codes_courses_odoo16)]
    df_courses_odoo12 = df_courses_odoo12[df_courses_odoo12['name'].apply(lambda x: x not in names_courses_odoo16)]
    # ************************** CREATE COURSES ************************************************************************
    course_type_id_dict = {
        'Mestrado': 'op_course_type_0001', 'Monográfico': 'op_course_type_0002', 'Curso': 'op_course_type_0003',
        'Especialização': 'op_course_type_0004', 'Maestría': 'op_course_type_0005', 'Apagar': 'op_course_type_0006',
        'Diplomado': 'op_course_type_0007', 'Módulo': 'op_course_type_0008', 'CERTIPROF': 'op_course_type_0009',
        'Curso 30h': 'op_course_type_0010', 'Doctorado': 'op_course_type_0011', 'Licenciatura': 'op_course_type_0012',
        'Graduação': 'op_course_type_0013', 'Jornada': 'op_course_type_0014', 'Sesión Clínica': 'op_course_type_0015'
    }
    area_id_dict = {
        'Empresarial': 'op_area_course_0001', 'Inmobiliaria': 'op_area_course_0002',
        'Oposiciones': 'op_area_course_0003', 'Pediatría': 'op_area_course_0004', 'Sanitaria': 'op_area_course_0005',
        'Seguridad': 'op_area_course_0006', 'Técnica': 'op_area_course_0007', 'Veterinaria': 'op_area_course_0008',
        'Psicología Clínica': 'op_area_course_0009', 'Psicopedagogía': 'op_area_course_0010',
        'Genéricos': 'op_area_course_0011', 'Logopedia': 'op_area_course_0012',
        'Formación Profesional': 'op_area_course_0013', 'Sociosanitaria': 'op_area_course_0014',
        'Pruebas de acceso': 'op_area_course_0015', 'Programa Corta Duración': 'op_area_course_0016',
        'All': 'op_area_course_0017', 'Salud y Bienestar': 'op_area_course_0018',
        'Administración': 'op_area_course_0019', 'Neurociencias': 'op_area_course_0020',
        'Educación': 'op_area_course_0021', 'Psicologia - BR': 'op_area_course_0022', 'Educação': 'op_area_course_0023',
        'Neurociência': 'op_area_course_0024', 'Administração': 'op_area_course_0025',
        'Neuropsicología - BR': 'op_area_course_0026', 'Certificação': 'op_area_course_0027',
        'Geral': 'op_area_course_0028', 'Ciências Humanas': 'op_area_course_0029', 'CERTIPROF': 'op_area_course_0030',
        'sicuales': 'op_area_course_0031', 'Ciencias Sociales': 'op_area_course_0032',
        'Ingeniería': 'op_area_course_0033', 'Fonoaudiólogia': 'op_area_course_0034'
    }
    fees_term_id_dict = {
        'Normal': 'op_fees_terms_3_c7c12456'
    }
    company_id_dict = {
        'ISEP INTERNACIONAL, LLC': 'main_company',
        'Isep Latam': 'res_company_5_6c52fb92',
        'ISEP BRASIL': 'res_company_8_50662d8b'
    }
    campus_0001 = [
        'Albacete', 'Aragón', 'Bilbao', 'Buenos Aires', 'Catalunya', 'Euskadi', 'Granada', 'Illes', 'Logroño',
        'Málaga (Cursos Antiguos)', 'Madrid', 'Murcia', 'Oporto (Portugal)', 'Pamplona', 'Las Palmas de Gran Canaria',
        'Palma de Mallorca', 'Santiago de compostela', 'San Sebastián', 'Sevilla', 'Tenerife', 'Valencia', 'Vic',
        'Vitoria', 'Zaragoza', 'Barcelona'
    ]
    campus_id_dict = {campus: 'op_campus_0001' for campus in campus_0001}
    campus_id_dict.update({'E-Learning': 'op_campus_0002', 'Online': 'op_campus_0002'})
    modality_id_dict = {
        'Presencial': 'op_modality_0001', 'Presencial SIN': 'op_modality_0001', 'Presencial INT': 'op_modality_0001',
        'Online': 'op_modality_0002', 'E-Learning': 'op_modality_0002', 'Distancia': 'op_modality_0002',
        'E-Learning (no residente)': 'op_modality_0002', 'Metodología 360°': 'op_modality_0002'
    }
    lang_dict = {
        'ISEP INTERNACIONAL, LLC': 'es_MX',
        'Isep Latam': 'es_MX',
        'ISEP BRASIL': 'pt_BR'
    }
    batch_sequence = 467


    def process_row_courses(row):
        related_fields = dict.fromkeys(['course_type_id', 'area_id', 'fees_term_id', 'company_id', 'lang'], False)
        for key in related_fields:
            if key == 'lang':
                dictionary_of_related_value = globals().get(f'{key}_dict')
                name = row['company_id'][1]
                name = dictionary_of_related_value[name]
                related_fields[key] = name
            elif row.get(key):
                dictionary_of_related_value = globals().get(f'{key}_dict')
                name = row[key][1]
                name = dictionary_of_related_value[name]
                id_value = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'ir.model.data',
                                                    'search_read', [[['name', '=', name]]],
                                                    {'fields': ['res_id']})[0]['res_id']
                related_fields[key] = id_value
        return related_fields


    def create_courses():
        course_counter = 1
        course_sequence = 185

        for _, row in df_courses_odoo12.iterrows():
            related_fields = process_row_courses(row)
            values_to_create = {
                'name': row['name'],
                'code': row['code'],
                'evaluation_type': 'normal',
                'is_imported_record': True,
                'active': False,
                **related_fields
            }
            course_id = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'op.course', 'create',
                                                 [values_to_create])
            print(f'THE COURSE WAS SUCCESSFULLY CREATED: {course_id = } - {row["name"]}')
            dict_model_data = {
                'name': f'op_course_0{course_sequence}',
                'module': 'isep_student_migration',
                'res_id': course_id,
                'model': 'op.course',
                'noupdate': True
            }
            ir_model_data_record = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'ir.model.data',
                                                            'create', [dict_model_data])
            print(f'THE EXTERNAL ID OF COURSE WAS SUCCESSFULLY CREATED {ir_model_data_record = }')
            print(f'************************** {course_counter = } **************************')
            course_counter += 1
            course_sequence += 1

            create_batches(course_id=course_id, course_name=row['name'])

        print('CONGRATULATIONS - ALL COURSES WERE SUCCESSFULLY CREATED.')


    def process_row_batches(row):
        related_fields = dict.fromkeys(['company_id', 'campus_id', 'modality_id'], False)
        if row.get('company_id'):
            dictionary_of_related_value = globals().get(f'company_id_dict')
            name_company = row['company_id'][1]
            name_company = dictionary_of_related_value[name_company]
            company_id = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'ir.model.data',
                                                  'search_read', [[['name', '=', name_company]]],
                                                  {'fields': ['res_id']})[0]['res_id']
            related_fields['company_id'] = company_id

        if row.get('modality_id'):
            dictionary_of_related_value = globals().get(f'modality_id_dict')
            name_modality = row['modality_id'][1]
            name_modality = dictionary_of_related_value[name_modality]
            name_campus = 'op_campus_0001' if name_modality == 'op_modality_0001' else 'op_campus_0002'
            campus_id = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'ir.model.data',
                                                 'search_read', [[['name', '=', name_campus]]],
                                                 {'fields': ['res_id']})[0]['res_id']
            modality_id = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'ir.model.data',
                                                   'search_read', [[['name', '=', name_modality]]],
                                                   {'fields': ['res_id']})[0]['res_id']
            related_fields.update({'campus_id': campus_id, 'modality_id': modality_id})

        if not row.get('modality_id') and row.get('campus_id'):
            dictionary_of_related_value = globals().get(f'campus_id_dict')
            name_campus = row['campus_id'][1]
            name_campus = dictionary_of_related_value[name_campus]
            name_modality = 'op_modality_0001' if name_campus == 'op_campus_0001' else 'op_modality_0002'
            campus_id = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'ir.model.data',
                                                 'search_read', [[['name', '=', name_campus]]],
                                                 {'fields': ['res_id']})[0]['res_id']
            modality_id = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'ir.model.data',
                                                   'search_read', [[['name', '=', name_modality]]],
                                                   {'fields': ['res_id']})[0]['res_id']
            related_fields.update({'campus_id': campus_id, 'modality_id': modality_id})

        return related_fields


    def create_batches(course_id=False, course_name=None):
        global batch_sequence
        batch_counter = 1
        df_batches_by_course = df_batches_odoo12[
            df_batches_odoo12['course_id'].apply(lambda x: x[1].upper() == course_name.upper())]
        df_batches_by_course = df_batches_by_course[
            df_batches_by_course['end_date'] > df_batches_by_course['start_date']]
        normal_fields = [
            'name', 'start_date', 'uvic_program', 'code', 'end_date', 'students_limit', 'sepyc_program',
            'expiration_days', 'date_diplomas', 'academic_year', 'generation', 'hours', 'credits', 'ects',
            'practical_hours_total', 'independent_hours_total', 'theoretical_hours_total', 'hours_total',
            'practical_hours_credits', 'independent_hours_credits', 'theoretical_hours_credits', 'credits_total',
            'days_week', 'schedule', 'contact_class', 'type_practices', 'acknowledgments', 'reconeixements'
        ]
        for _, row in df_batches_by_course.iterrows():
            related_fields = process_row_batches(row)
            values_to_create = {
                'course_id': course_id,
                'is_imported_record': True,
                'active': False,
                **related_fields
            }
            values_to_create.update({index: row[index] for index in row.index if index in normal_fields})
            batch_id = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'op.batch', 'create',
                                                [values_to_create])
            print(f'THE BATCH WERE SUCCESSFULLY CREATED: {batch_id = } - {row["name"]}')
            dict_model_data = {
                'name': f'op_batch_0{batch_sequence}',
                'module': 'isep_student_migration',
                'res_id': batch_id,
                'model': 'op.batch',
                'noupdate': True
            }
            ir_model_data_record = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'ir.model.data',
                                                            'create', [dict_model_data])
            print(f'THE EXTERNAL ID OF BATCH WAS SUCCESSFULLY CREATED {ir_model_data_record = }')
            print(f'************************** {batch_counter = } **************************')
            batch_counter += 1
            batch_sequence += 1

        print(f'CONGRATULATIONS - ALL BATCHES OF THE COURSE {course_id} WERE SUCCESSFULLY CREATED.')
        print(sep='\n')


    create_courses()

except Exception as exc:
    print(f'********** EXCEPTION ********** {exc = }')
