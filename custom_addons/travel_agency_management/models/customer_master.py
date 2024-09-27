from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CustomerMaster(models.Model):
    _name = 'customer.master'
    _description = 'Customer Details'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Customer', required=True, track_visibility="onchange")
    phone_no = fields.Char(string='Phone', required=True, track_visibility="onchange")
    email = fields.Char(string='Email', required=True, track_visibility="onchange")
    age = fields.Integer(string='Age', required=True)
    gender = fields.Selection([('male', "Male"), ('female', 'Female'), ('other', 'Other')], string='Gender',
                              required=True)

    def custom_save(self):
        for record in self:
            if not record.name or not record.phone_no or not record.email:
                raise ValidationError("All fields are required.")

        record.write({
            'name': record.name,
            'phone_no': record.phone_no,
            'email': record.email,
            'age': record.age,
            'gender': record.gender,
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Master',
            'res_model': 'customer.master',
            'view_mode': 'tree,form',
            'target': 'current'
        }
