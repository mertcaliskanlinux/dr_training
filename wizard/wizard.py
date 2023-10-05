from odoo import models, fields, api


class AppointmentWizard(models.TransientModel):
    _name = 'dr_patients.appointment.wizard'
    _description = 'Create Appointment Wizard'

    patient = fields.Many2one('dr_patients.patient', string='Patient', required=True)
    doctor_id = fields.Many2many('dr_patients.doctor', string='Doctors')
    code = fields.Char(string='Code', required=True)
    appointment_date_time = fields.Datetime(string="Appointment Date & Time", required=True)  # Eklenen satır



    def create_appointment(self):
        appointment_vals = {
            'patient': self.patient.id,
            'doctor_id': [(6, 0, self.doctor_id.ids)],
            'code': self.code,
            'stage': 'draft',
            'appointment_date_time': self.appointment_date_time,  # Eklenen satır
            # Other necessary fields...
        }
        self.env['dr_patients.appointment'].create(appointment_vals)
