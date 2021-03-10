# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import ValidationError


class MpohodaPaymentType(models.Model):
    _name = 'mpohoda.payment.type'
    _description = 'Mpohoda Payment Type'

    acquirer_id = fields.Many2one(
        comodel_name='payment.acquirer', 
        string='Odoo Payment Method')
    
    mpohoda_acquirer = fields.Char(
        string='Mpohoda Payment Method', 
        readonly=True)
    
    mpohoda_code = fields.Char(
        string='Mpohoda Code',
        readonly=True)
    
    name = fields.Char(
        related='mpohoda_acquirer',
        string='Payment Method',
        store=True)
    
    company_id = fields.Many2one(
        comodel_name='res.company', 
        string='Company', 
        required=False,
        default=lambda self: self.env['res.company']._company_default_get('mpohoda.payment.type'))
    
    
    @api.constrains('acquirer_id')
    def _check_acquirer(self):
        for t in self:
            if t.acquirer_id:
                if self.search_count([('acquirer_id','=',t.acquirer_id.id)]) > 1:
                    raise ValidationError(_('Payment acquirer must be unique!'))



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
    
    invoice_type = fields.Selection(
        [('out_invoice',_('Invoice')),('in_invoice',_('Vendor Bill')),
        ('out_refund',_('Credit Note')),('in_refund',_('Vendor Credit note'))],
        string='Invoice Type')

    
    company_id = fields.Many2one(
        comodel_name='res.company', 
        string='Company', 
        required=False,
        default=lambda self: self.env['res.company']._company_default_get('mpohoda.invoice.type'))

    @api.constrains('journal_id')
    def _check_journal(self):
        for t in self:
            if t.journal_id and t.invoice_type:
                if self.search_count([('journal_id','=',t.journal_id.id),('invoice_type','=',t.invoice_type)]) > 1:
                    raise ValidationError(_('Journal and invoice type must be unique!'))






