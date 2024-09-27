from odoo import models, fields

class Customer(models.Model):
    _name = 'travel.customer'
    _description = 'Customer Information'

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='Phone Number')
    email = fields.Char(string='Email Address')
