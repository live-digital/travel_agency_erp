from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta, datetime
import logging

_logger = logging.getLogger(__name__)


class TravelTicket(models.Model):
    _name = 'travel.ticket'
    _description = 'Ticket Information'
    TICKET_STATE = [
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    from_city_id = fields.Many2one('travel.city', string="From City", required=True,
                                   default=lambda self: self.env['travel.city'].search([('name', '=', 'Bhubaneswar')],
                                                                                       limit=1))
    to_city_id = fields.Many2one('travel.city', string="To City", required=True,  domain="[('id', '!=', from_city_id)]")
    customer_id = fields.Many2one('travel.customer', string="Customer", required=True)
    trip_id = fields.Many2one('travel.trip', string="Trip", required=True,
                              domain="[('departure_time', '>', datetime.now())]")
    bus_id = fields.Many2one('travel.bus', string="Bus", required=True)  # Bus is set from trip
    available_seats = fields.Integer(string="Available Seats", compute="_compute_available_seats", store=True)
    payment_amount = fields.Float(string="Payment Amount", required=True)
    boarding_time = fields.Datetime(string="Boarding Time", required=True)
    departure_time = fields.Datetime(string="Departure Time")
    state = fields.Selection(TICKET_STATE, string='Status', readonly=True, default='draft')

    @api.model
    def get_future_trips(self):
        current_time = datetime.now()
        return self.env['travel.trip'].search([('departure_time', '>', current_time)])

    @api.onchange('from_city_id', 'to_city_id')
    def _onchange_trip_domain(self):
        if self.from_city_id and self.to_city_id:
            return {
                'domain': {
                    'trip_id': [
                        ('from_city_id', '=', self.from_city_id.id),
                        ('to_city_id', '=', self.to_city_id.id),
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

    @api.depends('trip_id')
    def _compute_available_seats(self):
        """ Compute available seats based on booked tickets and bus capacity. """
        for record in self:
            if record.trip_id:
                booked_tickets = self.env['travel.ticket'].search_count([('trip_id', '=', record.trip_id.id)])
                record.available_seats = record.bus_id.seating_capacity - booked_tickets

    @api.onchange('trip_id')
    def _onchange_trip_id(self):
        """ Automatically set bus, payment amount, departure time, and boarding time when a trip is selected. """
        if self.trip_id:
            print(self.trip_id, self.trip_id.bus_id)
            self.bus_id = self.trip_id.bus_id or False
            self.payment_amount = self.trip_id.payment_amount
            self.departure_time = self.trip_id.departure_time
            # Set boarding time 30 minutes earlier than departure time
            if self.departure_time:
                self.boarding_time = self.departure_time - timedelta(minutes=30)

    @api.constrains('payment_amount')
    def _check_payment_amount(self):
        """ Ensure the payment amount is positive. """
        for record in self:
            if record.payment_amount <= 0:
                raise ValidationError("The payment amount must be a positive value.")

    @api.model
    def create(self, vals):
        """ Check seat availability before creating a ticket. """
        # trip = self.env['travel.ticket'].browse(vals['bus_id'])
        # booked_tickets = self.env['travel.ticket'].search_count([('trip_id', '=', trip.id)])

        # Check if there are enough seats left on the bus for the trip
        """ Ensure bus_id is set from the selected trip before creating the ticket. """
        if 'trip_id' in vals:
            trip = self.env['travel.trip'].browse(vals['trip_id'])
            vals['bus_id'] = trip.bus_id.id

        for record in self:
            if record.available_seats <= 0:
                raise ValidationError(f"Cannot book more tickets. The bus is fully booked for this trip.")

        # Proceed to create the ticket
        return super(TravelTicket, self).create(vals)

    def unlink(self):
        """ Restore available seats when a ticket is canceled. """
        for ticket in self:
            trip = ticket.trip_id
            booked_tickets = self.env['travel.ticket'].search_count([('trip_id', '=', trip.id)])
            if booked_tickets < trip.passenger_capacity:
                # Proceed with ticket deletion
                return super(TravelTicket, self).unlink()
            else:
                raise ValidationError("Cannot delete ticket as it might exceed the seating capacity.")

    def action_confirm(self):
        if self.state == 'draft':
            self.write({'state': 'confirmed'})

    def action_cancel(self):
        if self.state == 'confirmed':
            self.write({'state': 'cancelled'})

    def action_draft(self):
        if self.state == 'cancelled':
            self.write({'state': 'draft'})

    @api.constrains('from_city_id', 'to_city_id')
    def _check_cities(self):
        for record in self:
            if record.from_city_id == record.to_city_id:
                raise ValidationError("The departure city and destination city cannot be the same.")

    def action_send_email(self):
        """Send confirmation email to the customer."""
        # for ticket in self:
        #     if ticket.state != 'confirmed':
        #         raise ValidationError("Email can only be sent for confirmed tickets.")
        #
        #     # Fetch the email template
        #     template = self.env.ref('Travel_Agency.email_template_ticket_confirmation')
        #     if not template:
        #         _logger.warning("Email template not found.")
        #         return
        #
        #     # Prepare the email values
        #     email_values = {
        #         'email_to': ticket.customer_id.email,  # Customer's email
        #         'email_from': template.email_from,
        #         'subject': template.subject,
        #         'body_html': template.body_html.format(
        #             object=ticket  # Pass the ticket object to the template
        #         ),
        #     }
        #
        #     # Send the email
        #     mail = self.env['mail.mail'].create(email_values)
        #     mail.send()