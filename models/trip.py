from odoo import models, fields

class TravelTrip(models.Model):
    _name = 'travel.trip'
    _description = 'Trip Management'

    bus_id = fields.Many2one('travel.bus', string="Bus", required=True)
    from_city = fields.Char(string="From City", required=True)
    to_city = fields.Char(string="To City", required=True)
    departure_time = fields.Datetime(string="Departure Time", required=True)
    arrival_time = fields.Datetime(string="Arrival Time")
    ticket_ids = fields.One2many('travel.ticket', 'trip_id', string="Tickets")
