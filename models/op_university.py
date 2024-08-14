# -*- coding: utf-8 -*-

from odoo import fields, models

class OpUniversity(models.Model):
    _name= "op.university"
    _description = "Universidad"

    name = fields.Char("Nombre", required=True, copy=False,size=128)
    code = fields.Char("Codigo", required=True, copy=False,size=32)
    