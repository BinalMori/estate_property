from odoo import models,fields,api

class Res_Config_Settings(models.TransientModel):
   _inherit = 'res.config.settings'

   days = fields.Integer('add model',config_parameter ='estate.days')