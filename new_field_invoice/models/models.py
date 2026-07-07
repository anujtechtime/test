# -*- coding: utf-8 -*-
from odoo import models, fields, api
import re


# class new_field_invoice(models.Model):
#     _name = 'new_field_invoice.new_field_invoice'
#     _description = 'new_field_invoice.new_field_invoice'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class TwchtTimet(models.Model):
    _inherit = 'account.move'

    Status = fields.Selection([('status4', 'مؤجل'),('status1','ترقين قيد'),('status2','طالب غير مباشر'),('status3','انسحاب'),('currecnt_student','Current student'),('succeeded','Succeeded'),('failed','Falied'),('transferred_from_us','Transferred From Us'),('graduated','Graduated')], string="Status", store=True, related="partner_id.Status")
    year_of_acceptance_1 = fields.Many2one("techtime_mcc_data.techtime_mcc_data", string="Year of acceptance", store=True, related="partner_id.year_of_acceptance_1")
