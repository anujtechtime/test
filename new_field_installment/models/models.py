# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MoveDiv(models.Model):
    _inherit = "account.move"

    student_status_in_department = fields.Char(" الطالب في القسم")
    Status = fields.Selection([('status4', 'مؤجل'),('status1','ترقين قيد'),('status2','طالب غير مباشر'),('status3','انسحاب'),('currecnt_student','Current student'),('succeeded','Succeeded'),('failed','Falied'),('transferred_from_us','Transferred From Us'),('graduated','Graduated')], string="Status", store=True, related="partner_id.Status")
    year_of_acceptance_1 = fields.Many2one("techtime_mcc_data.techtime_mcc_data", string="Year of acceptance", store=True, related="partner_id.year_of_acceptance_1")

class SaleInstallment(models.Model):
    _inherit = 'sale.installment'

    # department = fields.Many2one(
    #     comodel_name='department.department',
    #     string='Department',
    #     compute='_compute_department',
    #     store=True,        # Store for performance
    #     readonly=True,
    # )
    department = fields.Many2one(
        'department.department',
        string='Department',
    )

    # @api.depends('invoice_id.department')
    # def _compute_department(self):
    #     for record in self:
    #         record.department = record.invoice_id.department

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

#     department = fields.Many2one(
#         'department.department',
#         related='invoice_id.department',
#         store=True,
#         readonly=True,
#     )

