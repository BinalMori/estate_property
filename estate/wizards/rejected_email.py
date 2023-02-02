from odoo import models, fields, api,_

class RejectedEmail(models.TransientModel):

    _name = 'rejected.email'


    # Reason=fields.Selection([('not intrested','not intrested'),('offer price is high','offer price is high'),('other','other')],default='not intrested')
    Reason=fields.Char(string='reson',required=True)

    def rejected_email(self):
        # self.env['account.move'].write({'reason': self.Reason})
        active_id = self._context.get('active_id')
        self.env['account.move'].browse(active_id).write({'reason': self.Reason})

        self.ensure_one()
        default_template = self.env.ref('estate.rejected_mail_template_demo')
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='account.move',
            default_res_id=self.id,
            default_use_template=bool(default_template),
            default_template_id=default_template and default_template.id,
            default_composition_mode='comment',
            custom_layout='mail.mail_notification_light',
            force_email=True,
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }


