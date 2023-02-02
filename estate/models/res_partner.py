# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    employee_name = fields.Char(string="Employee Name")