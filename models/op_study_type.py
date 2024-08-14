
from odoo import models, fields


class OpStudyType(models.Model):
    _name = "op.study.type"
    _description = "Tipo de estudio"

    name = fields.Char('Nombre', size=128, required=True)
    code = fields.Char('Codigo', size=12, required=True)
