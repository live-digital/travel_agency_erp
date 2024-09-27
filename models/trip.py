
from odoo import models, fields, api ,_
from odoo.odoo import exceptions



class Trip(models.Model):
    _name = 'travel.trip'
    _description = 'Trip Management'
    _inherit = ['mail.thread']


    name = fields.Char(string='Trip Name', required=True, default='New Trip', readonly=True, copy=False, index=True)
    from_city_id = fields.Many2one('travel.city', string='From City')
    to_city_id = fields.Many2one('travel.city', string='To City')
    datetime = fields.Datetime(string='Date and Time')
    bus_id = fields.Many2one('travel.bus', string='Bus')
    driver_id = fields.Many2one('travel.driver', string='Driver')
    payment_amount = fields.Float(string='Payment Amount', default=0.0)
    passenger_capacity = fields.Integer(string='Passenger Capacity', compute='_compute_passenger_capacity', store=True)
    ticket_ids = fields.One2many('travel.ticket', 'trip_id', string='Tickets')

    # @api.model
    # def create(self, vals):
    #     if vals.get('name', 'New Trip') == 'New Trip':
    #         vals['name'] = self.env['ir.sequence'].next_by_code('travel.trip') or 'New Trip'
    #     return super(Trip, self).create(vals)



    @api.model
    def create(self, vals):
        # Generate the sequence number
     #   sequence = self.env['ir.sequence'].next_by_code('travel.trip') or 'New Trip'
        bus_name = self.env['travel.bus'].browse(vals['bus_id']).name if 'bus_id' in vals else 'N/A'
        departure_time = vals.get('datetime', '')
        formatted_name = f"{bus_name}/{departure_time}"
        vals['name'] = formatted_name
        trip = super(Trip, self).create(vals)
        return trip

    def write(self, vals):
        for trip in self:
            trip.message_post(body="Trip updated: Changes made.")
        # Call the original write method
        result = super(Trip, self).write(vals)
        # Recompute the name if bus or datetime is changed
        if 'bus_id' in vals or 'datetime' in vals:
            for trip in self:
                bus_name = trip.bus_id.name if trip.bus_id else 'N/A'
                departure_time = trip.datetime.strftime('%Y-%m-%d %H:%M:%S') if trip.datetime else 'No Time'
                trip.name = f"{trip.name.split(' ')[0]} {bus_name} - {departure_time}"

        return result


    @api.depends('bus_id')
    def _compute_passenger_capacity(self):
        for trip in self:
            if trip.bus_id:
                trip.passenger_capacity = trip.bus_id.seating_capacity
            else:
                trip.passenger_capacity = 0

    @api.constrains('bus_id', 'datetime')
    def _check_bus_availability(self):
        for trip in self:
            # Check if there is another trip with the same bus and departure time
            existing_trip = self.search([
                ('bus_id', '=', trip.bus_id.id),
                ('datetime', '=', trip.datetime),
                ('id', '!=', trip.id)  # Exclude the current trip from the search
            ], limit=1)
            if existing_trip:
                raise exceptions.ValidationError(
                    _('The bus %s is already booked for the departure time %s. Please choose a different time or bus.') % (
                    trip.bus_id.name, trip.datetime)
                )
