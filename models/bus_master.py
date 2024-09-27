from odoo import models, fields

class TravelBus(models.Model):
    _name = 'travel.bus'
    _description = 'Bus Information'

    name = fields.Char(string="Bus Name", required=True)
    number_plate = fields.Char(string="Number Plate", required=True)
    chassis_no = fields.Char(string="Chessis Number")
    bus_type = fields.Selection([('ac', 'AC'), ('non_ac', 'Non-AC')], string="Bus Type")
    seating_capacity = fields.Integer(string="Seating Capacity", required=True)