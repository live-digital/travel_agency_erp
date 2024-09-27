from odoo.tools import format_datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

from odoo.odoo import exceptions
from odoo.odoo.tools.safe_eval import datetime

_logger = logging.getLogger(__name__)


class Ticket(models.Model):
    _name = 'travel.ticket'
    _description = 'Ticket Management'
    _inherit = ['mail.thread']

    pnr = fields.Char(string='PNR')
    name = fields.Char(string='Ticket Number', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    from_city_id = fields.Many2one('travel.city', string='From City', required=True,
                                   default=lambda self: self.env['travel.city'].search([('name', '=', 'Bhubaneswar')],
                                                                                       limit=1))
    to_city_id = fields.Many2one('travel.city', string='To City', required=True)
    customer_id = fields.Many2one('travel.customer', string='Customer', required=True)
    customer_age = fields.Integer(string='Customer Age', related='customer_id.age', store=True)
    customer_gender = fields.Selection(related='customer_id.gender', string='Customer Gender', store=True)
    seat_no = fields.Integer(string='Seat Number')  # Or use fields.Char if you need alphanumeric seat identifiers
    bus_id = fields.Many2one('travel.bus', string='Bus', required=True)
    boarding_time = fields.Datetime(string='Boarding Time', required=True)
    departure_time = fields.Datetime(string='Departure Time', required=True)
    payment_amount = fields.Float(string='Payment Amount', required=True)
    available_seats = fields.Integer(string="Available Seats", compute="_compute_available_seats", store=True)
    trip_id = fields.Many2one('travel.trip', string='Trip', required=True,
                              domain="[('departure_time', '>', datetime.now())]")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled')
    ], string='Status', default='draft', tracking=True)

    def action_print_ticket(self):
        return self.env.ref('travel_agency_management.ticket_report_action').report_action(self)

    @api.model
    def get_future_trips(self):
        current_time = datetime.now()
        return self.env['travel.trip'].search([('departure_time', '>', current_time)])

    @api.depends('trip_id')
    def _compute_available_seats(self):
        """ Compute available seats based on booked tickets and bus capacity. """
        for record in self:
            if record.trip_id:
                booked_tickets = self.env['travel.ticket'].search_count([('trip_id', '=', record.trip_id.id)])
                record.available_seats = record.bus_id.seating_capacity - booked_tickets

    @api.onchange('trip_id')
    def _onchange_trip_id(self):
        if self.trip_id:
            self.bus_id = self.trip_id.bus_id.id
            self.departure_time = self.trip_id.datetime
            self.payment_amount = self.trip_id.payment_amount

    @api.onchange('from_city_id', 'to_city_id')
    def _onchange_city(self):
        if self.from_city_id and self.to_city_id:
            # Auto-refresh the domain when cities are selected
            return {
                'domain': {
                    'trip_id': [('from_city_id', '=', self.from_city_id.id), ('to_city_id', '=', self.to_city_id.id)]
                }
            }

    def action_email(self):
        # Get the email template
        template_id = self.env.ref('travel_agency_management.email_template')

        # Log note with detailed information
        log_message = (
            f"Email sent for Ticket {self.name}:\n"
            f"Dear {self.customer_id.name},\n"
            f"Your ticket for the bus {self.trip_id.bus_id.name} has been confirmed.\n"
            f"Departure Time: {format_datetime(self.env, self.trip_id.datetime, tz=self.env.user.tz)}\n"
            f"From: {self.from_city_id.name}\n"
            f"To: {self.to_city_id.name}\n"
            f"Boarding Time: {self.boarding_time}\n"
            f"Payment Amount: {self.payment_amount}\n"
        )

        self.message_post(body=log_message)
        if template_id:
            template_id.send_mail(self.id, force_send=True)
            # confirm button

    def action_confirm(self):
        if self.state != 'draft':
            raise exceptions.UserError("Only tickets in draft state can be confirmed.")
        self.write({'state': 'confirmed'})
        _logger.info("Ticket %s confirmed.", self.name)

    # cancel button
    def action_cancel(self):
        if self.state != 'draft':
            raise UserError("Only tickets in draft state can be canceled.")
        self.write({'state': 'canceled'})
        _logger.info("Ticket %s canceled.", self.name)

    # draft button
    def action_draft(self):
        if self.state == 'confirmed':
            raise UserError("Confirmed tickets can't be reverted to draft.")
        elif self.state == 'canceled':
            raise UserError("Canceled tickets can't be reverted to draft.")

        # Set the ticket to draft
        self.write({'state': 'draft'})
        _logger.info("Ticket %s set to draft.", self.name)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            # Call the sequence generator defined in the XML
            _logger.info(self.customer_id.age)
            _logger.info(self.customer_id.gender)
            vals['name'] = self.env['ir.sequence'].next_by_code('travel.ticket') or _('New')
        return super(Ticket, self).create(vals)
