from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BusMaster(models.Model):
    _name = 'bus.master'
    _description = 'Bus Details'
    _inherit = ['mail.thread']
    _rec_name = 'name'

    name = fields.Char(string='Bus', required=True)
    number = fields.Char(string='Bus Number', required=True)
    chassis_no = fields.Char(string='Chassis No')
    type = fields.Selection([('ac', 'AC'), ('non_ac', 'Non-AC')], string='Bus Type')
    seating_capacity = fields.Integer(string='Seating Capacity', required=True)

    def custom_save(self):
        for record in self:
            if not record.name or not record.number or not record.seating_capacity:
                raise ValidationError('All fields are required.')

        record.write({
            'name': record.name,
            'number': record.number,
            'chassis_no': record.chassis_no,
            'type': record.type,
            'seating_capacity': record.seating_capacity,
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Bus Master',
            'res_model': 'bus.master',
            'view_mode': 'tree,form',
            'target': 'current'
        }
