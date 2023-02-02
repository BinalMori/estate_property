from odoo import api,models,fields

class Invoice(models.Model):
    _inherit = "stock.quant"
    button_visible = fields.Boolean(default=True,compute='onchange_a_b')
    button= fields.Boolean()
    a=fields.Integer()
    b = fields.Integer()


    def Approved_Inventory(self):
        print("approved")
        self.button= True




    def onchange_a_b(self):
        limit = int(self.env['ir.config_parameter'].sudo().get_param('estate.limit'))
        s = self.quantity
        ratio = (s * limit) / 100
        self.a = s + ratio
        self.b = s - ratio
        print(self.a)
        print(self.b)
        q = self.inventory_quantity
        for record in self:
            if q > record.a or q < record.b:
                self.button_visible = False
            else:
                self.button_visible = True
