from odoo import http
import io
from odoo.http import request, route
import tempfile
import json
from json import JSONEncoder
from odoo.tools import date_utils

class ImageUrl(http.Controller):

    def image(self, model, id, field_name, **kw):
        url = f'/web/content/{model}/{id}/{field_name}'
        return url

class Image(ImageUrl):
    @http.route(['/imageurl','/imageurl/<int:id>'], type='http', auth="public")
    def products_image(self,id):
        model='product.product'
        res = request.env[model].sudo().search_read([('id','=',id)])
        data = []
        field_name=['image_1920','image_1024','image_512','image_256','image_128']
        for record in res:
            id=record.get('id')
            for i in field_name:
                if record[i]:
                     record[i] = super().image(model,id,i)
            data.append(record)
        return json.dumps(data, default=date_utils.json_default)

        # def get_image_url(self):
        #     web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        #
        #     for record in web_base_url:
        #         image_1920 = f'{web_base_url}/web/image/{self._name}/{record.id}/{record.image}'
        #     return image_1920


# from odoo.addons.website_sale.controllers.main import WebsiteSale