# -*- coding: utf-8 -*-
from odoo import models, fields


class ResUsersLog(models.Model):
    _inherit = 'res.users.log'

    last_access = fields.Char(string='Hace',readonly=True, compute='_get_last_access')

    def _get_last_access(self):
        for record in self:
            access_ago = fields.Datetime.now() - record.create_date
            access_string = ""
            
            days = access_ago.days
            seconds = access_ago.seconds
            
            years, days = divmod(days, 365)
            months, days = divmod(days, 30)
            hours, seconds = divmod(seconds, 3600)
            minutes, seconds = divmod(seconds, 60)
            
            if years > 0:
                access_string += "{} años, ".format(years)
            if months > 0:
                access_string += "{} meses, ".format(months)
            if days > 0:
                access_string += "{} días, ".format(days)
            if hours > 0:
                access_string += "{} horas, ".format(hours)
            if minutes > 0:
                access_string += "{} minutos, ".format(minutes)
            
            record.last_access = access_string[:-2] if access_string else "Menos de un minuto"
