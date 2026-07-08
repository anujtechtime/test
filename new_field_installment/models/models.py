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


# class SaleMembershipInt(models.Model):
#     _inherit = 'sale.installment'

#     sale_installment_id = fields.Many2one("sale.order", string="Installment")

#     department = fields.Many2one(
#         'department.department',
#         related='sale_installment_id.department',
#         store=True,
#         readonly=True,
#     )

#     student = fields.Many2one(
#         'level.level',
#         related='sale_installment_id.student',
#         store=True,
#         readonly=True,
#     )

#     year = fields.Many2one(
#         'year.year',
#         related='sale_installment_id.year',
#         store=True,
#         readonly=True,
#     )
