# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.addons.intel_stormware_mpohoda.models.mpohoda_request import MpohodaAPI
import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    mpohoda_status = fields.Selection(
        [('ready','Ready'),('sent','Sent'),('error','Error')],
        string='Mpohoda Status',
        default='ready',
        track_visibility='onchange',
        required=True)
    
    mpohoda_type_id = fields.Many2one(
        comodel_name='mpohoda.payment.type', 
        string='Mpohoda Payment Type',
        default=lambda self: self.env['mpohoda.payment.type'].search([],limit=1),
        required=False)
    

    @api.multi
    def invoice_validate(self):
        res = super(AccountInvoice, self).invoice_validate()
        company = self.company_id
        mpohoda = MpohodaAPI(company.mserver_host, company.mserver_port, company.mserver_user, \
            company.mserver_password, company.company_registry)
        for invoice in self:
            try:
                _logger.info('Sending invoice %s to MPOHODA'%invoice.name)
                mpohoda.generate_invoice(invoice)
                invoice.mpohoda_status = 'sent'
                _logger.info('Generated invoice %s from MPOHODA'%invoice.name)
            except Exception as e:
                invoice.mpohoda_status = 'error'
                _logger.info('Error for invoice %s from MPOHODA: %s'%(invoice.name,e))

        return res


    

    

    