from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    sale_order_type = fields.Selection([
        ('online', 'Online'),   
        ('offline', 'Offline')
    ], string='Sale Order Type', default='online')
