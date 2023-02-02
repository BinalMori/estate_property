from odoo import models, fields, api

class Report(models.TransientModel):

    _name = 'report'


    Date_From=fields.Date(string='date from')
    Date_To=fields.Date(string='date to')

    def print_report(self):
        domain=[]
        if self.Date_From:
            domain=[('date_availability','>=',self.Date_From)]

        if self.Date_To:
            domain=[('expiring_date','<=',self.Date_To)]
        property=self.env['estate.property'].search_read(domain)
        data={
            'form_data': self.read()[0],
            'property':property
        }
        return self.env.ref('estate.action_report_pdf').report_action(self,data=data)

