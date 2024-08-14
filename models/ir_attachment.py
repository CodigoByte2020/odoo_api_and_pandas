from odoo import fields, models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    op_document_type_id = fields.Many2one(comodel_name='op.document.type', string='Tipo de documento')
    document_type_id = fields.Many2one('op.document.type', string='Tipo de Documento')
    drive_url = fields.Char(string="Gdrive URL")
    drive_id = fields.Char(string="Gdrive ID")
    # document_name = fields.Char(string="Nombre del Documento")
