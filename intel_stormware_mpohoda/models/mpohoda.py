# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID


class MpohodaPaymentType(models.Model):
    _name = 'mpohoda.payment.type'
    _description = 'Mpohoda Payment Type'

    acquirer_id = fields.Many2one(
        comodel_name='payment.acquirer', 
        string='Odoo Payment Method')
    
    mpohoda_acquirer = fields.Char(
        string='Mpohoda Payment Method', 
        readonly=True)
    
    company_id = fields.Many2one(
        comodel_name='res.company', 
        string='Company', 
        required=True,
        default=lambda self: self.env['res.company']._company_default_get('mpohoda.payment.type'))



class MpohodaInvoiceType(models.Model):
    _name = 'mpohoda.invoice.type'
    _description = 'Mpohoda Invoice Type'

    journal_id = fields.Many2one(
        comodel_name='account.journal', 
        string='Odoo Journal')
    
    mpohoda_journal = fields.Char(
        string='Mpohoda Journal', 
        readonly=True)
    
    mpohoda_code = fields.Char(
        string='Mpohoda Code',
        readonly=True)
    
    company_id = fields.Many2one(
        comodel_name='res.company', 
        string='Company', 
        required=True,
        default=lambda self: self.env['res.company']._company_default_get('mpohoda.invoice.type'))




