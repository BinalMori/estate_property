from odoo import api,models,fields, _

class EstatePropertyType(models.Model):

    _name="estate.property.type"
    _order='name'
    # _inherit='estate.property'

    property_no = fields.Char(readonly=True, default=lambda self: _('New'))
    property_ids = fields.One2many("estate.property", "property_type_id")
    name=fields.Char()
    sequence=fields.Integer('Sequence', default=1)
    highest_price=fields.Float(compute="_compute_highest_price")
    total_offer = fields.Integer(compute="_compute_total_offer")
    offer_ids=fields.One2many("estate.property.offer","property_type_id")
    offer_count = fields.Integer(compute="_compute_total_offer")


    _sql_constraints = [
        ('unique_tag', 'unique(name)', 'A property type name must be unique, this type is already used.')
    ]


    def _compute_total_offer(self):
        for record in self:
            self.offer_count = self.env['estate.property.offer'].search_count([("property_type_id", "=", record.name)])

    @api.model
    def create(self, vals):
        if vals.get('property_no', _('New')) == _('New'):
            vals['property_no'] = self.env['ir.sequence'].next_by_code('estate.property.type') or _('New')
        res = super(EstatePropertyType, self).create(vals)
        return res

    def write(self,vals):
        if not self.property_no and not vals.get('property_no'):
            vals['property_no'] = self.env['ir.sequence'].next_by_code('estate.property.type')
        return super(EstatePropertyType, self).write(vals)

    # @api.model
    # def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    #     args = args or []
    #     domain = []
    #     if name:
    #         domain = ['|', ('name', operator, name), ('state', operator, name),('highest_price', operator, name)]
    #     return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)


    def _compute_highest_price(self):
        self.highest_price = self.env["estate.property"].search([('property_type_id', '=', self.name)], order = 'expected_price desc', limit=1).expected_price



    # def action_view_offer(self):
    #     return

