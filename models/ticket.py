from odoo import models, fields, api

class TravelTicket(models.Model):
    _name = 'travel.ticket'
    _description = 'Ticket'

    trip_id = fields.Many2one('travel.trip', string="Trip", required=True)
    bus_name = fields.Char(string="Bus Name", related='trip_id.bus_id.name', store=True, readonly=True)
    departure_time = fields.Datetime(string="Departure Time", related='trip_id.departure_time', store=True,
                                     readonly=True)
    payment_amount = fields.Float(string="Payment Amount", compute="_compute_payment_amount")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ], default='draft', string="Status")

    @api.depends('trip_id')
    def _compute_payment_amount(self):
        for record in self:
            record.payment_amount = 100.00  # Example, you can customize as per logic

