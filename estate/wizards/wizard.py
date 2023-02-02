from odoo import models, fields, api

class Wizard(models.TransientModel):

    _name = 'wizard'


    name=fields.Char(string='Name')


    def wizard_create(self):
        for record in self:
            print(record.name)

