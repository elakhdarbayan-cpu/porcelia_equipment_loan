from odoo import models, fields,api
from datetime import datetime,date
from odoo.exceptions import ValidationError, UserError

class RealState(models.Model):
    _name = 'real.state'      
    _inherit = ['mail.thread', 'mail.activity.mixin']    
    _description = 'Real State'
    _rec_name = 'name'

    refrence = fields.Char(string='Reference', readonly=True,  default=lambda self: ('New'))
  
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('refrence', ('New')) == ('New'):
                vals['refrence'] = self.env['ir.sequence'].next_by_code('real.state.sequence') or ('New')
        result = super(RealState, self).create(vals_list)
        return result

    name = fields.Char(string='Property Name', tracking=True)
    description = fields.Text(string='Description')
    #namelength = fields.Integer(string='Length', compute='_compute_name_length', store=True)

    #@api.depends('name')
    #def _compute_name_length(self):
        #for record in self:
            #record.namelength = len(record.name or "")
          

    price = fields.Float(string='Price', tracking=True)
    tax = fields.Float(string='Tax')
    tax_total = fields.Float(string='Total Price', compute='_compute_tax_total', store=True)

    @api.depends('price','tax')
    def _compute_tax_total(self):
        for record in self:
            record.tax_total = record.price + record.tax

    @api.onchange('price')
    def _onchange_tax_total(self):
        warning={}
        if self.price < 0:
            warning = {
                'title': 'Invalid Price',
                'message': 'Price cannot be negative.',
            }
        return {'warning': warning}
    
   # @api.constrains('price')
    #def _check_price(self):
     #   for record in self:
      #      if record.price < 0:
       #         raise ValidationError('Price cannot be negative.')        
            
    location = fields.Char(string='Location')
    available = fields.Boolean(string='Available', default=True)        
    availability_status = fields.Char(string='Availability Status', compute='_compute_availability')
    @api.depends('available')
    def _compute_availability(self):
        for record in self:
            record.availability_status = 'Available' if record.available else 'Not Available'
    
    
    binary_image = fields.Binary(string='Property Image')   
    state = fields.Selection([
        ('available', 'Available'),
        ('done', 'Done'),('draft', 'Draft')
    ], string="State", default='draft', tracking=True)

    def action_draft(self):
        self.write({'state': 'draft'})
        return True

    def action_available(self):
        self.write({'state': 'available'})
        return True

    def action_done(self):
        self.write({'state': 'done'})
        return True
    
    property_details = fields.Html(string='Property Details')
    
    property_type = fields.Selection([
        ('sale', 'For Sale'),
        ('rent', 'For Rent')
    ], string='Property Type', default='sale')
    sale_date = fields.Date(string='Sale Date')
    create_date = fields.Date(string='Created On' , compute ='_compute_sale_date', store=True)

    @api.constrains('sale_date')
    def _check_sale_date(self):
        today = date.today()
        for record in self:
            if record.sale_date and record.sale_date >= today:
                raise ValidationError('Sale date cannot be in the future or today.')
            
    @api.depends('create_date')
    def _compute_sale_date(self):
        for record in self:
            if record.property_type == 'sale' and not record.sale_date:
                record.create_date = date.today()
    
    
    field_order = fields.Many2one('sale.order',string="Field Order", domain="[('state', '=', 'sale')]"  )
    sale_customer = fields.Many2one('res.partner',string="Sale Customer", related='field_order.partner_id')
    sale_date = fields.Datetime(string="Sale Date", related='field_order.date_order')  #related field

    field_orders = fields.Many2many('sale.order',string="Field Orders")
    user_id = fields.Many2one('res.users',string="User")

    partner_id = fields.Many2one('res.partner',string="partner")
    partner_phone = fields.Char(string="Phone", related='partner_id.phone')
   
   
   
   
    def create_real_state(self):
        new_record = self.env['real.state'].create(
            {
                'name':'new odoo',
                'description':'this is new record',
                'price': 100000.0,
                'location':'cairo',
                'available': True,
                'property_type': 'sale',
            }          
            )
        return new_record
    def read_real_state(self):
        records = self.env['real.state'].browse(21)
        if records.exists():
            print(f"Record Name: {records.name}, Price: {records.price}")
        return records
    
    def search_real_state(self):
        records = self.env['real.state'].search([('price', '>', 50000)])
        for record in records:
            print(f"Record Name: {record.name}, Price: {record.price}, Location: {record.location}")
        return records   

    def search_or(self):
        records = self.env['real.state'].search([
            '|',
            ('price', '>', 50000),
            ('location','=','cairo')])
        for record in records:
            print(f"Record Name: {record.name}, Price: {record.price}, Location: {record.location}")
        return records
    
    def delete_real_state(self):
        record = self.env['real.state'].browse(1)
        record.unlink()


     # =================  buttons =================


    @api.model
    #def create(self, vals):
        
     #   if not vals.get('description'):
      #     vals['description'] = "Default description"
       # record = super().create(vals)
        #return record
    
   
    def write(self, vals):
        if 'price' in vals and vals['price'] < 0:
            raise ValidationError('Price cannot be negative.')
        return super().write(vals)
    
    def unlink(self):
        for record in self:
            if record.availability_status=="Available":
                raise ValidationError('Cannot delete available properties.')
        record= super().unlink()
        return record
    
    def copy(self, default=None):
        if self.property_type == 'sale':
            raise UserError('Cannot duplicate properties for sale.')
        return super().copy(default)


 
    #######################################################################################################################

    line_ids = fields.One2many('real.state.line', 'line_id', string=' Lines')
    





class RealStateLine(models.Model):
    _name = 'real.state.line'
    _description = 'Real State Line'

    
    line_id = fields.Many2one('real.state', string='Real State')
    name = fields.Char(string='Line Name')
    price = fields.Float(string=' Price')