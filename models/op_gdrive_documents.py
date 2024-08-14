# -*- coding: utf-8 -*-

from odoo import fields, models


class OpGdriveDocuments(models.Model):
    _name = 'op.gdrive.documents'

    student_id = fields.Many2one('op.student')
    document_type_id = fields.Many2one('op.document.type', string='Tipo de Documento')
    drive_url = fields.Char(string="Gdrive URL")
    drive_id = fields.Char(string="Gdrive ID")
    document_name = fields.Char(string="Nombre del Documento")
