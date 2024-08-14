import base64
import io

from odoo import fields, models
import pandas as pd

# TODO:
#     first: I have imported records of op.campus - LOCAL
#     second: I imported records of op.modality - LOCAL
#     third: I do not import records of op.practices.type because there is not any record
#     fourd: I should import records of op.batch


# ME QUEDEN PROCESANDO LA FILA 300
# REVISAR ESPECIALIDAD EN TRASTORNOS AUTISTAS. Y ESPECIALIDAD EN TRASTORNOS AUTISTAS


class OpBatch(models.Model):
    _inherit = 'op.batch'

    def process_batch(self):
        '''
            Processing data of op_batch model:
            One: Prepare template of data. OK
            Two: Download native records of odoo 12.
            Three: Index all models with its ids extern on template csv.
            Four: Convert records to uppercase.
            Five: Delete duplicate records. (code)
            Six: Related records of op.batch with records of op.course
        '''
        path_file = '/home/gianmarco/PycharmProjects/isep_16/odoo16isep/addons-extra/addons_uisep/isep_student_custom/models/op.batch.5.csv'
        with open(path_file, 'r') as csv_file:
            names = [
                'id', 'name', 'course_id/id', 'start_date', 'coordinator/id', 'campus_id/id', 'uvic_program', 'code',
                'company_id/id', 'end_date', 'modality_id/id', 'students_limit', 'sepyc_program', 'expiration_days',
                'date_diplomas', 'academic_year', 'generation', 'hours', 'credits', 'ects', 'practical_hours_total',
                'independent_hours_total', 'theoretical_hours_total', 'hours_total', 'practical_hours_credits',
                'independent_hours_credits', 'theoretical_hours_credits', 'credits_total', 'days_week', 'schedule',
                'contact_class', 'type_practices/id', 'acknowledgments', 'reconeixements'
            ]
            txt_lines = ''
            batches = pd.read_csv(csv_file, sep=',', names=names)
            batches['name'] = batches['name'].str.upper()
            batches.drop_duplicates(subset=['name'], inplace=True)
            batches.drop_duplicates(subset=['code'], inplace=True)

            # I WOULD FILL EMPTY VALUES OF DATAFRAME
            # columns_to_fill = ['date_diplomas', 'generation', 'contact_class', 'acknowledgments', 'reconeixements']
            # batches[columns_to_fill] = batches[columns_to_fill].fillna(value='')
            batches.fillna(value='', inplace=True)

            for index, row in batches.iterrows():
                txt_lines += '"'
                txt_lines += '","'.join(row)
                txt_lines += '"'
                txt_lines += '\n'
        return self.button_export_txt(txt_lines)

    def process_batch_add_is_imported_record(self):
        path_file = '/home/gianmarco/PycharmProjects/isep_16/odoo16isep/addons-extra/addons_uisep/isep_student_custom/models/op.batch.5.process.1.csv'
        with open(path_file, 'r') as csv_file:
            names = [
                "id", "name", "course_id/id", "start_date", "coordinator/id", "campus_id/id", "uvic_program", "code",
                "company_id/id", "end_date", "modality_id/id", "students_limit", "sepyc_program", "expiration_days",
                "date_diplomas", "academic_year", "generation", "hours", "credits", "ects", "practical_hours_total",
                "independent_hours_total", "theoretical_hours_total", "hours_total", "practical_hours_credits",
                "independent_hours_credits", "theoretical_hours_credits", "credits_total", "days_week", "schedule",
                "contact_class", "type_practices/id", "acknowledgments", "reconeixements", "is_imported_record"
            ]
            txt_lines = ''
            batches2 = pd.read_csv(csv_file, sep=',', names=names)
            batches2['is_imported_record'][1:] = 'True'
            # print(batches2.head())
            batches2.fillna(value='', inplace=True)
            for index, row in batches2.iterrows():
                txt_lines += '"'
                txt_lines += '","'.join(row)
                txt_lines += '"'
                txt_lines += '\n'
        return self.button_export_txt(txt_lines)

    def button_export_txt(self, txt_lines):
        file = io.BytesIO()
        file.write(txt_lines.encode('utf-8'))
        content = file.getvalue()
        datas = base64.b64encode(content)
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        attachment_model = self.env['ir.attachment']
        attachment_id = attachment_model.create({
            'name': 'op.batch.5.process.2.csv',
            'datas': datas
        })
        download_url = f'/web/content/{attachment_id.id}?download=true'
        return {
            'type': 'ir.actions.act_url',
            'url': f'{base_url}{download_url}',
            'target': 'new',
        }
