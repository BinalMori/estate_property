from odoo import api,models,fields

class EstateDetail(models.Model):

    _name="estate.detail"


    name=fields.Char(string='name')
    user_id=fields.Many2one('res.users',string='user_id',default=lambda self:self.env.user)