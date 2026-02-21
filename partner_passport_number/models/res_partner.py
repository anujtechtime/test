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


    # @api.model
    # def create(self, vals):
    #     if vals.get('passport_number'):
    #         passport = vals.get('passport_number').strip()

    #         # If contains any alphabet → keep in passport field
    #         if re.search(r'[A-Za-z]', passport):
    #             pass
    #         else:
    #             # Only numbers → shift to ID_Unified_Number
    #             vals['ID_Unified_Number'] = passport
    #             vals['passport_number'] = False

    #     return super(ResPartner, self).create(vals)

    # def write(self, vals):
    #     if vals.get('passport_number'):
    #         passport = vals.get('passport_number').strip()

    #         if re.search(r'[A-Za-z]', passport):
    #             pass
    #         else:
    #             vals['ID_Unified_Number'] = passport
    #             vals['passport_number'] = False

    #     return super(ResPartner, self).write(vals)

    @api.model
    def create(self, vals):
        passport = vals.get('passport_number')

        if passport:
            passport = passport.strip()

            # If ONLY digits → move to ID_Unified_Number
            if passport.isdigit():
                vals['ID_Unified_Number'] = passport
                vals['passport_number'] = False
            else:
                vals['passport_number'] = passport
                vals['ID_Unified_Number'] = False

        return super(ResPartner, self).create(vals)

    def write(self, vals):
        if 'passport_number' in vals:
            passport = vals.get('passport_number')

            if passport:
                passport = passport.strip()

                if passport.isdigit():
                    vals['ID_Unified_Number'] = passport
                    vals['passport_number'] = False
                else:
                    vals['passport_number'] = passport
                    vals['ID_Unified_Number'] = False

        return super(ResPartner, self).write(vals) 

