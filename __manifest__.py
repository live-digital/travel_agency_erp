{
  "name": "Travel Management System",
  "author" : "manasi",
  "license" : "LGPL-3",
  "version" : "17.0.1.1",
  "summary" : "Manage travel buses, trips, tickets, and drivers",
  "depends" : ["base", "mail"],
  "data" :
    [
      "security/ir.model.access.csv",
      "security/groups.xml",
      "views/bus_views.xml",
      "views/city_views.xml",
      "views/driver_views.xml",
      "views/customer_views.xml",
      "views/trip_views.xml",
      "views/ticket_views.xml",
      "views/menu_views.xml",
      ],

  "installable": True,
  "application": True
}