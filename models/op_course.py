import base64
import io
from pprint import pprint

from odoo import api, fields, models
import pandas as pd


class OpCourse(models.Model):
    _inherit = 'op.course'

    # is_imported_record = fields.Boolean(string='¿Es registro importado de la 12 a la 16?', default=False)

    @api.model_create_multi
    def create(self, values_list):
        res = super(OpCourse, self).create(values_list)
        pprint(res)
        return res

    def process_courses(self):
        # If this method run, the program is well
        # The program is well if this method run
        # when this method run, all the code is good
        # all the code is good when this method run
        # path_file = '/home/gianmarco/PycharmProjects/isep_16/odoo16isep/addons-extra/addons_uisep/isep_student_custom/models/op.course.csv'
        # path_file = '/home/gianmarco/PycharmProjects/isep_16/odoo16isep/addons-extra/addons_uisep/isep_student_custom/models/op.course.nativos.and.process.csv'
        path_file = '/home/gianmarco/PycharmProjects/isep_16/odoo16isep/addons-extra/addons_uisep/isep_student_custom/models/op.area.course.csv'
        with open(path_file, 'r') as csv_file:
            # names = ['id', 'name', 'code', 'evaluation_type', 'fees_term_id/id', 'company_id/id', 'lang']
            names = ['name', 'code']
            # subset = ['name', 'code']
            txt_lines = ''
            courses = pd.read_csv(csv_file, sep=',', names=names)
            courses['name'] = courses['name'].str.upper()
            courses.drop_duplicates(subset=['name'], inplace=True)
            courses.drop_duplicates(subset=['code'], inplace=True)
            print(courses)
            # courses.drop_duplicates(subset=subset, inplace=True)
            # courses.drop(courses.index[[1, 3, 5, 21]])
            # courses.drop(index=[1, 3, 5], axis=0, inplace=True)
            # courses.drop(index=[3], axis=0, inplace=True)
            # courses.drop(index=[5], axis=0, inplace=True)
            # courses.drop(index=[21], axis=0, inplace=True)
            # courses.drop(courses['code'] in ['NP', 'PC', 'MP', 'MN'], axis=0, inplace=True)
            for index, row in courses.iterrows():
                txt_lines += '"'
                txt_lines += '","'.join(row)
                txt_lines += '"'
                txt_lines += '\n'
            # TODO: REVISAR EL CASO DEL CURSO MÁSTER EN SEXOLOGÍA CLÍNICA Y TERAPIA DE PAREJAS
        return self.button_export_txt(txt_lines)

    def button_export_txt(self, txt_lines):
        '''
            If the code is bad, the program will not run
            If the method is bad, the program should not run
        '''
        file = io.BytesIO()
        file.write(txt_lines.encode('utf-8'))
        content = file.getvalue()
        datas = base64.b64encode(content)
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        attachment_model = self.env['ir.attachment']
        attachment_id = attachment_model.create({
            'name': 'op.course.nativos.and.process.process.csv',
            'datas': datas
        })
        download_url = f'/web/content/{attachment_id.id}?download=true'
        return {
            'type': 'ir.actions.act_url',
            'url': f'{base_url}{download_url}',
            'target': 'new',
        }
