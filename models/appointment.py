from odoo import models, fields, api, exceptions

class Appointment(models.Model):
    _name = "dr_patients.appointment"

    _rec_name = "doctor_full_name"
    _rec_patient = "patient_full_name"
    _rec_treatment = "treatment_name"
    _description = "Appointment"

    appointment_date_time = fields.Datetime(string="Appointment Date & Time", required=True)
    code = fields.Char(string='code', required=True, index=True, copy=False, default=lambda self: self.env['ir.sequence'].next_by_code('dr_patients.appointment') or 'New')
    doctor_id = fields.Many2many(comodel_name="dr_patients.doctor", string="Doctor")
    patient = fields.Many2one(comodel_name="dr_patients.patient", string="Patient", required=True)
    stage = fields.Selection(
        string="Stage",
        selection=[('draft', 'Draft'),('in_progress', 'In Progress'), ('done', 'Done'),
                   ('cancel', 'Cancel')],
        default='draft',
        required=True
    )
    treatment = fields.One2many('dr_patients.treatment', 'appointment', string='Treatments')
    patient_full_name = fields.Char(string="Patient Name", compute="_compute_patient_full_name", store=True)
    doctor_full_name = fields.Char(string="Doctor Name", compute="_compute_doctor_full_name", store=True)
    is_readonly = fields.Boolean(string="Is Readonly", compute="_compute_is_readonly")

    @api.depends('patient')
    def _compute_treatment(self):
        for appointment in self:
            if appointment.patient:
                appointment.treatment = appointment.patient.treatment
            else:
                appointment.treatment = False

    @api.depends('patient')
    def _compute_patient_full_name(self):
        for appointment in self:
            if appointment.patient:
                appointment.patient_full_name = appointment.patient.full_name
            else:
                appointment.patient_full_name = ""

    @api.depends('doctor_id')
    def _compute_doctor_full_name(self):
        for appointment in self:
            if appointment.doctor_id:
                appointment.doctor_full_name = ', '.join(appointment.doctor_id.mapped('full_name'))
            else:
                appointment.doctor_full_name = ""

    @api.depends('patient')
    def _compute_treatment(self):
        for appointment in self:
            if appointment.patient:
                appointment.treatment = appointment.patient.treatment
            else:
                appointment.treatment = False

    def action_confirm(self):
        print("BUTTON PROGRESS")
        self.stage = 'in_progress'

    def action_done(self):
        print("BUTTON DONE")
        self.stage = 'done'
        context = dict(self.env.context, readonly_doctor=True)  # "Done" düğmesine tıklanınca "doctor" alanı readonly yapılır
        self = self.with_context(context)  # Context'i güncelleyin

    def action_draft(self):
        print("BUTTON DRAFT")
        self.stage = 'draft'
        context = dict(self.env.context, readonly_doctor=False)  # Özel bir context oluşturun
        self.with_context(context)  # Context'i güncelleyin


    def action_cancel(self):
        print("BUTTON CANCEL")
        self.stage = 'cancel'

    def unlink(self):
        if self.stage == 'done':
            raise exceptions.ValidationError("You cannot delete a done appointment")
        return super(Appointment, self).unlink()
    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('dr_patients.appointment') or 'New'
        return super(Appointment, self).create(vals)

    @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            if self.env['dr_patients.appointment'].search_count([('code', '=', record.code)]) > 1:
                raise exceptions.ValidationError('The Code must be unique.')






