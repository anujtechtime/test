# -*- coding: utf-8 -*-

from odoo import models, fields, api , _ 
from odoo.exceptions import UserError, ValidationError
import logging
import base64
from pdf2image import convert_from_path
from PIL import Image 
from datetime import date, datetime, timedelta


_logger = logging.getLogger(__name__)

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
    code = fields.Integer("Code")

# class ResPartnerInherit(models.Model):
#     _inherit = "res.partner"

    

class InstallmentDetails(models.Model):
    _inherit = "installment.details"

    student_dicount = fields.Boolean("Student Dicount")
    percentage_from = fields.Float("Percentage From")
    percentage_to = fields.Float("Percentage To")

class InheritData(models.Model):
    _inherit = 'department.department'

    code = fields.Integer("Code")    

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

    @api.model
    def create(self, vals):
        result = super(ResPrtner, self).create(vals)
        print("result##############",result)    
        print("result.college###########",result.college,result.department,result.student, result.year)
        installmet_dat = result.env["installment.details"].search([('college' , '=', result.college.id),("level","=",result.level),("Subject","=",result.Subject),('department','=',result.department.id),('Student','=',result.student.id),('year','=', result.year.id)],limit=1)
        print("result.id#$$$$$$$$$$$$$$$",installmet_dat)
        instamm_ment_details = self.env["installment.details"].search([("student_dicount","=",True),('college','=',result.college.id),('Subject','=',result.partner_id.shift),('year','=',result.year.id),('department','=',result.department.id),('percentage_from','<=',result.partner_id.final_result),('percentage_to','>=',result.partner_id.final_result)])
        print("installmet_dat@@@@@@@@@@@@@@@",installmet_dat)
        
        failed_student = self.env["sale.order"].search([("partner_id","=",result.partner_id.id),("college","=",result.partner_id.college.id),("year","!=",result.partner_id.year.id),("level","=",result.partner_id.level)], limit=1)
        print("failed_student@@@@@@@@@@@@@@@@",failed_student)
        _logger.info("failed_student************11111111111111#####**%s" %failed_student)
        if failed_student:
            result.installment_amount = failed_student.installment_amount
            for i in failed_student.sale_installment_line_ids:
                installment = result.sale_installment_line_ids.create({
                'number' : i.number,
                'payment_date' : i.payment_date,
                'amount_installment' : i.amount_installment,
                'description': 'Installment Payment',
                'sale_installment_id' : result.id,
                # "invoice_id" : invoice_id.id
                })  
        if not failed_student and installmet_dat:
            count = 0
            _logger.info("instamm_ment_detailsinstamm_ment_details11111111111111#####**%s" %instamm_ment_details)
            if instamm_ment_details:
                result.installment_amount = instamm_ment_details.installment
                for d in instamm_ment_details.sale_installment_line_ids:
                    _logger.info("dddddddddddddddddddddddddddddd#####**%s" %d)
                    sale_installment = result.sale_installment_line_ids.create({
                        'number' : d.number,
                        'payment_date' : d.payment_date,
                        'amount_installment' : d.amount_installment,
                        'description': 'Installment Payment',
                        'sale_installment_id' : result.id,
                        # "invoice_id" : invoice_id.id
                        })
            else:            
                result.installment_amount = installmet_dat.installment
                for i in installmet_dat.sale_installment_line_ids:
                    sale_installment = result.sale_installment_line_ids.create({
                        'number' : i.number,
                        'payment_date' : i.payment_date,
                        'amount_installment' : i.amount_installment,
                        'description': 'Installment Payment',
                        'sale_installment_id' : result.id,
                        # "invoice_id" : invoice_id.id
                        })
                    count = count + 1          

        if installmet_dat:
            print("sale_installment_line_ids########",installmet_dat.sale_installment_line_ids.ids)
            # for datts in installmet_dat.sale_installment_line_ids:
            # result.sale_installment_line_ids = [(6, 0, installmet_dat.sale_installment_line_ids.ids)]
            
            # result.payable_amount = installmet_dat.installment / installmet_dat.installment_number
            result.tenure_month = installmet_dat.installment_number
            result.second_payment_date = datetime.today().date()
            order_line = result.env['sale.order.line'].create({
                'product_id': 1,
                'price_unit': result.installment_amount,
                'product_uom': result.env.ref('uom.product_uom_unit').id,
                'product_uom_qty': 1,
                'order_id': result._origin.id,
                'name': 'sales order line',
            })

        return result


    @api.onchange('partner_id')
    def _compute_partner_id(self):
        if self.partner_id:
            # if self.partner_id.shift >=  cgpa.shift and self.partner_id.student_cgpa >=  cgpa.percentage_from and self.partner_id.student_cgpa <=  cgpa.percentage_to:
            instamm_ment_details = self.env["installment.details"].search([("student_dicount","=",True),('college','=',self.college.id),('Subject','=',self.partner_id.shift),('year','=',self.year.id),('department','=',self.department.id),('percentage_from','<=',self.partner_id.final_result),('percentage_to','>=',self.partner_id.final_result)])
            self.installment_amount = instamm_ment_details.installment
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


class ResPartnerSeq(models.Model):
    _inherit = "res.partner"
    student_cgpa = fields.Float("Student CGPA")

    @api.model
    def create(self, vals):
        result = super(ResPartnerSeq, self).create(vals)
        if 
        sequence_res = result.env['ir.sequence'].next_by_code('res.sequence')
        shift = 1 if result.shift == "morning" else 2
        result.college_number = str(result.year_of_acceptance_1.name)[-2:] + str(result.college.code) + str(result.department.code) + str(shift) + str(sequence_res)
        return result


    def add_sequence(self):
        sequence_res = self.env['ir.sequence'].next_by_code('res.sequence')
        shift = 1 if self.shift == "morning" else 2
        self.college_number = str(self.year_of_acceptance_1.name)[-2:] + str(self.college.code) + str(self.department.code) + str(shift) + str(sequence_res)


#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
