from odoo import fields,models

class SalesOrderLine(models.Model):

    _inherit = "sale.order.line"

    extra_charge = fields.Float(string='ExtraCharge')


