# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID


class AccountTax(models.Model):
    _inherit = 'account.tax'

    mpohoda_vat = fields.Selection(
        [('none','None'),('high','High'),('low','Low'),('third','Third'),
        ('historyHigh','History High'),('historyLow','History Low'),
        ('historyThird','History Third')],
        string='Mpohoda Rate Vat', 
        default='high')



    

    