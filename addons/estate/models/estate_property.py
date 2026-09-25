from odoo import models, fields, api
from datetime import datetime,date, timedelta



class RealEstate(models.Model):
    _name = 'estate.property'         
    _description = 'Estate Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char(string='Name', required=True , default='House' )
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Post Code')
    date_availabilty = fields.Date( string = 'Data Availability', default=date.today(), copy=False)
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden Orientation')
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
        ('accepted', ' Offer Accepted')] , 
        required=True, default='new', string='Status', copy=False)
    postcode = fields.Char(string='Postcode')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers',tracking=True)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    total_area = fields.Integer(string='Total Area (sqm)', compute='_compute_total_area', store=True)


    best_offer = fields.Float(string='Best Offer', compute='_compute_best_offer', store=True)
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0.0

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    @api.depends( 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.date_availabilty + timedelta(days=record.validity)
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days 
