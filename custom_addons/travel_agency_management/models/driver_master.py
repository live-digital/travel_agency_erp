from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DriverMaster(models.Model):
    _name = 'driver.master'
    _description = 'Driver Details'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Driver', required=True, track_visibility="onchange")
    phone_no = fields.Char(string='Phone', required=True)
    aadhar_no = fields.Char(string='Aadhar No', required=True)
    pan_no = fields.Char(string='PAN No')
    aadhar_attachment = fields.Binary(string='Aadhar Attachment')

    def custom_save(self):
        for record in self:
            if not record.name or not record.phone_no or not record.aadhar_no:
                raise ValidationError("All fields are required.")

        record.write({
            'name': record.name,
            'phone_no': record.phone_no,
            'aadhar_no': record.aadhar_no,
            'pan_no': record.pan_no,
            'aadhar_attachment': record.aadhar_attachment
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Driver Master',
            'res_model': 'driver.master',
            'view_mode': 'tree,form',
            'target': 'current'
        }
