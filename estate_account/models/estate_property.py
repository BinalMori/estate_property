from odoo import models,fields,api,Command

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        self.env["account.move"].create(
            {
                'partner_id': super().buyer,
                'move_type': 'out_invoice',
                "invoice_line_ids": [
                    Command.create({
                        "name": super().name,
                        "quantity": 1,
                        "price_unit": super().selling_price + (lambda x : x * 0.06)(super().selling_price),
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100,
                    }),
                ],
            }
        )
        return super().action_sold()