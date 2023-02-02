from odoo import http
from odoo import fields,models,api

class Navbar_login(models.Model):


    _name="navbar.login"


    username=fields.Char(string='name')
    password=fields.Char(string='password',widget='password')

    def login(self):
        user = self.env['res.users'].authenticate(self.env.cr.dbname, self.username, self.password, None)
        http.request.session.uid=user
        # self.env.user = user
        action = {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        return action

        # try:
        #     uid=self.env.user.sudo().authenticate(self.username, self.password, None)
        #     action = self.env.ref('base.action_res_users').read()[0]
        #     action['res_id'] = uid
        #     return action
        # except Exception:
        #     raise UserError("Invalid login. Please try again.")
#
# self.env.user = user
#         action = {
#             'type': 'ir.actions.client',
#             'tag': 'reload',
#         }

# self.env.cr.commit()


    # def login(self):
    #     self.env['base.automation']._call_on_workers(self.env.cr.dbname, self.env.user.id, 'session', 'logout')
    #     new_user = self.env['res.users'].authenticate(self.env.cr.dbname, self.username.login, self.password.password,None)
    #     if new_user:
    #         self.env.user = new_user
    #
    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'reload'
    #     }