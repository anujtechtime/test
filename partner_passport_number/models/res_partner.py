from odoo import models, fields, api
import re

class ResPartner(models.Model):
    _inherit = 'res.partner'

    passport_number = fields.Char(string='Passport Number')
    attempts = fields.Boolean(string='Attempts')
    registration_date = fields.Date(string='Registration Date')

    institute = fields.Boolean(string='معلومات المرحلة الاعدادية')
    specialization = fields.Char(string='Specialization')
    certificate = fields.Binary(string='Certificate')
    certificate_filename = fields.Char(string='Certificate Filename')



    @api.model
    def create(self, vals):
        if vals.get('passport_number'):
            vals['ID_Unified_Number'] = self._extract_numeric(vals['passport_number'])
        return super(ResPartner, self).create(vals)

    def write(self, vals):
        if vals.get('passport_number'):
            vals['ID_Unified_Number'] = self._extract_numeric(vals['passport_number'])
        return super(ResPartner, self).write(vals)

    def _extract_numeric(self, value):
        return ''.join(re.findall(r'\d+', value))
