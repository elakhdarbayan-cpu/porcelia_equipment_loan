from odoo import models, fields, api

class EquipmentItem(models.Model):
    _name = 'equipment.item'
    _description = 'Equipment Item'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(
        string='Code',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('equipment.item') or 'New'
    )
    category_id = fields.Many2one(
        'equipment.category',
        string='Category'
    )
    image_1920 = fields.Image(string='Image')
    active = fields.Boolean(string='Active', default=True)

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    daily_rate = fields.Monetary(
        string='Daily Rate',
        currency_field='currency_id'
    )

    condition_score = fields.Integer(
        string='Condition Score',
        default=100
    )

    state = fields.Selection([
        ('available', 'Available'),
        ('on_loan', 'On Loan'),
        ('maintenance', 'Maintenance'),
        ('scrapped', 'Scrapped')
    ], string='Status', default='available', compute='_compute_state', store=True)

    loan_ids = fields.One2many(
        'equipment.loan',
        'item_id',
        string='Loans'
    )
    loan_count = fields.Integer(
        string='Loan Count',
        compute='_compute_loan_count'
    )

    total_days_on_loan = fields.Integer(
        string='Total Days on Loan',
        compute='_compute_total_days_on_loan'
    )

    @api.depends('loan_ids', 'loan_ids.state', 'loan_ids.date_return')
    def _compute_state(self):
        for item in self:
            confirmed_loans = item.loan_ids.filtered(
                lambda l: l.state == 'confirmed' and not l.date_return
            )
            if confirmed_loans:
                item.state = 'on_loan'
            else:
                item.state = 'available'

    def _compute_loan_count(self):
        for item in self:
            item.loan_count = len(item.loan_ids)

    def action_view_loans(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Loans',
            'res_model': 'equipment.loan',
            'view_mode': 'list,form',
            'domain': [('item_id', '=', self.id)],
            'context': {'default_item_id': self.id},
        }
    _sql_constraints = [
    (
        'code_unique',
        'unique(code)',
        'The equipment item code must be unique!'
    ),]
