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

    compensation = fields.Float("Compensation")


    married_with_house_wife = fields.Boolean("Married Male with house wife")
    married_with_working_wife = fields.Boolean("Married Male with working wife")

    married_with_non_working_husband = fields.Boolean("Married Female with non-working husband")
    married_with_working_husband = fields.Boolean("Married Female with working husband")



    single_male = fields.Boolean("Single Male")

    male_female_with_children = fields.Integer("Female with No. of children")

    divorced_male = fields.Boolean("Divorced Male")

    sinle_female = fields.Boolean("Single Female")

    divorced_female = fields.Boolean("Divorced Female")

    if_age_is_above_63 = fields.Boolean("Age is above 63")

    total_salary = fields.Float("Total Salary")



    # tax = fields.Float("Tax")
    # tax_other = fields.Float("Tax Other")
    # traning = fields.Float("Traning")
    # allowance = fields.Float("Allowance")
    # day_deduction = fields.Float("Day-Deduction")



    @api.onchange('wage','compensation','social_security','married_with_house_wife','married_with_working_wife','married_with_non_working_husband','married_with_working_husband','single_male','male_female_with_children','divorced_male','sinle_female','divorced_female','if_age_is_above_63')
    def _inverse_wage(self):
        if self.wage:
            self.basic_salary = float(self.wage) * 0.7
            self.compensation = float(self.basic_salary) * 0.3
            self.social_security = float(self.basic_salary) * 0.05


            if self.married_with_house_wife:
                self.total_salary = self.social_security + self.compensation + 375000
            if self.married_with_working_wife:
                self.total_salary = self.social_security + self.compensation + 208333
            if self.married_with_non_working_husband:
                self.total_salary = self.social_security + self.compensation + 416666
            if self.married_with_working_husband:
                self.total_salary = self.social_security + self.compensation + 208333
            if self.single_male:
                self.total_salary = self.social_security + self.compensation + 208333
            if self.male_female_with_children:
                self.total_salary = self.social_security + self.compensation + self.male_female_with_children * 16666
            if self.divorced_male:
                self.total_salary = self.social_security + self.compensation + 208333
            if self.sinle_female:
                self.total_salary = self.social_security + self.compensation + 255555
            if self.divorced_female:
                self.total_salary = self.social_security + self.compensation + 255555
            if self.if_age_is_above_63:
                self.total_salary = self.social_security + self.compensation + 25000

            if self.total_salary > 1000000:
                self.total_salary =  self.total_salary - 83333 * 0.15 + 5833

            if self.total_salary > 500000:
                self.total_salary =  self.total_salary - 41666 * 0.1 + 1666

            if self.total_salary > 250000:
                self.total_salary =  self.total_salary - 20833 * 0.05 + 625           





class ContraPayslipDateAccount(models.Model):

    _inherit="hr.payslip"

    description = fields.Html("Description")






