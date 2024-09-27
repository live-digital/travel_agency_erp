from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CityMaster(models.Model):
    _name = 'city.master'
    _description = 'City Details'
    _inherit = ['mail.thread']

    name = fields.Char(string='City Name', required=True)

    def custom_save(self):
        if not self.name:
            raise ValidationError("City name is required")

        self.write({
            'name': self.name,
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'City Master',
            'res_model': 'city.master',
            'view_mode': 'tree,form',
            'target': 'current'
        }
