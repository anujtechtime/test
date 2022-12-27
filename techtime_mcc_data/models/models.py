# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


# class techtime_mcc_data(models.Model):
#     _name = 'techtime_mcc_data.techtime_mcc_data'
#     _description = 'techtime_mcc_data.techtime_mcc_data'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
class CrmTeamDateAccount(models.Model):

    _inherit = "account.payment"

    payment_method = fields.Account_Type = fields.Selection([('cash','نقد'),
        ('debit','دين'),
        ('cheque','صك')],string="Payment Method")


class CrmTeamDateAccount(models.Model):

    _inherit = "purchase.order.line"

    qty_received = fields.Float("Received Qty", related="product_qty", inverse='_inverse_qty_received', compute_sudo=True, store=True, digits='Product Unit of Measure')

class ContractmDateAccount(models.Model):

    _inherit = "hr.contract"

    employ_type  = fields.Selection([('option1','تعيين - متقاعد'),
        ('option2','تعيين - غير متقاعد مشمول بالضمان'),
        ('option3','اعارة'),
        ('option4', 'محاضر خارجي'),
        ('option5','اجر يومي')], string="Employee Type")
    basic_salary = fields.Float('Basic Salary')
    social_security = fields.Float("Social Security")
    tax = fields.Float("Tax")
    tax_other = fields.Float("Tax Other")
    traning = fields.Float("Traning")
    allowance = fields.Float("Allowance")
    day_deduction = fields.Float("Day-Deduction")


    @api.onchange('wage')
    def _inverse_wage(self):
        if self.wage:
            self.basic_salary = float(self.wage) * 0.7




class ContraPayslipDateAccount(models.Model):

    _inherit="hr.payslip"

    description = fields.Html("Description")






