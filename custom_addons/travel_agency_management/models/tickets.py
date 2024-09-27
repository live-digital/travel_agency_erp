from odoo import models, fields, api
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError


class Ticket(models.Model):
    _name = 'travel.ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Ticket Details'
    _rec_name = 'ticket_number'

    TICKET_STATE = [
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    ticket_number = fields.Char(string='Ticket Number', readonly=True, copy=False)
    from_city = fields.Many2one('city.master', string="From City", required=True,
                                default=lambda self: self.env['city.master'].search([('name', '=', 'Bhubaneswar')],
                                                                                    limit=1))
    to_city = fields.Many2one('city.master', 'To City', required=True, domain="[('id','!=',from_city)]")
    customer_id = fields.Many2one('customer.master', 'Customer', required=True, track_visibility="onchange")
    bus_id = fields.Many2one('bus.master', 'Bus', required=True)
    boarding_time = fields.Datetime('Boarding Time')
    departure_time = fields.Datetime('Departure Time', required=True)
    payment_amount = fields.Float('Payment Amount', required=True, track_visibility="onchange")
    trip_id = fields.Many2one('travel.trip', 'Trip', required=True, domain="[('departure_time', '>', datetime.now())]",
                              track_visibility="onchange")
    available_seats = fields.Integer(string="Available Seats", compute="_compute_available_seats", store=True)
    state = fields.Selection(TICKET_STATE, string='Status', readonly=True, default='draft', track_visibility="onchange")

    @api.model
    def get_future_trips(self):
        current_time = datetime.now()
        return self.env['travel.trip'].search([('departure_time', '>', current_time)])

    @api.onchange('from_city', 'to_city')
    def _onchange_trip_domain(self):
        if self.from_city and self.to_city:
            return {
                'domain': {
                    'trip_id': [
                        ('from_city', '=', self.from_city.id),
                        ('to_city', '=', self.to_city.id),
                        ('departure_time', '>', fields.Datetime.now())
                    ]
                }
            }
        else:
            return {
                'domain': {
                    'trip_id': []
                }
            }

    # @api.onchange('from_city', 'to_city')
    # def _onchange_city(self):
    #     if self.from_city and self.to_city:
    #         # Get the current time
    #         now = datetime.now()
    #
    #         # Apply the filter to future trips where the departure time is greater than the current time
    #         return {
    #             'domain': {
    #                 'trip_id': [
    #                     ('from_city', '=', self.from_city.id),
    #                     ('to_city', '=', self.to_city.id),
    #                     ('datetime', '>', now)  # Ensure only future trips are displayed
    #                 ]
    #             }
    #         }

    @api.depends('trip_id')
    def _compute_available_seats(self):
        """ Compute available seats based on booked tickets and bus capacity. """
        for record in self:
            if record.trip_id:
                booked_tickets = self.env['travel.ticket'].search_count([('trip_id', '=', record.trip_id.id)])
                record.available_seats = record.bus_id.seating_capacity - booked_tickets

    @api.constrains('from_city', 'to_city')
    def _check_cities(self):
        for record in self:
            if record.from_city == record.to_city:
                raise ValidationError("The departure city and destination city cannot be the same.")

    # Set default value for 'from_city' using the default_get method
    # @api.model
    # def default_get(self, fields_list):
    #     res = super(Ticket, self).default_get(fields_list)
    #     # Search for the city with the name 'Bhubaneswar'
    #     city_id = self.env['city.master'].search([('name', '=', 'Bhubaneswar')], limit=1)
    #     if city_id:
    #         res['from_city'] = city_id.id
    #     return res

    # Onchange method for 'trip_id'
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Check if trip_id is in vals and assign the corresponding bus_id from the trip
            if 'trip_id' in vals:
                trip = self.env['travel.trip'].browse(vals['trip_id'])
                vals['bus_id'] = trip.bus_id.id if trip.bus_id else False

            # Generate ticket number if not provided
            if not vals.get('ticket_number'):
                vals['ticket_number'] = self.env['ir.sequence'].next_by_code('travel.ticket')

        # Create the record using the superclass method
        return super(Ticket, self).create(vals_list)

    @api.onchange('trip_id')
    def _onchange_trip_id(self):
        if self.trip_id:
            trip = self.trip_id
            # Make sure that the bus_id is assigned to the actual Bus record, not the name.
            self.bus_id = trip.bus_id or False
            self.departure_time = trip.departure_time
            self.payment_amount = trip.ticket_price
            self.boarding_time = trip.departure_time - timedelta(minutes=15) if trip.departure_time else False

    def action_print_ticket(self):
        return self.env.ref('travel_agency_management.ticket_report_action').report_action(self)

    # Action methods for state change
    def action_confirm(self):
        if self.state == 'draft':
            self.write({'state': 'confirmed'})

    def action_cancel(self):
        if self.state == 'confirmed':
            self.write({'state': 'cancelled'})

    def action_draft(self):
        if self.state == 'cancelled':
            self.write({'state': 'draft'})
