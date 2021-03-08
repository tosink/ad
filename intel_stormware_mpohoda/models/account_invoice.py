# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    mpohoda_status = fields.Selection(
        [('ready','Ready'),('sent','Sent'),('error','Error')],
        string='Mpohoda Status',
        default='ready',
        track_visibility='onchange',
        required=True)
    
    mpohoda_acquirer_id = fields.Many2one(
        comodel_name='mpohoda.payment.type', 
        string='Mpohoda Payment Type',
        default=lambda self: self.env['mpohoda.payment.type'].search([],limit=1),
        required=True)
    

    

    