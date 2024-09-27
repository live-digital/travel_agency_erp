from odoo import models, fields, api

from odoo.exceptions import ValidationError


class Trip(models.Model):
    _name = 'travel.trip'
    _inherit = ['mail.thread']
    _description = 'Trip Details'

    trip_id = fields.Char('Trip ID', readonly=True, copy=False)
    name = fields.Char(String="Trip Name", store=True)
    from_city = fields.Many2one('city.master', 'From City', required=True)
    to_city = fields.Many2one('city.master', 'To City', required=True, domain="[('id','!=',from_city)]")
    departure_time = fields.Datetime('Departure Date & Time', required=True)
    bus_id = fields.Many2one('bus.master', 'Bus', required=True)
    driver_id = fields.Many2one('driver.master', 'Driver', required=True)
    passenger_capacity = fields.Integer('Passenger Capacity', required=True)
    ticket_price = fields.Float('Ticket Price', required=True, digits=(10, 2))
    ticket_ids = fields.One2many('travel.ticket', 'trip_id', 'Tickets')

    @api.model
    def create(self, vals):
        # Generate the sequence number
        sequence = self.env['ir.sequence'].next_by_code('travel.trip') or 'New Trip'

        # Fetch the city names and departure time (only if provided in vals)
        from_city = self.env['city.master'].browse(vals['from_city']).name if 'from_city' in vals else 'Unknown'
        to_city = self.env['city.master'].browse(vals['to_city']).name if 'to_city' in vals else 'Unknown'
        departure_time = vals.get('departure_time', '')

        # Format the custom name as sequence + fromcity -> tocity, departure_time
        formatted_name = f"{from_city} -> {to_city}, {departure_time}"

        if not vals.get('trip_id'):
            vals['trip_id'] = self.env['ir.sequence'].next_by_code('travel.trip')

        # Set the generated name in vals
        vals['name'] = formatted_name

        # Create the trip record
        trip = super(Trip, self).create(vals)

        # Post a log note after creation
        trip.message_post(body="Trip created: {} -> {}, Departure: {}".format(
            from_city, to_city, departure_time))

        return trip

    @api.constrains('from_city', 'to_city')
    def _check_cities(self):
        for record in self:
            if record.from_city == record.to_city:
                raise ValidationError("The departure city and destination city cannot be the same.")

    # def write(self, vals):
    #     # Log a note before updating the record
    #     for trip in self:
    #         trip.message_post(body="Trip updated: Changes made.")
    #
    #     result = super(Trip, self).write(vals)
    #
    #     # Recompute the name if cities or departure time is changed
    #     if 'from_city' in vals or 'to_city' in vals or 'departure_time' in vals:
    #         for trip in self:
    #             from_city = trip.from_city.name
    #             to_city = trip.to_city.name
    #             departure_time = trip.departure_time
    #             trip.name = f" -> {to_city}, {departure_time}"
    #
    #     return result

    @api.onchange('bus_id')
    def _onchange_bus_id(self):
        if self.bus_id:
            bus = self.bus_id
            if bus.seating_capacity:
                self.passenger_capacity = bus.seating_capacity
            else:
                self.passenger_capacity = 0  # Default value if seating_capacity is not set
        else:
            self.passenger_capacity = 0  # Default value if no bus is selected
