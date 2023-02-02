from odoo import fields,models

class InheritedModel(models.Model):

    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "seller", domain="['|',('state', '=', 'n'),('state','=','or')]")
    employee_name=fields.Char(string="Employee Name")


