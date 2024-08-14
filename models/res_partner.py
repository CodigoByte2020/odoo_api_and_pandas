from pprint import pprint
import pandas as pd
from odoo import api, fields, models
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, values_list):
        res = super(ResPartner, self).create(values_list)
        pprint(res)
        return res

    def create_partners(self):
        file_path = '/home/gianmarco/PycharmProjects/ISEP_16EE/odoo16isep/addons-extra/addons_uisep/isep_student_custom/models/op.student.csv'
        records = []
        with open(file_path, 'r') as csv_file:
            names = ['name', 'email', 'birth_date', 'country_id']
            people = pd.read_csv(csv_file, sep=',', names=names)
            for index, row in people.iterrows():
                if index >= 1:
                    records.append({
                        'name': row['name'],
                        'email': row['email'],
                        'birth_date': row['birth_date']
                    })
        _logger.info('JAJAJ')
        partners = self.env['res.partner'].sudo().search([])
        partner_emails = partners.mapped(lambda x: x.email)
        partner_phones = partners.mapped(lambda x: x.phone)
        records_to_create = []
        for record in records:
            # self.validate_email(record, partner_emails)
            # self.validate_phone(record, partner_phones)
            # self.create_type_document(record)
            records_to_create.append(record)

        self.create(records_to_create)
        # self.env['op.student'].create(records)

    @staticmethod
    def validate_email(record, partner_emails):
        if record['email'] not in partner_emails:
            raise ValidationError('El email ya existe')

    @staticmethod
    def validate_phone(record, partner_phones):
        if record['phone'] not in partner_phones:
            raise ValidationError('El teléfono ya existe')


    # def create_type_document(self, record):
    #     country_id = record.get('country_id', False)
    #     if country_id:
    #         country = self.env['res.country'].browse(country_id)
    #         if country.code == 'MX':
    #             raise ValidationError('¡Debes crear una Lista de documentos documentos mexicanos !!!')
    #         elif country.code != 'MX':
    #             raise ValidationError('¡Debes crear una Lista de documentos extranjeros !!!')
