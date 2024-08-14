# -*- coding: utf-8 -*-

from odoo import fields, models


class OpDocumentType(models.Model):
    _name = 'op.document.type'

    name = fields.Char('Nombre', required=True)
    code = fields.Char('Codigo', required=True)
    required = fields.Boolean('Obligatorio', default=False)

    _sql_constraints = [('unique_document_type_code', 'unique(code)', 'El código es único por documento!')]
