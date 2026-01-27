from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    passport_number = fields.Char(string='Passport Number')
    attempts = fields.Boolean(string='Attempts')
    registration_date = fields.Date(string='Registration Date')

    institute = fields.Boolean(string='معلومات المرحلة الاعدادية')
    specialization = fields.Char(string='Specialization')
    certificate = fields.Binary(string='Certificate')
    certificate_filename = fields.Char(string='Certificate Filename')
