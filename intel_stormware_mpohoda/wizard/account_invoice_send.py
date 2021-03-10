# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree

from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"

    def get_mpohoda_document(self):
        active_id = self.env.context.get('active_id', False)
        if self.env.context.get('params', False):
            params = self.env.context.get('params', False)
            if params['model'] == 'account.invoice':
                active_id = params['id']
        invoice = self.env["account.invoice"].browse(active_id)
        
        mpohoda_attachment_ids = self.env["ir.attachment"].search(
            [
                ("res_model", "=", 'account.invoice'),
                ("res_id", "=", invoice.id),
                ("description","=","MPOHODA")
            ]
        )
        if mpohoda_attachment_ids:
            self.attachment_ids = [(6,0,mpohoda_attachment_ids.ids)]