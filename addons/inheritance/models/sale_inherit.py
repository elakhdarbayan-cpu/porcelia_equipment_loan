from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # ================= Extension InheritanceFields =================
    custom_field = fields.Char(string='Custom Field')
    