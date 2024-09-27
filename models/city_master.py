from odoo import models, fields

class TravelCity(models.Model):
    _name = 'travel.city'
    _description = 'City Information'

    name = fields.Char(string="City Name", required=True)
