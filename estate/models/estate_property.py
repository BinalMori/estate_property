from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from datetime import date
# from odoo.tools import float_compare
import datetime


class EstateProperty(models.Model):

    _name="estate.property"
    _order="id desc"

    name=fields.Char()
    email=fields.Char()
    image=fields.Binary(string="Image")
    property_no=fields.Char(string='Property No', readonly=True, index=True, default=lambda self: _('New'))
    #property_type=fields.Many2one("estate.property.type")
    property_type_id = fields.Many2one("estate.property.type")
    offer_ids=fields.One2many("estate.property.offer","property_id")
    buyer=fields.Many2one('res.partner',string='Buyer')
    seller=fields.Many2one('res.users',string='Salesperson',index=True)
    tag_ids=fields.Many2many("estate.property.tag",)
    description=fields.Text()
    active=fields.Boolean(default=True)
    state=fields.Selection([('n','New'),('or','Offer Receives'),('oa','Offer Accepted'),('s','Sold'),('c','Cancel')], default='n', tracking=True)
    postcode=fields.Char()
    date_availability=fields.Date(default=date.today())
    expiring_date=fields.Datetime(default=date.today())
    expected_price=fields.Float(required=True)
    selling_price=fields.Float(readonly=True)
    bedrooms=fields.Integer(default=2)
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer()
    total_area=fields.Integer(compute="_compute_total_area")
    best_price=fields.Float(compute="_compute_best_price",default=0.0)
    garden_orientation=fields.Selection([('n','North'),('s','South'),('e','East'),('w','West')])
    total_offer = fields.Integer(compute="_compute_total_offer")

    def default_get(self, fields):
        result = super(EstateProperty, self).default_get(fields)
        result['bedrooms']=4
        return result

    # def browse(self):
    #     return self.env['estate.property.tag'].browse(self.id)

    @api.model
    def create(self,vals):
        if vals.get('property_no', _('New')) == _('New'):
            vals['property_no'] = self.env['ir.sequence'].next_by_code('estate.property') or _('New')
        res = super(EstateProperty, self).create(vals)
        return res

    def unlink(self):
        if self.state not in ('n', 'c'):
            raise ValidationError('You cannot delete an record which is not in %s state.' % self.state)
        return super(EstateProperty, self).unlink()

    #dependencies
    def _compute_total_area(self):
        for record in self:
            record.total_area=record.living_area+record.garden_area

    def _compute_best_price(self):
        for record in self:
            if(record.offer_ids):
                record.best_price=max(record.offer_ids.mapped("price"))
            else:
                record.best_price=0

    def _compute_total_offer(self):
        for record in self:
            record.total_offer = self.env['estate.property.offer'].search_count([("property_id", "=", record.name)])

    # def search_read(self):
    #     records = self.env['estate.property'].search_read([('name', 'like', 'ho%')], ['name'], offset=1)
    #     for record in records:
    #         print("\n\n\n name", record['name'])

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'n'
        else:
            self.garden_area=0
            self.garden_orientation = ''

    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = ('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match == None:
                raise ValidationError('Not a valid E-mail ID')

    #buttons
    def action_cancel(self):
        for record in self:
            if record.state == 's':
                raise UserError('sold property cannot be canceled')
            else:
                record.state='c'
        return True

    def action_sold(self):
        for record in self:
            if record.state == 'c':
                raise UserError('canceled property cannot be sold')
            record.state='s'
        return True


    @api.constrains('selling_price')
    def _check_sell_price(self):
        if self.selling_price < 0.9 * self.expected_price:
            raise ValidationError("Selling price cannot be lower than 90% of the expected price.")


    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = self.name + "(copy)"

        return super(EstateProperty, self).copy(default)



    def server_action(self):
        return {
            'name': 'Wizard',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            "view_type": "form",
            'res_model': 'wizard',
            'target': 'new',
            'view_id': self.env.ref
            ('estate.wizard_view_form').id,
            'context': {'active_id': self.id},
        }
    def automated_action(self):
        print("automated action call")

    def client_action(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'title': _("Here is a new notification"),
                'message': 'property sale is here 50% off'
                }
        }

    def send_email(self):
        # mail_template = self.env.ref('estate.mail_template_demo')
        # mail_template.send_mail(self.id, force_send=True)

        self.ensure_one()
        default_template = self.env.ref('estate.mail_template_demo')
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='estate.property',
            default_res_id=self.id,
            default_use_template=bool(default_template),
            default_template_id=default_template and default_template.id,
            default_composition_mode='comment',
            custom_layout='mail.mail_notification_light',
            force_email=True,
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0)', 'The expected price must be positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')
    ]


