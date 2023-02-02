from odoo import models,fields,api

class Res_Config_Settings(models.TransientModel):
   _inherit = 'res.config.settings'

   limit = fields.Integer(string='limit',config_parameter ='estate.limit')
