# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID


class AccountMove(models.Model):
    _inherit = 'account.move'

    mpohoda_status = fields.Selection(
        [('ready','Ready'),('sent','Sent'),('error','Error')],
        string='Mpohoda Status',
        default='ready',
        required=True)
    