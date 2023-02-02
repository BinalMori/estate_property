from odoo import http
import json
from odoo.http import request, route
from json import JSONEncoder
from odoo.tools import date_utils

class ProductController(http.Controller):

    @http.route('/products',type='http', auth='public')
    def products(self, **kwargs):
        data = request.env['product.product'].sudo().search_read({})
        return json.dumps(data,default=date_utils.json_default)

    @http.route('/products/<int:id>', type='http', auth='public')
    def products_id(self,id):
        data = request.env['product.product'].sudo().search_read([('id','=',id)])
        return json.dumps(data, default=date_utils.json_default)

class ImageUrl(http.Controller):

    def image(self, model, id, field_name, **kw):
        url = f'/web/content/{model}/{id}/{field_name}'
        return url

class Image(ImageUrl):
    @http.route(['/imageurl'], type='http', auth="public")
    def products_image(self):
        model='product.product'
        res = request.env[model].sudo().search_read({})
        # res1 = request.env[model].sudo().search_read([('id','=',id)])
        data = []
        if model =='res.company':
            field_name='logo'
            for record in res:
                id = record.get('id')
                if record[field_name]:
                    record[field_name] = super().image(model, id, field_name)
                data.append(record)
        else:
            field_name=['image_1920','image_1024','image_512','image_256','image_128']
            for record in res:
                id=record.get('id')
                for i in field_name:
                    if record[i]:
                         record[i] = super().image(model,id,i)
                data.append(record)
        return json.dumps(data, default=date_utils.json_default)

