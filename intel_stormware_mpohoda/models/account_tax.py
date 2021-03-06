# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID


class AccountTax(models.Model):
    _inherit = 'account.tax'

    