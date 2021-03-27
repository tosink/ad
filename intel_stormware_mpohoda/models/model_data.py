# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, SUPERUSER_ID


class ModelData(models.Model):
    _inherit = 'ir.model.data'

    import_name = fields.Char('Import Name')



    

    