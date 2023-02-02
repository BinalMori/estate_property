from odoo import models,fields

class ContactForm(models.Model):

    _name="contact.form"


    name=fields.Char(string='name')
    email_from=fields.Char(string='email')