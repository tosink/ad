# Copyright 2021 intelligenti.io - Tosin Komolafe
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import fields, models
from odoo.addons.intel_stormware_mpohoda.models.mpohoda_request import MpohodaAPI


_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_vat_payer = fields.Boolean(
        related='company_id.is_vat_payer', 
        readonly=False)
    
    mserver_host = fields.Char(
        related='company_id.mserver_host', 
        readonly=False)
    
    mserver_port = fields.Integer(
        related='company_id.mserver_port', 
        readonly=False)
    
    mserver_user = fields.Char(
        related='company_id.mserver_user', 
        readonly=False)
    
    mserver_password = fields.Char(
        related='company_id.mserver_password', 
        readonly=False)
    
    mpohoda_payment_type_ids = fields.One2many(
        related='company_id.mpohoda_payment_type_ids', 
        readonly=False)
    
    mpohoda_invoice_type_ids = fields.One2many(
        related='company_id.mpohoda_invoice_type_ids', 
        readonly=False)
    
    store_document = fields.Boolean(
        related='company_id.store_document', 
        readonly=False)
    
    mserver_document_path = fields.Text(
        related='company_id.mserver_document_path', 
        readonly=False)
    
    def connect_mpohoda(self):
        mpohoda = MpohodaAPI(self.mserver_host, self.mserver_port, self.mserver_user, \
            self.mserver_password, self.company_id.company_registry)
        types = mpohoda.get_payment_types()
        _logger.info('PTypes %s',types)
        if types:
            for code, name in types:
                if not self.env['mpohoda.payment.type'].search([('mpohoda_code','=',code)], limit=1):
                    self.env['mpohoda.payment.type'].create({'mpohoda_code':code, 'mpohoda_acquirer':name})
        
        types = mpohoda.get_invoice_types()
        _logger.info('ITypes %s',types)
        if types:
            for code, name in types:
                if not self.env['mpohoda.invoice.type'].search([('mpohoda_code','=',code)], limit=1):
                    self.env['mpohoda.invoice.type'].create({'mpohoda_code':code, 'mpohoda_journal':name})
        return True

    
