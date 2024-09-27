from odoo import models, fields

class Driver(models.Model):
    _name = 'travel.driver'
    _description = 'Driver Information'

    name = fields.Char(string='Name', required=True)
    phone_no = fields.Char(string='Phone Number')
    adhar_no = fields.Char(string='Aadhar Number')
    pan_no = fields.Char(string='PAN Number')
    adhar_attachment = fields.Binary(string='Aadhar Attachment')
    bus_id = fields.Many2one('travel.bus', string='Assigned Bus')
