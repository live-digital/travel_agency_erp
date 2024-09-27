from odoo import models, fields

class City(models.Model):
    _name = 'travel.city'
    _description = 'City Management'
    _inherit = ['mail.thread']

    name = fields.Char(string='City Name', required=True)
