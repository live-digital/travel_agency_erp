from odoo import models, fields

class TransportCity(models.Model):
    _name = 'transport.city'
    _description = 'Transport City'

    name = fields.Char(string="City Name", required=True)
