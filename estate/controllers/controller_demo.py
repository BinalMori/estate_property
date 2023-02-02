from odoo import http
from odoo.http import request, route
import json
from datetime import datetime

class ControllerDemo(http.Controller):

    @http.route(['/estate_data/'], type='http', auth='public', website='True')
    def estate_data(self, **post):
        data = request.env['estate.property'].sudo().search([])
        values = {
        'records':data
        }
        return request.render('estate.estate_data', values)

class ContactForm(http.Controller):

    @http.route('/contact_form', type="http", auth="public", website=True)
    def contact_form(self, **kw):
        return http.request.render('estate.contact_form', {})


    @http.route('/create/contact', type="http", auth="public", website=True)
    def create_contact(self, **kw):
        # print("Data Received.....", kw)
        request.env['contact.form'].sudo().create(kw)
        request.env['crm.lead'].sudo().create(kw)
        return request.render("estate.thanks", {})



## class jsonProductData(http.Controller):
#
#     @http.route('/json/products',type='http', auth="public",csrf=False)
#     def product_data(self):
#         data=http.request.env['product.product'].search([])
#         product=data.read()
#         # a=json.dumps(product)
#         # print(a)
#         return http.Response(json.dumps(product), content_type='application/json;charset=utf-8', status=200)
#
#         # search([('name', '=', 'Acoustic Bloc Screens')])
        # data=request.env['product.product'].search([])
        # record=[]
        # for records in data:
        #     record.append(records)
        # return record
        #
# Controller file

