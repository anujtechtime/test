# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class almaqal_student_discount(models.Model):
    _name = 'student.grade'
    _description = 'student.grade'

    shift = fields.Selection([('morning','Morning'),('afternoon','AfterNoon')], string="Shift")
    percentage_from = fields.Float("Percentage From")
    percentage_to = fields.Float("Percentage To")
    amount = fields.Char("Amount")

class InheritData(models.Model):
    _inherit = 'faculty.faculty'

    student_discoubt = fields.Many2many("student.grade", string="Student CGPA (Discount)")

class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    student_cgpa = fields.Float("Student CGPA")

class InstallmentDetails(models.Model):
    _inherit = "installment.details"

    student_dicount = fields.Boolean("Student Dicount")

class ResPrtner(models.Model):
    _inherit = 'sale.order'

    # @api.onchange('partner_id')
    # def _compute_partner_id(self):
    #     print("college################eeeeeeeeeeeeeeee",self.college.student_discoubt) 
    #     for cgpa in self.college.student_discoubt:
    #         if self.partner_id.shift >=  cgpa.shift and self.partner_id.student_cgpa >=  cgpa.percentage_from and self.partner_id.student_cgpa <=  cgpa.percentage_to:
    #             self.installment_amount = cgpa.amount
    #             instamm_ment_details = self.env["installment.details"].search([("student_dicount","=",True),("installment","=",cgpa.amount)])
    #             if instamm_ment_details:
    #                 for i in instamm_ment_details.sale_installment_line_ids:
    #                     sale_installment = self.sale_installment_line_ids.create({
    #                         'number' : i.number,
    #                         'payment_date' : i.payment_date,
    #                         'amount_installment' : i.amount_installment,
    #                         'description': 'Installment Payment',
    #                         'sale_installment_id' : result.id,
    #                         # "invoice_id" : invoice_id.id
    #                         })

    @api.onchange('partner_id')
    def _compute_partner_id(self):
        # if self.partner_id.shift >=  cgpa.shift and self.partner_id.student_cgpa >=  cgpa.percentage_from and self.partner_id.student_cgpa <=  cgpa.percentage_to:
        instamm_ment_details = self.env["installment.details"].search([("student_dicount","=",True),('college','=',self.college.id),('shift','=',self.shift),('year','=',self.year.id),('department','=',self.department.id),('percentage_from','>=',self.partne_id.final_result),('percentage_to','<=',self.partne_id.final_result)])
        self.installment = instamm_ment_details.installment
        if instamm_ment_details:
            for i in instamm_ment_details.sale_installment_line_ids:
                sale_installment = self.sale_installment_line_ids.create({
                    'number' : i.number,
                    'payment_date' : i.payment_date,
                    'amount_installment' : i.amount_installment,
                    'description': 'Installment Payment',
                    'sale_installment_id' : result.id,
                    # "invoice_id" : invoice_id.id
                    })

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
