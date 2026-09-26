from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from math import ceil

class EquipmentLoan(models.Model):
    _name = 'equipment.loan'
    _description = 'Equipment Loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('equipment.loan') or 'New'
    )

    item_id = fields.Many2one(
        'equipment.item',
        string='Item',
        required=True,
        tracking=True
    )
    borrower_id = fields.Many2one(
        'res.users',
        string='Borrower',
        required=True,
        default=lambda self: self.env.user,
        tracking=True
    )

    date_start = fields.Datetime(
        string='Start Date',
        required=True,
        tracking=True
    )
    date_due = fields.Datetime(
        string='Due Date',
        required=True,
        tracking=True
    )
    date_return = fields.Datetime(
        string='Return Date',
        tracking=True
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    days_late = fields.Integer(
        string='Days Late',
        compute='_compute_penalty',
        store=True
    )
    penalty_amount = fields.Monetary(
        string='Penalty Amount',
        compute='_compute_penalty',
        store=True,
        currency_field='currency_id'
    )
    currency_id = fields.Many2one(
        related='item_id.currency_id',
        store=True
    )

    is_overdue = fields.Boolean(
        string='Is Overdue',
        default=False
    )
    notes = fields.Html(string='Notes')

    # ==================== Computed ====================
    @api.depends('date_return', 'date_due', 'item_id.daily_rate')
    def _compute_penalty(self):
        for loan in self:
            if loan.date_return and loan.date_due and loan.date_return > loan.date_due:
                delta = loan.date_return - loan.date_due
                loan.days_late = max(ceil(delta.total_seconds() / 86400), 0)
                loan.penalty_amount = loan.days_late * (loan.item_id.daily_rate or 0)
            else:
                loan.days_late = 0
                loan.penalty_amount = 0

    # ==================== Constraints ====================
    @api.constrains('date_start', 'date_due')
    def _check_dates(self):
        for loan in self:
            if loan.date_start and loan.date_due and loan.date_due <= loan.date_start:
                raise ValidationError("Due Date must be after Start Date.")

    # ==================== Buttons ========================
    def action_confirm(self):
        for loan in self:
         if loan.state != 'draft':
            raise ValidationError("Only draft loans can be confirmed.")

        # ===== No Double Booking =====
        overlapping = self.env['equipment.loan'].search([
            ('id', '!=', loan.id),
            ('item_id', '=', loan.item_id.id),
            ('state', '=', 'confirmed'),
            ('date_return', '=', False),
            ('date_start', '<', loan.date_due),
            ('date_due', '>', loan.date_start),
        ], limit=1)

        if overlapping:
            raise ValidationError(
                f"This item is already on loan in a conflicting period.\n"
                f"Conflicting Loan: {overlapping.name}\n"
                f"Period: {overlapping.date_start} → {overlapping.date_due}"
            )

        loan.state = 'confirmed'
        return True
        

    def action_return(self):
        for loan in self:
            if loan.state != 'confirmed':
                raise ValidationError("Only confirmed loans can be returned.")
            loan.state = 'returned'
            if not loan.date_return:
                loan.date_return = fields.Datetime.now()
        return True

    def action_cancel(self):
        for loan in self:
            if loan.state == 'returned':
                raise ValidationError("Returned loans cannot be cancelled.")
            loan.state = 'cancelled'
        return True

    def action_draft(self):
        for loan in self:
            loan.state = 'draft'
        return True
    @api.ondelete(at_uninstall=False)

    def _unlink_only_draft_or_cancelled(self):
        for loan in self:
            if loan.state not in ('draft', 'cancelled'):
                raise ValidationError("You can only delete draft or cancelled loans.")