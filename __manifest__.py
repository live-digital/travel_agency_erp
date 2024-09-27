{
    'name': 'Travel Agency Management',
    'version': '1.2',
    'author': 'Priyanka',
    'category': 'Services',
    'summary': 'Manage buses, drivers, cities, customers, trips, and tickets',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/trip_views.xml',
        'views/ticket_views.xml',
        'views/bus_views.xml',
        'views/driver_views.xml',
        'views/city_views.xml',
        'views/customer_views.xml',
        'reports/customer_booking_report.xml',
        # 'reports/bus_pnr_chart.xml',
        'data/email_template.xml',
        'data/ticket_sequence.xml',
        'data/trip_sequence.xml',
        'views/menu_views.xml'

    ],
    'installable': True,
    'application': True,
}
