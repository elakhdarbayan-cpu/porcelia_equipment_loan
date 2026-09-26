from odoo import models, fields, api

class EquipmentCategory(models.Model):
    _name = 'equipment.category'
    _description = 'Equipment Category'
    _parent_store = True
    _order = 'complete_name'

    name = fields.Char(string='Name', required=True, translate=True)
    parent_id = fields.Many2one(
        'equipment.category',
        string='Parent Category',
        ondelete='cascade'
    )
    child_ids = fields.One2many(
        'equipment.category',
        'parent_id',
        string='Child Categories'
    )
    parent_path = fields.Char(index=True)
    complete_name = fields.Char(
        string='Complete Name',
        compute='_compute_complete_name',
        store=True
    )
    item_count = fields.Integer(
        string='Items',
        compute='_compute_item_count'
    )

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = f"{category.parent_id.complete_name} / {category.name}"
            else:
                category.complete_name = category.name

    def _compute_item_count(self):
        for category in self:
            category.item_count = self.env['equipment.item'].search_count([
                ('category_id', '=', category.id)
            ])
            