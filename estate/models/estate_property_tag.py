from odoo import api,models,fields, _
from odoo.exceptions import UserError
from datetime import date
import datetime

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _order = 'name'

    tag_id = fields.Char(string='Tag ID', readonly=True, index=True, default=lambda self: _('New'))
    name = fields.Char()
    colour = fields.Integer()
    ref = fields.Char()


    @api.model
    def create(self, vals):
        if vals.get('tag_id', _('New')) == _('New'):
            vals['tag_id'] = self.env['ir.sequence'].next_by_code('estate.property.tag') or _('New')
        res = super(EstatePropertyTag, self).create(vals)
        return res
    def url_action(self):
        return {
            "type": "ir.actions.act_url",
            "url": "https://odoo.com",
            "target": "new",
        }


    # _sql_constraints = [
    #     ('unique_tag', 'unique(name)', 'This tag is already used define the tag must be unique.')
    # ]

    # def copy(self,default=None):
    #     if default is None:
    #         default = {}
    #     if not default.get('name'):
    #         default['name'] = _("%s (copy)", self.name)
    #     return super(EstatePropertyTag, self).copy(default)

    # def read_group(self,fields,groupby,orderby,offset=0):
    #     tag = self.env["estate.property.tag"].read_group([], fields=['ref'], groupby=['ref'], orderby=['name'])
    #     return tag

    # def flush(self):
    #     pass

