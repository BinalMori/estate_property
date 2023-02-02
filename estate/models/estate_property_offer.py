from odoo import api,models,fields
from datetime import date,timedelta,datetime
from odoo.exceptions import UserError,ValidationError

class EstatePropertyOffer(models.Model):

    _name="estate.property.offer"
    _order="price desc"

    price=fields.Float()
    status=fields.Selection([('a','Accepted'),('r','Refused')])
    partner_id=fields.Many2one('res.partner',required=True)
    property_id=fields.Many2one('estate.property',required=True)
    validity=fields.Integer(default=7)
    date_deadline=fields.Date(compute="_compute_date_deadline",inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id")

    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0.0)', 'An offer price must be positive.'),
    ]

    @api.model
    def create(self, vals):
        offer = super(EstatePropertyOffer, self).create(vals)
        offer.property_id.state = 'or'

        if offer.price<offer.property_id.best_price:
            raise UserError("please enter offer amount greater than Best price")

        return offer


    def _compute_total_offer(self):
        for record in self:
            record.total_offer = self.env['estate.property.offer'].search_count([("property_id", "=", record.name)])


    def action_accepted(self):
        for record in self:
            record.status = 'a'
            record.property_id.state='oa'
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_total_offer(self):
        for record in self:
            record.property_type_id = self.env['estate.property'].search_count([("offer_ids", "=", record.name)])
        return True


    def action_refused(self):
        for record in self:
            record.status = 'r'
            record.property_id.selling_price = 0
            record.property_id.buyer = None
        return True


    def _compute_date_deadline(self):
            for record in self:
                record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        create_date = self.create_date
        create_date = create_date.date()
        difference = self.date_deadline - create_date


        if create_date > self.date_deadline:
            raise ValidationError("date deadline should be after create date")
        else:
            self.validity = difference.days

    # def lower_amount(self):
    #     for record in self:
    #         if record.price<record.property_id.best_price:
    #             raise ValueError("please enter offer amount greater than expected price")
