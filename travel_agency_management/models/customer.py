from odoo import models, fields

class Customer(models.Model):
    _name = 'travel.customer'
    _description = 'Customer Management'
    _inherit = ['mail.thread']
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')

    name = fields.Char(string='Name', required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    age = fields.Integer(string='Age')

