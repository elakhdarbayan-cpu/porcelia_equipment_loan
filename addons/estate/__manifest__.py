{
    "name": "Estate",
    "version": "1.0",
    "category": "Real Estate",
    "summary": "Manage real estate properties",
    "description": "This module allows you to manage real estate properties, including listings, contracts, and transactions.",
    "depends": [
        "base",
        "sale",
        "contacts",
        "account"
    ],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menu.xml", 
        "views/sale_order_views.xml"
    ],
    "demo":[
        "demo/demo.xml"
    ],
    "installable": True,
    "application": True,
}