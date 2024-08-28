# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


# class almaaqal_payroll(models.Model):
#     _name = 'almaaqal_payroll.almaaqal_payroll'
#     _description = 'almaaqal_payroll.almaaqal_payroll'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class ContractmFields(models.Model):

    _inherit = "hr.contract"

    deduction_1 = fields.Float("Deduction One")
    deduction_2 = fields.Float("Deduction Two")


