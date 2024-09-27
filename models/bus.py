from odoo import fields, models #imported all 2 from odoo

class Bus(models.Model): #here we defined a class inside models
    _name = 'travel.bus'  #a database table is created for storing employees travel details
    _description = 'Bus Information'

    name = fields.Char(string='Bus Name', required=True)
    number_plate = fields.Char(string='Number Plate')
    bus_type = fields.Selection([('ac', 'AC'), ('non_ac', 'Non AC')], string='Bus Type')
    seating_capacity = fields.Integer(string='Seating Capacity', required=True)