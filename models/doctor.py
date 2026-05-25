from odoo import models, fields


class HmsDoctor(models.Model):
    _name = 'hms.doctor'
    _description = 'HMS Doctor'

    first_name = fields.Char(string="First Name", required=True)

    last_name = fields.Char(string="Last Name", required=True)

    image = fields.Image()

    department_id = fields.Many2one(
        'hms.department',
        string="Department"
    )

    patient_ids = fields.Many2many(
        'hms.patient',
        string="Patients"
    )

    full_name = fields.Char(
        compute="_compute_full_name"
    )

    def _compute_full_name(self):
        for rec in self:
            rec.full_name = f"{rec.first_name} {rec.last_name}"