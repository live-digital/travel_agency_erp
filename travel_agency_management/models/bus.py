from odoo import models, fields


class Bus(models.Model):
    _name = 'travel.bus'
    _description = 'Bus Management'
    _inherit = ['mail.thread']

    name = fields.Char(string='Bus Name', required=True, track_visibility='onchange')
    number_plate = fields.Char(string='Number Plate', track_visibility='onchange')
    chassis_no = fields.Char(string='Chassis Number')
    bus_type = fields.Selection([('ac', 'AC'), ('non_ac', 'Non-AC')], string='Bus Type')
    seating_capacity = fields.Integer(string='Seating Capacity')

