# -*- coding: utf-8 -*-

from odoo import fields, models

STATUS_SELECTION = [
    ('valid', 'Vigente'),
    ('graduate', 'Graduado'),
    ('low', 'Baja')
]


class OpAdmission(models.Model):
    _inherit = 'op.admission'

    academic_record_closing = fields.Date(string='Cierre de expediente académico')
    start_date = fields.Date(string='Fecha de Inicio', copy=False)
    unsubscribed_date = fields.Date(string='Fecha de Baja')

    # TODO: HAY UN MISMO CAMPO EN ESTUDIANTE
    status = fields.Selection(selection=STATUS_SELECTION, default='valid', string='Estado de la admisión')
