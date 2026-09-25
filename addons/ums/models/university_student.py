from odoo import models, fields
from datetime import datetime, date

class UniversityStudent(models.Model):
    _name = 'university.student'
    _description = 'University Student'

    name = fields.Char(string='Name')
    student_id = fields.Char(string='Student ID', unique=True)
    age = fields.Integer(string='Age')
    gpa = fields.Float(string='GPA')
    is_active = fields.Boolean(string='Active')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],string='Gender')
    birth_date = fields.Date(string='Birth Date')
    admission_date = fields.Datetime(string='Admission Date')   
    address = fields.Text(string='Address')
    profile_picture = fields.Binary(string='Profile Picture')
    profile= fields.Html(string='Profile')
