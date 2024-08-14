from pprint import pprint
from odoo_connection import *
import pandas as pd

try:
    def get_df_merge_subjects_and_courses():
        subject_fields = ['id', 'code', 'name', 'subject_type', 'type', 'credits', 'grade_weightage', 'active',
                          'course_id', 'company_id']
        subject_domain = ['&', ['course_id', '!=', False], '|', ['active', '=', True], ['active', '=', False]]
        subjects_odoo12 = models_odoo12.execute_kw(DB_ODOO12, uid_odoo12, PASSWORD_ODOO12, 'op.subject', 'search_read',
                                                   [subject_domain], {'fields': subject_fields, 'limit': None})
        df_subjects_odoo12 = pd.DataFrame(subjects_odoo12)
        df_subjects_odoo12.drop_duplicates(subset=['code'], inplace=True)
        df_subjects_odoo12.drop_duplicates(subset=['name'], inplace=True)
        df_subjects_odoo12['name_two'] = df_subjects_odoo12['course_id'].apply(lambda x: x[1].upper())

        course_fields = ['id', 'name']
        course_names = list(set(df_subjects_odoo12['name_two']))
        course_domain = ['&', ['name', 'in', list(set(course_names))], '|', ['active', '=', True],
                         ['active', '=', False]]
        courses_odoo16 = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'op.course', 'search_read',
                                                  [course_domain], {'fields': course_fields, 'limit': None})
        df_courses_odoo16 = pd.DataFrame(courses_odoo16)
        df_courses_odoo16['name_three'] = df_courses_odoo16['name'].apply(lambda x: x.upper())

        df_merge_subjects_and_courses = pd.merge(left=df_subjects_odoo12, right=df_courses_odoo16, left_on='name_two',
                                                 right_on='name_three', suffixes=('_subject', '_course'))
        return df_merge_subjects_and_courses


    def drop_duplicate_subjects(df_merged):
        subject_fields = ['code', 'name']
        subject_domain = ['|', ['active', '=', True], ['active', '=', False]]
        subjects_odoo16 = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'op.subject', 'search_read',
                                                   [subject_domain], {'fields': subject_fields, 'limit': None})
        df_subjects_odoo16 = pd.DataFrame(subjects_odoo16)
        mask_code = df_merged['code'].isin(df_subjects_odoo16['code'])
        mask_name = df_merged['name_subject'].isin(df_subjects_odoo16['name'])
        # mask_final = ~mask_code & ~mask_name
        mask_final = ~(mask_code | mask_name)
        return df_merged[mask_final]


    def get_company_id(company_name):
        company_dict = {
            'ISEP INTERNACIONAL, LLC': 'ISEP INTERNACIONAL LLC',
            'Isep Latam': 'ISEP LATAM',
            'ISEP BRASIL': 'ISEP INTERNACIONAL LLC - (BRASIL)'
        }
        company_name = company_dict.get(company_name, None)
        company_domain = ['&', ['name', '=', company_name], '|', ['active', '=', True], ['active', '=', False]]
        company_id = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'res.company', 'search_read',
                                              [company_domain], {'fields': ['id'], 'limit': None})[0]['id']
        return company_id


    def create_subjects(df_subjects):
        colum_names = ['code', 'subject_type', 'type', 'grade_weightage', 'active']
        for index, row in df_subjects.iterrows():
            company_id = get_company_id(row['company_id'][1])
            print(f'CODE: {row["code"]} - COMPANY: {row["company_id"][1]}')
            values_to_create = {
                'name': row['name_subject'],
                'credit_point': row['credits'],
                'is_imported_record': True,
                'course_id': row['id_course'],
                'company_id': company_id
            }
            values_to_create.update({colum_name: row[colum_name] for colum_name in colum_names})
            subject_id = models_odoo16.execute_kw(DB_ODOO16, uid_odoo16, API_KEY_ODOO16, 'op.subject', 'create',
                                                  [values_to_create])
            print(f'RECORD WAS SUCCESSFULLY CREATED => {subject_id}')


    df_merged_subjects_courses = get_df_merge_subjects_and_courses()
    df_final = drop_duplicate_subjects(df_merged_subjects_courses)
    create_subjects(df_final)

except Exception as exc:
    print(f'************************* EXCEPTION ************************* {exc = }')
