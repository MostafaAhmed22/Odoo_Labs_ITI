from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string='Related Patient')

    @api.constrains('related_patient_id', 'email')
    def _check_customer_email(self):
        for partner in self.filtered('related_patient_id'):
            if partner.email:
                existing_patient = self.env['hms.patient'].search([('email', '=', partner.email)], limit=1)
                if existing_patient:
                    raise ValidationError(
                        'A customer cannot be linked if its email already exists in a patient record.'
                    )

    def unlink(self):
        linked_customers = self.filtered('related_patient_id')
        if linked_customers:
            raise ValidationError('You cannot delete a customer linked to a patient.')
        return super().unlink()