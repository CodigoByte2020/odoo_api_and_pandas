import json
import re

from odoo_connection import *
import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

PATH_ORIGINAL_VALUES_ACTIVE_BATCHES = '/home/gianmarco/PycharmProjects/isep_16/odoo16isep/addons-extra/addons_uisep/isep_student_custom/api/original_values.json'
PATH_ORIGINAL_VALUES_INACTIVE_BATCHES = '/home/gianmarco/PycharmProjects/isep_16/odoo16isep/addons-extra/addons_uisep/isep_student_custom/api/original_values_inactive_batches.json'

batch_fields = ['id', 'course_id', 'start_date', 'end_date', 'code', 'academic_year']
# ACTIVE BATCHES
# batches_odoo16 = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'op.batch', 'search_read',
#                                           [[['is_imported_record', '=', True]]], {'fields': batch_fields, 'limit': None})
# INACTIVE BATCHES
batches_odoo16 = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'op.batch', 'search_read',
                                          [[['active', '=', False], ['is_imported_record', '=', True]]],
                                          {'fields': batch_fields, 'limit': None})
df_batches_odoo_16 = pd.DataFrame(batches_odoo16)

course_ids = list(df_batches_odoo_16['course_id'].apply(lambda x: x[0]))
courses_odoo16 = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'op.course', 'search_read',
                                          [[['id', 'in', course_ids], ['active', 'in', [True, False]]]],
                                          {'fields': ['id', 'name', 'course_type_id']})
df_courses_odoo_16 = pd.DataFrame(courses_odoo16)
df_courses_odoo_16['course_type_name'] = df_courses_odoo_16['course_type_id'].apply(lambda x: x and x[1])
df_batches_odoo_16['course_id2'] = df_batches_odoo_16['course_id'].apply(lambda x: x[0])

df_merge_batches_and_courses = pd.merge(left=df_batches_odoo_16, right=df_courses_odoo_16, left_on='course_id2',
                                        right_on='id', suffixes=('_batch', '_course'))
df_merge_batches_and_courses.rename(columns={'name': 'course_name'}, inplace=True)

hours_of_course = {'Monográfico': 10, 'Curso': 30, 'Módulo': 10, 'Curso 30h': 30, 'Jornada': 10, 'Sesión Clínica': 2}

hours_of_course2 = {
    10: ['MONOGRÁFICO', 'MONOGRÁFICOS', 'MÓDULO', 'JORNADA', 'JORNADAS'],  # SHUFFLED: MONOGRÁFICO,
    30: ['CURSO', 'CURSO 30H'],  # SHUFFLED: CURSO - CURSO 30H, I USE IT (CATEGORY)
    2: ['SESIÓN CLÍNICA']
}

months_of_course = {
    'Mestrado': 24, 'Especialização': 12, 'Maestría': 24, 'Diplomado': 6, 'CERTIPROF': 1, 'Doctorado': 24,
    'Licenciatura': 32, 'Graduação': 32
}

months_of_course2 = {
    24: ['MÁSTER', 'MAESTRÍA', 'MESTRADO', 'MASTER', 'MAESTRIA', 'DOCTORADO'],  # SHUFFLED - MESTRADO - MAESTRÍA
    12: ['ESPECIALIZAÇÃO', 'ESPECIALIDAD', 'ESPECIALIDADE', 'ESPECIALIZACIÓN', 'POSGRADO'],  # SHUFFLED - ESPECIALIZAÇÃO
    6: ['DIPLOMADO', 'DIPLOMADOS'],
    1: ['CERTIPROF'],  # SHUFFLED - CERTIPROF, I SHOULD USE IT (CATEGORY)
    32: ['LICENCIATURA', 'GRADUAÇÃO']
}


def backup_data_active_batches():
    original_values = {}
    for _, row in df_merge_batches_and_courses.iterrows():
        batch_id = row['id_batch']
        original_values[batch_id] = {
            'start_date': row.get('start_date'),
            'end_date': row.get('end_date'),
            'academic_year': row.get('academic_year')
        }
    with open('original_values_active_batches_production.json', 'w') as file:
        json.dump(original_values, file, indent=4)
    print('THE ORIGINAL VALUES OF ACTIVE BATCHES HAVE BEEN SUCCESSFULLY SAVE')


def backup_data_inactive_batches():
    original_values = {}
    for _, row in df_merge_batches_and_courses.iterrows():
        batch_id = row['id_batch']
        original_values[batch_id] = {
            'start_date': row.get('start_date'),
            'end_date': row.get('end_date'),
            'academic_year': row.get('academic_year')
        }
    with open('original_values_inactive_batches_production.json', 'w') as file:
        json.dump(original_values, file, indent=4)
    print('THE ORIGINAL VALUES OF INACTIVE BATCHES HAVE BEEN SUCCESSFULLY SAVE')


def revert_changes(path_file):
    with open(path_file, 'r') as file:
        original_values = json.load(file)
        for batch_id, original in original_values.items():
            batch_id = int(batch_id)
            models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'op.batch', 'write', [[batch_id], original])
        print('THE ORIGINAL VALUES HAVE BEEN SUCCESSFULLY REVERT')


def get_key_hours(value):
    for key, v in hours_of_course2.items():
        if value.upper() in v:
            return {'hours': key}


def get_key_months(value):
    for key, v in months_of_course2.items():
        if value.upper() in v:
            return {'months': key}


# TODO: CHECK UPDATED BATCHES IN GRAFIC INTERFACE
#  CHECK CODE AND ACADEMIC YEAR
#  CHECK COURSE NAME AND TYPE COURSE OF BATCHES
try:
    # IF I FILTER FOR NAME, IT IS WELL
    # IT IS WELL IF I AFTER FILTER FOR CATEGORY
    def update_dates():
        values = []
        for _, row in df_merge_batches_and_courses.iterrows():
            batch_id = row['id_batch']
            start_date = row.get('start_date')
            course_name = row['course_name']
            course_name_split = course_name.split(sep=None, maxsplit=1)[0]
            time_to_sum = get_key_hours(course_name_split) or get_key_months(course_name_split)
            academic_year = row.get('academic_year')

            if academic_year == 'None':
                academic_year = None

            if not time_to_sum:
                course_type_name = row.get('course_type_name')
                if course_type_name in hours_of_course.keys():
                    hours_quantity = hours_of_course[course_type_name]
                    time_to_sum = {'hours': hours_quantity}
                elif course_type_name in months_of_course.keys():
                    months_quantity = months_of_course[course_type_name]
                    time_to_sum = {'months': months_quantity}

            if academic_year:
                pattern = r'[-/]'
                academic_year = re.split(pattern=pattern, string=academic_year)[0]
                start_year = start_date.split('-')[0]
                if academic_year != start_year:
                    start_date = date(int(academic_year), 1, 1)

            start_date = datetime.strptime(str(start_date), '%Y-%m-%d').date()
            end_date = start_date + relativedelta(**time_to_sum)
            start_date_string = str(start_date)
            end_date_string = str(end_date)
            academic_year = f'{start_date.year}-{end_date.year}'
            values.append([[batch_id], {'start_date': start_date_string, 'end_date': end_date_string,
                                        'academic_year': academic_year}])
            print(f'IF IT RUN, IT IS WELL - {batch_id = }')

        for value in values:
            models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'op.batch', 'write', value)
            print(f'THE BATCH WAS UPDATED SUCCESSFULLY - {value[0][0] = }')

        print('ALL RECORDS WERE UPDATED SUCCESSFULLY')

    # backup_data_active_batches()
    # backup_data_inactive_batches()
    update_dates()
    # revert_changes(PATH_ORIGINAL_VALUES_ACTIVE_BATCHES)
    # revert_changes(PATH_ORIGINAL_VALUES_INACTIVE_BATCHES)

except Exception as exc:
    print(f'*************** EXCEPTION *************** {exc = }')
