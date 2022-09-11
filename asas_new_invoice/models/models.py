# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigCompany_Bank(models.Model):
    _inherit = 'res.company'

    Bank_Name = fields.Char("Bank Name")
    Bank_City = fields.Char("Bank City")
    Bank_Country = fields.Char("Bank Country")
    Swift_Code = fields.Char("Swift Code")
    Bank_Account_number = fields.Char("Bank Account number")
    IBAN = fields.Char("IBAN")
    Account_currency = fields.Char("Account currency")
    Bank_Account_Name = fields.Char("Bank Account Name")
