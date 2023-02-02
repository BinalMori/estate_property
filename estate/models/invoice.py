from odoo import fields,models,_
from odoo.exceptions import UserError

class Invoice(models.Model):
    _inherit = "account.move"

    reason=fields.Char(string="reason", readonly=True)
    state=fields.Selection(selection_add=[('submit','submit'),('rejected','rejected'),('approved','approved')], ondelete={'approved': 'set default', 'rejected':'set default','submit':'set default'})


    def approved(self):
        for record in self:
            record.state='approved'

        self.ensure_one()
        default_template = self.env.ref('estate.approved_mail_template_demo')
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


    def reject(self):
        for record in self:
                record.state='rejected'
        return {
            'name': 'rejected email wizard',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            "view_type": "form",
            'res_model': 'rejected.email',
            'target': 'new',
            'view_id': self.env.ref
            ('estate.rejected_email_wizard_view_form').id,
            'context': {'active_id': self.id,}
        }

    def submit(self):
        for record in self:
            record.state = 'submit'
        self.ensure_one()
        default_template = self.env.ref('estate.submit_mail_template')
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

