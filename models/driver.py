from odoo import models, fields

class Driver(models.Model):
    _name = 'travel.driver'
    _description = 'Driver Management'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', required=True)
    phone_no = fields.Char(string='Phone Number')
    aadhar_no = fields.Char(string='Aadhar Number')
    pan_no = fields.Char(string='PAN Number')
    aadhar_attachment = fields.Binary(string='Aadhar Attachment')
