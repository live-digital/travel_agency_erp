from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TravelTrip(models.Model):
    _name = 'travel.trip'
    _description = 'Trip Information'
    _inherit = ['mail.thread']

    name = fields.Char(string="Trip Name", store=True)
    from_city_id = fields.Many2one('travel.city', string="From City", required=True)
    to_city_id = fields.Many2one('travel.city', string="To City", required=True, domain="[('id', '!=', from_city_id)]")
    departure_time = fields.Datetime(string="Departure Time", required=True)
    bus_id = fields.Many2one('travel.bus', string="Bus", required=True)
    driver_id = fields.Many2one('travel.driver', string="Driver", required=True)
    passenger_capacity = fields.Integer(string="Passenger Capacity", readonly=True, compute="_compute_available_seat")
    payment_amount = fields.Float(string="Payment Amount", required=True)
    ticket_ids = fields.One2many('travel.ticket', 'trip_id', string='Tickets')

    @api.depends('bus_id')
    def _compute_available_seat(self):
        for record in self:
            if record.bus_id:
                record.passenger_capacity = record.bus_id.seating_capacity
            else:
                record.passenger_capacity = 0

    @api.constrains('from_city_id', 'to_city_id')
    def _check_cities(self):
        for record in self:
            if record.from_city_id == record.to_city_id:
                raise ValidationError("The departure city and destination city cannot be the same.")

    # @api.depends('from_city_id', 'to_city_id', 'departure_time')
    # def _compute_trip_name(self):
    #     for record in self:
    #         if record.from_city_id and record.to_city_id and record.departure_time:
    #             departure_str = fields.Datetime.to_string(record.departure_time)
    #             record.name = f"{record.from_city_id.name} -> {record.to_city_id.name}, {departure_str}"
    #         else:
    #             record.name = "New Trip"

    @api.model
    def create(self, vals):
        # Generate the sequence number
        # sequence = self.env['ir.sequence'].next_by_code('travel.trip') or 'New Trip'

        # Fetch the city names and departure time (only if provided in vals)
        from_city = self.env['travel.city'].browse(vals['from_city_id']).name if 'from_city_id' in vals else 'Unknown'
        to_city = self.env['travel.city'].browse(vals['to_city_id']).name if 'to_city_id' in vals else 'Unknown'
        # Convert departure time to user's time zone
        departure_time = vals.get('departure_time', False)
        if departure_time:
            departure_time = fields.Datetime.from_string(departure_time)
            departure_time_local = fields.Datetime.context_timestamp(self, departure_time)
            departure_time_str = fields.Datetime.to_string(departure_time_local)
        else:
            departure_time_str = 'No departure time'

        # Format the custom name as sequence + fromcity -> tocity, departure_time
        formatted_name = f"{from_city} -> {to_city}, {departure_time_str}"

        # Set the generated name in vals
        vals['name'] = ""
        vals['name'] = formatted_name

        # Create the trip record
        trip = super(TravelTrip, self).create(vals)

        # Post a log note after creation
        trip.message_post(body="Trip created: {} -> {}, Departure: {}".format(
            from_city, to_city, departure_time))

        return trip

    def write(self, vals):
        # Log a note before updating the record
        for trip in self:
            trip.message_post(body="Trip updated: Changes made.")

        result = super(TravelTrip, self).write(vals)

        # Recompute the name if cities or departure time is changed
        if 'from_city_id' in vals or 'to_city_id' in vals or 'departure_time' in vals:
            for trip in self:
                from_city = trip.from_city_id.name
                to_city = trip.to_city_id.name
                departure_time = trip.departure_time
                trip.name = f"{trip.name.split(' ')[0]} {from_city} -> {to_city}, {departure_time}"

        return result



