from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Patient(models.Model):
    _name = "dr_patients.patient"
    _description = "Patient"
    _rec_name = "full_name"

    patient_id = fields.Char(
        string="Patient ID",
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('dr_patients.patient')
    )
    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    full_name = fields.Char(string="Full Name",store=True, compute="_onchange_full_name")
    date_of_birth = fields.Date(string="Date of Birth", required=True)
    age = fields.Integer(string="Age", readonly=True, compute="_compute_age")
    address = fields.Text(string="Address", required=True)
    phone = fields.Char(string="Phone", required=True)
    email = fields.Char(string="Email", required=True)
    national_id_no = fields.Char(string="National ID No.", required=True, unique=True)

    @api.depends('first_name', 'last_name')
    def _onchange_full_name(self):
        for rec in self:
            if rec.first_name and rec.last_name:
                rec.full_name = rec.first_name + ' ' + rec.last_name  # eğer isim ve soyisim dolu ise full_name alanını doldur
            else:
                rec.full_name = ""  # eğer isim ve soyisim boş ise full_name alanını boş bırak


    @api.constrains('national_id_no')
    def _check_unique_national_id_no(self):
        for record in self:
            if record.national_id_no:
                existing_patient = self.env['dr_patients.patient'].search([
                    ('national_id_no', '=', record.national_id_no),
                    ('id', '!=', record.id),
                ])
                if existing_patient:
                    raise ValidationError("National ID No. must be unique.")

    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = fields.Date.today()
                birth_date = fields.Date.from_string(record.date_of_birth)
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                record.age = age
            else:
                record.age = 0



