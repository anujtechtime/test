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

    final_result = fields.Char("CGPA", compute="_data_for_final_result")
    data_one = fields.Many2one("new.work", string="نافذة القبول")
    show_invoice_button = fields.Boolean("Show Invoive Button")

    def _data_for_final_result(self):
        for final in self:
            if final.partner_id:
                final.final_result = final.partner_id.final_result
                final.data_one = final.partner_id.data_one

    def action_installment_invoice(self):
        result = super(ResPrtner, self).action_installment_invoice()
        result.show_invoice_button = False
        return result

    def action_create_badge_invoice(self):
        for result in self:
            instamm_ment_details = self.env["installment.details"].search([("student_dicount","=",True),('college','=',result.partner_id.college.id),("Student","=",result.student.id),("level","=",result.partner_id.level),('Subject','=',result.partner_id.shift),('year','=',result.partner_id.year.id),('department','=',result.partner_id.department.id),('percentage_from','<=',result.partner_id.final_result),('percentage_to','>=',result.partner_id.final_result)], limit=1)
            print("instamm_ment_details@@@@@@@@@@@@@@@@",instamm_ment_details)
            product_id = self.env["product.product"].search([("id",'=',3)])
            journal = self.env['account.move'].with_context(default_type='out_invoice')._get_default_journal()
            count = 0
            invoice_vals = {
                'ref': result.client_order_ref or '',
                'type': 'out_invoice',
                'narration': result.note,
                'invoice_date': result.second_payment_date,
                'invoice_date_due' : result.date_order,
                'currency_id': result.pricelist_id.currency_id.id,
                'campaign_id': result.campaign_id.id,
                'medium_id': result.medium_id.id,
                'source_id': result.source_id.id,
                'invoice_user_id': result.user_id and result.user_id.id,
                'team_id': result.team_id.id,
                'partner_id': result.partner_invoice_id.id,
                'partner_shipping_id': result.partner_shipping_id.id,
                'invoice_partner_bank_id': result.company_id.partner_id.bank_ids[:1].id,
                'fiscal_position_id': result.fiscal_position_id.id or result.partner_invoice_id.property_account_position_id.id,
                'journal_id': journal.id,  # company comes from the journal
                'invoice_origin': result.name,
                'invoice_payment_term_id': result.payment_term_id.id,
                'invoice_payment_ref': result.reference,
                'transaction_ids': [(6, 0, result.transaction_ids.ids)],
                'invoice_line_ids': [(0, 0, {
                    'name': product_id.name,
                    'price_unit': product_id.lst_price,
                    'quantity': 1.0,
                    'product_id': product_id.id,
                    # 'tax_ids': [(6, 0, self.order_line.tax_id.ids)],
                    'analytic_account_id': result.analytic_account_id.id or False,
                })],
                'company_id': result.company_id.id,
                'sponsor' : result.sponsor.id,
            } 

            result.show_invoice_button = True
            count = count + 1

            invoice_id = self.env['account.move'].create(invoice_vals)
            invoice_id.action_post()
            # i.invoice_id = invoice_id.id
            # print("invoice_id##############",invoice_id)

            # account_invoice_line  = self.env['account.move.line'].with_context(
            #     check_move_validity=False).create({
            #     'name': self.order_line.product_id.name,
            #     'price_unit': self.payable_amount,
            #     'quantity': 1.0,
            #     'discount': 0.0,
            #     'journal_id': journal.id,
            #     'product_id': self.order_line.product_id.id,
            #     'analytic_account_id': self.analytic_account_id.id,
            #     'account_id': self.partner_invoice_id.property_account_receivable_id.id,
            #     'move_id': invoice_id.id,
            #     })
            # for order in self:
            #     order.order_line.update({
            #         'invoice_lines' : [(4, account_invoice_line.id)]
            #         })

            result.order_line.update({
                'invoice_lines' : [(4, invoice_id.invoice_line_ids.id)]
                })


            # result.write({
            #     "invoice_id" : invoice_id.id,
            # })
        return True

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

    def change_value_for_sale_order_line(self):
        for lin in self:
            if lin.order_line:
                lin.order_line.price_unit = lin.installment_amount

    @api.model
    def create(self, vals):
        result = super(ResPrtner, self).create(vals)
        print("result##############",result)    
        print("result.college###########",result.college,result.department,result.student, result.year)
        installmet_dat = result.env["installment.details"].search([('college' , '=', result.college.id),("level","=",result.level),("Subject","=",result.Subject),('department','=',result.department.id),('Student','=',result.student.id),('year','=', result.year.id)],limit=1)
        print("result.id#$$$$$$$$$$$$$$$",installmet_dat)
        instamm_ment_details = self.env["installment.details"].search([("student_dicount","=",True),('college','=',result.partner_id.college.id),("Student","=",result.student.id),("level","=",result.partner_id.level),('Subject','=',result.partner_id.shift),('year','=',result.partner_id.year.id),('department','=',result.partner_id.department.id),('percentage_from','<=',result.partner_id.final_result),('percentage_to','>=',result.partner_id.final_result)], limit=1)
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
        count = 0        
        if not failed_student and installmet_dat:
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
                    if count == 0:
                        result.amount = ('{:,}'.format(d.amount_installment))
                        count = count + 1
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
                    if count == 0:
                        result.amount = ('{:,}'.format(i.amount_installment))
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
            # if count == 0:
            #     result.amount = d.amount_installment
            #     count = count + 1

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
        if result.college and result.year_of_acceptance_1 and result.department: 
            sequence_res = result.env['ir.sequence'].next_by_code('res.sequence')
            shift = 1 if result.shift == "morning" else 2
            result.college_number = str(result.year_of_acceptance_1.name)[-2:] + str(result.college.code) + str(result.department.code) + str(shift) + str(sequence_res)
        return result


    def add_sequence(self):
        for sstd in self:
            sequence_res = self.env['ir.sequence'].next_by_code('res.sequence')
            shift = 1 if sstd.shift == "morning" else 2
            sstd.college_number = str(sstd.year_of_acceptance_1.name)[-2:] + str(sstd.college.code) + str(sstd.department.code) + str(shift) + str(sequence_res)



class PaymentValue(models.Model):
    _inherit = "account.payment"
 
    boolean_data = fields.Boolean("رسوم هوية")
    
    def change_the_value_department(self):
        _logger.info("self************11111111111111#####**%s" %self)
        for ddtt in self:
            if ddtt.partner_id:
                _logger.info("ddtt.partner_id************11111111111111#####**%s" %ddtt.partner_id)
                ddtt.update({
                    "college" : ddtt.partner_id.college.id if ddtt.partner_id.college else False,
                    "student" : ddtt.partner_id.student_type.id if ddtt.partner_id.student_type else False,
                    "department" : ddtt.partner_id.department.id if ddtt.partner_id.department else False,
                    "Subject" : ddtt.partner_id.shift if ddtt.partner_id.shift else False,
                    "level" : ddtt.partner_id.level if ddtt.partner_id.level else False,
                    "year" : ddtt.partner_id.year if ddtt.partner_id.year else False,
                    })     


class DataInherit(models.Model):
    _inherit = "account.move"

    def change_the_value_using_sale_order(self):
        for ddtt in self:
            sale_order_data = self.env['sale.order'].search([("name",'=',ddtt.invoice_origin)])
            if sale_order_data:
                _logger.info("ddtt.partner_id************11111111111111#####**%s" %ddtt.partner_id)
                ddtt.update({
                    "college" : sale_order_data.college.id if sale_order_data.college else False,
                    "student" : sale_order_data.student.id if sale_order_data.student else False,
                    "department" : sale_order_data.department.id if sale_order_data.department else False,
                    "Subject" : sale_order_data.Subject if sale_order_data.Subject else False,
                    "level" : sale_order_data.level if sale_order_data.level else False,
                    "year" : sale_order_data.year if sale_order_data.year else False,
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
