from odoo import api, fields, models
import logging
import pandas as pd

_logger = logging.getLogger(__name__)


class RecordRequestList(models.Model):
    _inherit = 'record.request.list'

    def import_document_types(self):
        active_ids = self._context.get('active_ids', [])
        document_lists = self.browse(active_ids)
        file_path = '/home/gianmarco/PycharmProjects/ISEP_16EE/odoo16isep/addons-extra/addons_uisep/isep_student_custom/models/op.document.type.csv'
        values_list = []
        with open(file_path, 'r') as csv_file:
            names = ['name']
            people = pd.read_csv(csv_file, sep=',', names=names).drop_duplicates(subset=names)
            for index, row in people.iterrows():
                if index >= 1:
                    values_list.append((0, 0, {'document': row['name']}))
        _logger.info(values_list)
        for document_list in document_lists:
            document_list.update({'record_request_list_line_ids': values_list})

    # @api.model_create_multi
    # def create(self, values_list):
    #     res = super(RecordRequestList, self).create(values_list)
    #     return res
