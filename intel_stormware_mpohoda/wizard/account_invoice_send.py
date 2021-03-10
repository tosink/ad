# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree

from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)
# from odoo.osv.orm import setup_modifiers


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"

    def _get_document(self):
        active_id = self.env.context.get('active_id', False)
        return [(6,0,[])]
    
    mpohoda_attachment_ids = fields.Many2many(
        related='attachment_ids', 
        string='Mpohoda Attachment IDs',
        default=_get_document)