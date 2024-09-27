from odoo import models, fields

class TravelDriver(models.Model):
    _name = 'travel.driver'
    _description = 'Driver Information'

    name = fields.Char(string="Name", required=True)
    phone_no = fields.Char(string="Phone Number", required=True)
    aadhar_no = fields.Char(string="Aadhar Number", required=True)
    pan_no = fields.Char(string="PAN Number", required=True)
    aadhar_attachment = fields.Binary(string="Aadhar Attachment")
