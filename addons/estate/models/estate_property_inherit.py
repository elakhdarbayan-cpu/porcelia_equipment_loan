from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    
    @api.model
    def create(self, vals):
        if not vals.get('description'):
            vals['description'] = "No description provided"
        
        return super().create(vals)

    
    def unlink(self):
        for record in self:
            if record.state == 'sold':
                raise ValidationError("You cannot delete a sold property.")
        
        return super().unlink()