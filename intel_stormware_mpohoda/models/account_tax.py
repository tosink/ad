# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID


class AccountTax(models.Model):
    _inherit = 'account.tax'

    mpohoda_vat = fields.Selection(
        [('low','Low'),('medium','Medium'),('high','High')],
        string='Mpohoda Rate Vat', 
        default='high')
    

    