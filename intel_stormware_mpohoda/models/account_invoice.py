# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    mpohoda_status = fields.Selection(
        [('ready','Ready'),('sent','Sent'),('error','Error')],
        string='Mpohoda Status',
        default='ready',
        required=True)
    