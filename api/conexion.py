# TODO:
#  FILTRAR GRUPOS QUE TENGAN ALUMNOS, Y DE AHI SACAR LOS CURSOS DE ESOS GRUPOS.
#  MAESTRIA Y MASTER ES LO MISMO.
#  LO IMPORTANTE ES EL ALUMNO Y SUS NOTAS.
#  NO IMPORTA SI EN UN LOTE HAY 1000 ASIGNATURAS, SINO HAY ALUMNOS ESE LOTE NO SE IMPORTA
#  LOS LOTES SE IMPORTARON EL 02/07/24

# TODO:
#  CONSULTAS:
#  Se van a importar los registros archivados como archivados ? Los registros se van a importar como archivados.
#  Se han eliminado lotes o cursos en el sistema de producción, desde la fecha que se creo el ambiente de migración ?
#   - Mar dice que no está seguro, pero yo he revisado y si han eliminado cursos o lotes.
#  Las admisiones tambien se han archivado en el 12 ? No
#  Cuando tengo 2 registros iguales, cual prevalece el de la 12 o la 16 ? Prevalece el de la 16
#

import xmlrpc.client
from datetime import datetime
from pprint import pprint
import pandas as pd

# # CONNECTION DATA ODOO 16
# URL = 'https://odoo16migracion.universidadisep.com'
# DB = 'UniversidadISep2'
# USER_NAME = 'admin_miguel'
# PASSWORD = '12345678'
# API_KEY = 'aa73c825128ec71f64e4594a649a34ccd8f58d0f'

# CONNECTION DATA ODOO 16 - DEV
# URL = 'https://dev.odoo.universidadisep.com/'
# DB = 'UniversidadISep'
# USER_NAME = 'admin_copia'
# API_KEY = '47bd7099eb31149dd8aa6de2d348f4381a46403f'
# PASSWORD = '12345678'

# # CONNECTION DATA ODOO 16 - PRODUCTION
URL = 'https://app.universidadisep.com/'
DB = 'UniversidadISep2'
USER_NAME = 'admin_copia'
API_KEY = '47bd7099eb31149dd8aa6de2d348f4381a46403f'
PASSWORD = '12345678'

# LOGIN
try:
    common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common', allow_none=True)
    pprint(common.version())  # ODOO VERSION
    uid = common.authenticate(DB, USER_NAME, API_KEY, {})  # USER AUTHENTICATION
    print(f'{uid = } ')

    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object', allow_none=True)  # CREATE A PROXY FOR CONNECT TO THE ODOO SERVER
    # courses = obj.execute_kw(DB, uid, PASSWORD, 'op.course', 'search_count', [[['active', '=', True]]])
    # courses = obj.execute_kw(DB, uid, PASSWORD, 'op.course', 'search_read', [[]], {'fields': ['id']})
    courses_odoo16 = models.execute_kw(DB, uid, API_KEY, 'op.batch', 'search_read', [[['active', '=', True]]],
                                       {'fields': ['name', 'code']})
    codes = [course['code'] for course in courses_odoo16]
    names_upper = [course['name'].upper() for course in courses_odoo16]
    path_file = '/home/gianmarco/PycharmProjects/isep_16/odoo16isep/addons-extra/addons_uisep/isep_student_custom/models/op.batch.5.process.2.csv'
    with open(path_file, 'r') as csv_file:
        names = [
            "id", "name", "course_id/id", "start_date", "coordinator/id", "campus_id/id", "uvic_program", "code",
            "company_id/id", "end_date", "modality_id/id", "students_limit", "sepyc_program", "expiration_days",
            "date_diplomas", "academic_year", "generation", "hours", "credits", "ects", "practical_hours_total",
            "independent_hours_total", "theoretical_hours_total", "hours_total", "practical_hours_credits",
            "independent_hours_credits", "theoretical_hours_credits", "credits_total", "days_week", "schedule",
            "contact_class", "type_practices/id", "acknowledgments", "reconeixements", "is_imported_record"
        ]
        batches = pd.read_csv(csv_file, sep=',')
        batches.fillna(value='', inplace=True)
        repeated_batches, no_repeated_batches, dict_values_final = [], [], []
        related_fields = ['course_id', 'coordinator', 'campus_id', 'company_id', 'modality_id']
        float_fields = ['hours', 'credits', 'ects', 'practical_hours_total', 'independent_hours_total',
                        'theoretical_hours_total', 'practical_hours_credits', 'independent_hours_credits',
                        'theoretical_hours_credits', 'credits_total']

        for index, row in batches.iterrows():
            if row['code'] not in codes and row['name'] not in names_upper:
                no_repeated_batches.append({'name': row['name'], 'code': row['code']})
                print(f'Non repeated record {row["id"]}')
                dict_values = {}
                for name in names:
                    name_divided = name.split('/')[0]
                    if name != 'id':
                        if row[name] == '':
                            row[name] = None
                        # WE WILL PROCESS MANY2ONE FIELDS
                        elif len(name.split('/')) == 2:
                            foreign_name = str(row[name]).split('.')[-1]
                            if name_divided in related_fields:
                                foreign_id = models.execute_kw(
                                    DB, uid, API_KEY, 'ir.model.data', 'search_read', [[['name', '=', foreign_name]]],
                                    {'fields': ['res_id']})
                                row[name] = foreign_id and foreign_id[0]['res_id'] or 0
                        # WE WILL PROCESS FLOAT FIELDS
                        elif name_divided in float_fields:
                            row[name] = float(str(row[name]).replace(',', '.'))
                        dict_values[name_divided] = row[name]

                new_record = models.execute_kw(DB, uid, API_KEY, 'op.batch', 'create', [dict_values])

                dict_model_data = {
                    'name': row['id'],
                    'module': 'isep_student_migration',
                    'res_id': new_record,
                    'model': 'op.batch',
                    'noupdate': True
                }
                ir_model_data_record = models.execute_kw(DB, uid, API_KEY, 'ir.model.data', 'create', [dict_model_data])

            else:
                repeated_batches.append({'name': row['name'], 'code': row['code']})
                print(f'Repeated record {row["id"]}')

except Exception as exc:
    print(f'**************** ERROR AT THE NEXT ROW: {row["id"]} ****************')
    print(f'{row["id"] = } --- {row["code"] = } --- {row["name"] = }')
    print(f'***************** ERROR: {exc} *****************')
