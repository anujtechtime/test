# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MoveDiv(models.Model):
    _inherit = "account.move"

    student_status_in_department = fields.Char(" الطالب في القسم")

# class new_field_installment(models.Model):
#     _name = 'new_field_installment.new_field_installment'
#     _description = 'new_field_installment.new_field_installment'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class SaleMembershipInt(models.Model):
    _inherit = 'sale.installment'

    department = fields.Many2one(
        'department.department',
        related='invoice_id.department',
        store=True,
        readonly=True,
    )

