# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree

from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class AccountInvoiceSend(models.TransientModel):
    _inherit = "account.invoice.send"

    @api.onchange('template_id')
    def onchange_template(self):
        _logger.info('TEMPLATE ATTACHMENT')
        self.attachment_ids = [(6,0,[])]