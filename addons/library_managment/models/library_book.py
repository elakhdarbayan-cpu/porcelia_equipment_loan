from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _rec_name = 'reference'
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    # Sequence Reference
    reference = fields.Char(string='Reference', readonly=True, copy=False, default=lambda self: self.env['ir.sequence'].next_by_code('library.book') or 'New')

    
    
    name = fields.Char(string='Book Title', required=True, tracking=True)
    description = fields.Text(string='Description')
    is_active = fields.Boolean(string='Active', default=True)

    price = fields.Float(string='Price')
    quantity = fields.Integer(string='Quantity', default=1)

    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)

    attachment = fields.Binary(string='Attachment')
    last_update = fields.Datetime(string='Last Updated', default=fields.Datetime.now)

    publish_date = fields.Date(string='Publish Date')
    expiry_date = fields.Date(string='Expiry Date')
    is_expired = fields.Boolean(string='Is Expired', compute='_compute_is_expired', store=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost')
    ], string='Status', default='draft', tracking=True)

    user_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Customer')
    partner_phone = fields.Char(string='Phone', related='partner_id.phone')

    category_ids = fields.Many2many('library.category', string='Categories')
    line_ids = fields.One2many('library.book.line', 'book_id', string='Book Chapters')



    # ================= Computed Fields =================
    @api.depends('price', 'quantity')
    def _compute_total_amount(self):
        for book in self:
            book.total_amount = book.price * book.quantity

    @api.depends('expiry_date')
    def _compute_is_expired(self):
        today = date.today()
        for book in self:
            book.is_expired = book.expiry_date and book.expiry_date < today

    # ================= Constraints =================
    @api.constrains('price')
    def _check_price(self):
        for book in self:
            if book.price < 0:
                raise ValidationError('Price cannot be negative!')

    @api.constrains('quantity')
    def _check_quantity(self):
        for book in self:
            if book.quantity <= 0:
                raise ValidationError('Quantity must be greater than zero!')

    @api.constrains('publish_date', 'expiry_date')
    def _check_dates(self):
        for book in self:
            if book.publish_date and book.expiry_date and book.expiry_date < book.publish_date:
                raise ValidationError('Expiry date cannot be earlier than publish date!')
    @api.model        
    def unlink(self):
        for book in self:
            if book.state == 'borrowed':
                raise ValidationError('Cannot delete a book that is currently borrowed!')
        return super().unlink()

    # =================  buttons =================
    def action_draft(self):
        self.state = 'draft'

    def action_available(self):
        self.state = 'available'

    def action_borrowed(self):
        self.state = 'borrowed'

    def action_lost(self):
        self.state = 'lost'


class LibraryBookLine(models.Model):
    _name = 'library.book.line'
    _description = 'Library Book Chapter'

    book_id = fields.Many2one('library.book', string='Book',)
    chapter_name = fields.Char(string='Chapter Name')
    pages = fields.Integer(string='Number of Pages')