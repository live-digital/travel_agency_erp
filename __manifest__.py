{
    'name': 'Travel Agency Management',
    'version': '1.0.0',
    'category': 'Travel',
    'author' : 'Mangan',
    'license': 'LGPL-3',
    'summary': 'Module for managing bus trips, drivers, cities, and tickets',
    'description': """
       Travel Agency Management:
       - Manage buses, drivers, and trips
       - Handle customer ticket bookings
       - Generate reports (Customer Booking Ticket PDF, Bus PNR Chart)
       - Email alerts for customers
   """,
'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/email_templates.xml',
        # Views
        'views/bus_master.xml',
        'views/city_master.xml',
        'views/driver_master.xml',
        'views/customer_master.xml',
        'views/trip.xml',
        'views/ticket.xml',

        'data/Trip_Name.xml',
        'report/ticket_report.xml',

        # Menus
        'views/travel_agency_views.xml',



    ],
'installable': True,
'application': True,
}
