from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError

class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'HMS Patient'

    first_name = fields.Char(string="First Name", required=True)

    last_name = fields.Char(string="Last Name", required=True)

    birth_date = fields.Date(string="Birth Date")

    history = fields.Html()

    email = fields.Char(string="Email")

    pcr = fields.Boolean()

    image = fields.Image()

    address = fields.Text(string="Address")

    cr_ratio = fields.Float(string="CR Ratio")

    blood_type = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
    ])

    age = fields.Integer(
        compute="_compute_age",
        store=True
    )

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], default='undetermined')

    department_capacity = fields.Integer(
        related='department_id.capacity'
    )


 department_id = fields.Many2one(
        'hms.department',
        domain="[('is_opened', '=', True)]"
    )

    doctor_ids = fields.Many2many(
        'hms.doctor'
    )

    log_ids = fields.One2many(
        'hms.patient.log',
        'patient_id'
    )

    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                today = fields.Date.context_today(patient)
                patient.age = today.year - patient.birth_date.year - (
                    (today.month, today.day) < (patient.birth_date.month, patient.birth_date.day)
                )
            else:
                patient.age = 0

    @api.constrains('email')
    def _check_email(self):
        for patient in self:
            if patient.email:
                if not tools.email_validate(patient.email):
                    raise ValidationError('Please enter a valid email address.')
                # Check uniqueness
                existing = self.env['hms.patient'].search([
                    ('email', '=', patient.email),
                    ('id', '!=', patient.id),
                ])
                if existing:
                    raise ValidationError('This email address already exists in another patient record.')

    @api.constrains('pcr', 'cr_ratio')
    def check_cr_ratio(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError(
                    "CR Ratio is required when PCR is checked"
                )

    @api.onchange('age')
    def onchange_age(self):
        if self.age < 30:
            self.pcr = True

            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'PCR checked automatically because age is below 30'
                }
            }

    def write(self, vals):

        if 'state' in vals:
            for rec in self:

                self.env['hms.patient.log'].create({
                    'patient_id': rec.id,
                    'description': f"State changed to {vals['state']}"
                })

        return super().write(vals)