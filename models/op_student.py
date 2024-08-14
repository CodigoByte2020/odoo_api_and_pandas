# -*- coding: utf-8 -*-
import base64
import io
from pprint import pprint
import pandas as pd
from odoo import api, fields, models


class OpStudent(models.Model):
    _inherit = "op.student"

    # ***************************** CAMPOS WILLIAM *******************************
    university_id = fields.Many2one('op.university', string='Universidad de Procedencia')
    study_type_id = fields.Many2one('op.study.type', string='Tipo de estudio')
    year_end_studies = fields.Integer(string='Finalización estudios')
    date_title = fields.Integer(string='Fecha de titulacion')
    sepyc_program = fields.Boolean(string='Programa Sepyc / Sep',default=False)
    status_documentation = fields.Selection([
            ('complete', 'Completado'),
            ('in process', 'En proceso'),
            ('Not send', 'No enviada')
        ], string='Estado de documentación')
    
    status_student = fields.Selection(
        [('valid', 'Vigente'), ('graduate', 'Graduado'),
         ('low', 'Baja')], default='valid', string="Student Status",readonly=True)
         #compute='_compute_determine_status')

    admission_ids = fields.One2many('op.admission', 'student_id',
                                    string="Admisiones")
    user_log_ids = fields.One2many('res.users.log', compute='_compute_user_log_ids', string="Accesos")
    # ********************************* CAMPOS GIANMARCO ****************************
    place_birth = fields.Char(string='Lugar de nacimiento')  # OK
    op_document_type_id = fields.Many2one(comodel_name='op.document.type', string='Tipo de documento')  # OK
    document_number = fields.Char(string='Número de documento')  # OK
    grades_line_ids = fields.One2many(comodel_name='student.grade', inverse_name='student_id', string='Notas')
    document_ids = fields.One2many(comodel_name='op.gdrive.documents', inverse_name='student_id', string='Documentación')
    delay = fields.Boolean(string="Delay")  # OK
    ir_attachment_ids = fields.One2many(related='partner_id.ir_attachment_ids')
    # ***********************************************************************************

    def _compute_user_log_ids(self):
        for student in self:
            if student.user_id:
                student.user_log_ids = self.env['res.users.log'].search([('create_uid', '=', student.user_id.id)], order='create_date desc')
            else:
                student.user_log_ids = self.env['res.users.log']

    @api.model_create_multi
    def create(self, values_list):
        res = super(OpStudent, self).create(values_list)
        pprint(res)
        return res

    def button_export_txt(self):
        txt_lines = self.generate_txt()
        file = io.BytesIO()
        file.write(txt_lines.encode('utf-8'))
        content = file.getvalue()
        datas = base64.b64encode(content)
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        attachment_model = self.env['ir.attachment']
        attachment_id = attachment_model.create({
            'name': 'students.txt',
            'datas': datas
        })
        download_url = f'/web/content/{attachment_id.id}?download=true'
        return {
            'type': 'ir.actions.act_url',
            'url': f'{base_url}{download_url}',
            'target': 'new',
        }

    def generate_txt(self):
        txt_lines = ''
        active_ids = self._context.get('active_ids')
        students = self.browse(active_ids)
        field_names = [
            'birth_date',
            'document_number',
            'document_type_id',
            'email',
            'name',
            'partner_id/ID',
            'place_birth'
        ]
        txt_lines += ','.join(field_names)
        txt_lines += '\n'
        for student in students:
            student_values = [
                student.birth_date and student.birth_date.strftime("%Y-%m-%d") or '',
                student.document_number or '',
                student.op_document_type_id and student.op_document_type_id.name or '',
                student.email or '',
                student.name or '',
                student.partner_id.id and str(student.partner_id.id) or '',
                student.place_birth and student.place_birth.strftime("%Y-%m-%d") or ''
            ]
            txt_lines += ','.join(student_values)
            txt_lines += '\n'
        return txt_lines
