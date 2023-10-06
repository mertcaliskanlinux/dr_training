from odoo import models, fields

class SaleOrder(models.Model):

    _name = 'sale.order'
    _inherit = 'sale.order'

    doctor_fee = fields.Many2one('product.product', string='Doctor Fee', domain=[('type', '=', 'service')])
    medicines = fields.Many2one('product.product', string='Medicines', domain=[('type', '=', 'consu')])
    room_ward_charges = fields.Many2one('product.product', string='Room/Ward Charges', domain=[('type', '=', 'service')])
    injections = fields.Many2one('product.product', string='Injections', domain=[('type', '=', 'consu')])
    drips = fields.Many2one('product.product', string='Drips', domain=[('type', '=', 'consu')])
