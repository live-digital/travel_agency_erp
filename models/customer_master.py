from odoo import models, fields

class TravelCustomer(models.Model):
    _name = 'travel.customer'
    _description = 'Customer Information'

    name = fields.Char(string="Customer Name", required=True)
    phone = fields.Char(string="Phone Number", required=True)
    email = fields.Char(string="Email")
    age = fields.Selection([('male', 'Male'), ('female', 'Female'),('lgbtq', 'LGBTQ')], required=True)
    gender = fields.Char(string="Gender", required=True)
