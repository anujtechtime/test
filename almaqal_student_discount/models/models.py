# -*- coding: utf-8 -*-

from odoo import models, fields, api , _ 
from odoo.exceptions import UserError, ValidationError
import logging
import base64
from pdf2image import convert_from_path
from PIL import Image 
from datetime import date, datetime, timedelta

import json
import base64
import xlwt
from dateutil.relativedelta import relativedelta
import io
from lxml import etree
import html2text

_logger = logging.getLogger(__name__)


class techtime_payrollEmployee(models.Model):
    _inherit = 'hr.employee'

    first_field = fields.Char("Specialization")

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
    active_report = fields.Boolean("Show In Report", default=False)

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
        self.show_invoice_button = True
        return result

    def action_create_badge_invoice(self):
        for result in self:
            instamm_ment_details = self.env["installment.details"].search([("student_dicount","=",True),('college','=',result.partner_id.college.id),("Student","=",result.student.id),("level","=",result.partner_id.level),('Subject','=',result.partner_id.shift),('year','=',result.partner_id.year.id),('department','=',result.partner_id.department.id),('percentage_from','<=',result.partner_id.final_result),('percentage_to','>=',result.partner_id.final_result)], limit=1)
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

            result.show_invoice_button = False
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

    def contains_duplicate(self, lst):
        return len(lst) != len(set(lst))  

    @api.model
    def create(self, vals):
        result = super(ResPrtner, self).create(vals)
        installmet_dat = result.env["installment.details"].search([('college' , '=', result.college.id),("level","=",result.level),("Subject","=",result.Subject),('department','=',result.department.id),('Student','=',result.student.id),('year','=', result.year.id)],limit=1)
        instamm_ment_details = self.env["installment.details"].search([("student_dicount","=",True),('college','=',result.partner_id.college.id),("Student","=",result.student.id),("level","=",result.partner_id.level),('Subject','=',result.partner_id.shift),('year','=',result.partner_id.year.id),('department','=',result.partner_id.department.id),('percentage_from','<=',result.partner_id.final_result),('percentage_to','>=',result.partner_id.final_result)], limit=1)
        failed_student = self.env["sale.order"].search([("partner_id","=",result.partner_id.id),("college","=",result.partner_id.college.id),("year","!=",result.partner_id.year.id),("level","=",result.partner_id.level)], limit=1)
        _logger.info("failed_student************11111111111111#####**%s" %failed_student)

        perviously_failed_student = self.env["sale.order"].search([("partner_id","=",result.partner_id.id),("state","!=",'cancel')])

        multi_level = perviously_failed_student.mapped("level")

        # multi_level.pop(0)
        student_id = 0

        duplicates = set([item for item in multi_level if multi_level.count(item) > 1])

        if duplicates:
            print(f"Duplicate values found: {duplicates}")
            _logger.info("duplicates@@@@@@@@@@%s" %duplicates)
        else:
            print("No duplicate values found")
            _logger.info("duplicates@@@@@@@@@@111111111%s" %duplicates)



        print("multi_level@@@@@@@@@@",result.contains_duplicate(multi_level))
        _logger.info("multi_level@@@@@@@@@@%s" %result.contains_duplicate(multi_level))
        if result.contains_duplicate(multi_level):
            _logger.info("multi_level@@@@@@@@@@11111111111111111%s" %result.contains_duplicate(multi_level))
            student_id = result.student.id
            if result.level in duplicates:
                if result.student.id == 11:
                    student_id = 16
                elif result.student.id == 55:
                    student_id = 55
                    result.installment_amount = 0
                    return result
                else:
                    student_id = 8
                _logger.info("result.level@@@@@@@@@@111111111%s" %result.level)    

            installmet_datsstd = result.env["installment.details"].search([('college' , '=', result.college.id),("level","=",'leve1'),("Subject","=",result.Subject),('department','=',result.department.id),('Student','=',student_id),('percentage_from','<=',result.partner_id.final_result),('percentage_to','>=',result.partner_id.final_result)])
            _logger.info("installmet_datsstd33333333333333@@@@@@@@@@%s" %installmet_datsstd)
            for years in installmet_datsstd:
                if years.year.year[-4:] == result.partner_id.year_of_acceptance_1.name[-4:]:
                    _logger.info("years.year.year[-4:]@@@@@@@@@@%s" %years.year.year[-4:])
                    print("years.year.year[-4:]@@@@@@@@@@@@@@@@",years.year.year[-4:])
                    result.installment_amount = years.installment

                    payemnt_date = installmet_dat.sale_installment_line_ids.mapped("payment_date")

                    
                    count_no = 0
                    for i in years.sale_installment_line_ids:
                        installment = result.sale_installment_line_ids.create({
                        'number' : i.number,
                        'payment_date' : payemnt_date[count_no] if payemnt_date else i.payment_date,
                        'amount_installment' : i.amount_installment,
                        'description': 'Installment Payment',
                        'sale_installment_id' : result.id,
                        })
                        count_no = count_no + 1  
        else:
            instamm_ment_details = self.env["installment.details"].search([('college','=',result.partner_id.college.id),("Student","=",result.student.id),("level","=",result.partner_id.level),('Subject','=',result.partner_id.shift),('year','=',result.partner_id.year.id),('department','=',result.partner_id.department.id),('percentage_from','<=',result.partner_id.final_result),('percentage_to','>=',result.partner_id.final_result)], limit=1)
            _logger.info("instamm_ment_details@@@@@@@@@@ %s" %instamm_ment_details)
            result.installment_amount = instamm_ment_details.installment
            for i in instamm_ment_details.sale_installment_line_ids:
                installment = result.sale_installment_line_ids.create({
                    'number' : i.number,
                    'payment_date' : i.payment_date,
                    'amount_installment' : i.amount_installment,
                    'description': 'Installment Payment',
                    'sale_installment_id' : result.id,
                    })
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

        if failed_student:
            result.installment_amount = failed_student.installment_amount
            payemnt_date = installmet_dat.sale_installment_line_ids.mapped("payment_date")

            for i in failed_student.sale_installment_line_ids:
                dates = payemnt_date
                target_date = i.payment_date
                differences = [abs(target_date - date) for date in dates]
                if differences:
                    nearest_index = differences.index(min(differences))
                    nearest_date = dates[nearest_index]
                    print(nearest_date)

                installment = result.sale_installment_line_ids.create({
                'number' : i.number,
                'payment_date' : nearest_date if nearest_date else i.payment_date,
                'amount_installment' : i.amount_installment,
                'description': 'Installment Payment',
                'sale_installment_id' : result.id,
                # "invoice_id" : invoice_id.id
                })  
                payemnt_date.remove(nearest_date)
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

        result.second_payment_date = datetime.today().date()
        order_line = result.env['sale.order.line'].create({
            'product_id': 1,
            'price_unit': result.installment_amount,
            'product_uom': result.env.ref('uom.product_uom_unit').id,
            'product_uom_qty': 1,
            'order_id': result._origin.id,
            'name': 'sales order line',
        })

        # if installmet_dat:
        #     print("sale_installment_line_ids########",installmet_dat.sale_installment_line_ids.ids)
        #     result.tenure_month = installmet_dat.installment_number
            # result.second_payment_date = datetime.today().date()
            # order_line = result.env['sale.order.line'].create({
            #     'product_id': 1,
            #     'price_unit': result.installment_amount,
            #     'product_uom': result.env.ref('uom.product_uom_unit').id,
            #     'product_uom_qty': 1,
            #     'order_id': result._origin.id,
            #     'name': 'sales order line',
            # })
            # if count == 0:
            #     result.amount = d.amount_installment
            #     count = count + 1

        return result


    # @api.onchange('partner_id')
    # def _compute_partner_id(self):
    #     if self.partner_id:
    #         # if self.partner_id.shift >=  cgpa.shift and self.partner_id.student_cgpa >=  cgpa.percentage_from and self.partner_id.student_cgpa <=  cgpa.percentage_to:
    #         instamm_ment_details = self.env["installment.details"].search([("student_dicount","=",True),('college','=',self.college.id),('Subject','=',self.partner_id.shift),('year','=',self.year.id),('department','=',self.department.id),('percentage_from','<=',self.partner_id.final_result),('percentage_to','>=',self.partner_id.final_result)])
    #         self.installment_amount = instamm_ment_details.installment
    #         if instamm_ment_details:
    #             for i in instamm_ment_details.sale_installment_line_ids:
    #                 sale_installment = self.sale_installment_line_ids.create({
    #                     'number' : i.number,
    #                     'payment_date' : i.payment_date,
    #                     'amount_installment' : i.amount_installment,
    #                     'description': 'Installment Payment',
    #                     'sale_installment_id' : result.id,
    #                     # "invoice_id" : invoice_id.id
    #                     })

    @api.onchange('partner_id', 'year')
    def ompute_partner_id(self):
        print("self.partner_id@@@@@@@@@@@@@@@",self.partner_id)
        if self.partner_id and self.year:
            self.Status = self.partner_id.Status
            self.transferred_to_us = self.partner_id.transferred_to_us
            self.transfer_shift = self.partner_id.transfer_shift
            duplicate_student = self.env["sale.order"].search([("partner_id","=",self.partner_id.id),("year","=",self.year.id)], limit=1)
            print("duplicate_student@@@@@@@@@@@@@@@@@@",duplicate_student)
            if duplicate_student:
                return {'warning': { 
                        'title': "Warning", 
                        'message': "يرجئ التاكد من عدم تكرار بطاقه التسجيل ", 
                        } 
                    }

class DataLevelValue(models.TransientModel):
    _name = 'exipire.value'
   
    date = fields.Date(string="Date")


    def action_confirm_change_exipire(self):
        for idds in self._context.get("active_id"):
            levels_sale_order = self.env["res.partner"].browse(int(idds))
            levels_sale_order.date_of_expiration = self.date



class ResPartnerSeq(models.Model):
    _inherit = "res.partner"

    student_cgpa = fields.Float("Student CGPA")

    

    def action_done_show_wizard_exipire(self):
        # for ddtsh in self:
        #     payment_first = self.env['account.payment'].search([("partner_id",'=',ddtsh.id)],order='id asc', limit=1)
        #     if payment_first:
        #         ddtsh.payment_number = payment_first.id
        print("self._context##################",self._context.get("active_ids"))
        return {'type': 'ir.actions.act_window',
        'name': _('Change the Expiration Date'),
        'res_model': 'exipire.value',
        'target': 'new',
        'view_id': self.env.ref('almaqal_student_discount.view_any_name_form_level_exipire').id,
        'view_mode': 'form',
        'context': {"active_id" : self._context.get("active_ids")}
        }    

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

    def excel_for_payemnt_records(self):  
        filename = 'جدول الاحصاء الصباحي.xls'
        string = 'جدول الاحصاء الصباحي.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string, cell_overwrite_ok=True)
        worksheet.cols_right_to_left = True
        header_bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")
        cell_format = xlwt.easyxf()
        filename = 'Student_Report_%s.xls' % date.today()
        rested = self.env['sale.order'].search([])
        row = 1
        border_normal = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; font: bold on; pattern: pattern solid, fore_colour gray25;')
        border_1 = xlwt.easyxf('borders: left 1, right 1, top 1, bottom 1;')
        border_2 = xlwt.easyxf('borders: left 2, right 2, top 2, bottom 2;')
        border_color_2 = xlwt.easyxf('borders: top_color blue, bottom_color blue, right_color blue, left_color blue, left 2, right 2, top 2, bottom 2; font: bold on; pattern: pattern solid, fore_colour gray25;')
        # worksheet.col(0).width = 10000
        # worksheet.col(1).width = 15000
        # worksheet.col(2).width = 10000
        worksheet.col(1).width = 5000
        worksheet.col(2).width = 5000
        worksheet.col(3).width = 5000
        worksheet.col(4).width = 5000
        worksheet.col(5).width = 5000

        header_bold = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour gray25; align: horiz centre; font: bold 1,height 240;")


        header_bold_main_header = xlwt.easyxf("font: bold on, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; align: horiz centre; align: vert centre")


        
        main_cell_total = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour ivory; align: horiz centre; align: vert centre")


        main_cell_total_of_total = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour lime; align: horiz centre; align: vert centre")
        tttyl = xlwt.easyxf("align: horiz centre; align: vert centre")

        row = 0
        col = 2
        count = 1
        
        worksheet.write(row, 0, 'التسلسل', header_bold) #sequence
        worksheet.write(row, 1, 'التاريخ', header_bold) #payment date
        worksheet.write(row, 2, 'رقم الوصل', header_bold) #payment number
        worksheet.write(row, 3, 'الاسم', header_bold) # Student Name
        worksheet.write(row, 4, 'المبلغ', header_bold) # total amout
        worksheet.write(row, 5, 'رقم الحساب', header_bold) # Account/invoice lines
        worksheet.write(row, 6, 'الحالة', header_bold) # Status

        thislist = []
        list_data_account_1 = 0
        list_data_account_2 = 0
        list_data_account_3 = 0
        list_data_account_4 = 0
        list_data_account_5 = 0
        list_data_account_6 = 0
        list_data_account_7 = 0
        list_data_account_8 = 0
        list_data_account_9 = 0
        list_data_account_10 = 0
        list_data_account_11 = 0

        account_with_code = []


        row = 1

        # print("selfWWWWWWWWWWWWWWWWWWWWWW",self.read_group([], ['payment_date'], ['payment_date']))
        # groups = self.read_group([], ['payment_date'], ['payment_date'])
        # for group in groups:
        #     print('>>>>>>', group)
        tota_of_amount = 0 
        total_of_amount_with_account_4395 = 0
        total_of_amount_with_account_4351 = 0
        date_check = ""
        payment_amount = 0
        name = ''
        totl_amount = 0
        for rest in self.sorted(key=lambda r: r.payment_date):
            
            # if rest.state == "cancelled":
            #     # _logger.info("rest.staterest.state1111111111111#####**%s" %rest.name)
            #     worksheet.write(row, 0, count,main_cell_total)
            #     worksheet.write(row, 1, rest.payment_date.strftime('%m/%d/%Y'),main_cell_total)
            #     worksheet.write(row, 2, rest.name,main_cell_total)
            #     worksheet.write(row, 3, rest.partner_id.name , main_cell_total)
            #     worksheet.write(row, 4, '', main_cell_total)
            #     worksheet.write(row, 5, '', main_cell_total)
            #     worksheet.write(row, 6, "ملغي", main_cell_total)
            #     # tota_of_amount = tota_of_amount + int(inv.amount_total)
            #     row = row + 1
            #     date_check = rest.payment_date
            #     count = count + 1

            if rest.reconciled_invoice_ids:
                payment_amount = rest.amount
                for inv in rest.reconciled_invoice_ids:
                    # _logger.info("nameeeeeee************11111111111111#####**%s" %rest.name)
                    # _logger.info("date_check@@@@************11111111111111#####**%s" %date_check)
                    if rest.payment_date ==  date_check or date_check == "" and rest.state == "posted":
                        worksheet.write(row, 0, count)

                        worksheet.write(row, 1, rest.payment_date.strftime('%m/%d/%Y'))
                        if name != rest.name:
                            worksheet.write(row, 2, rest.name)
                        else:
                            worksheet.write_merge(row - 1, row, 2, 2, rest.name, tttyl)

                        name = rest.name

                        # _logger.info("rest.reconciled_invoice_ids.invoice_payments_widget************11111111111111#####**%s" %inv.invoice_payments_widget)

                        for amont in json.loads(inv.invoice_payments_widget).get("content"):
                            if amont.get("account_payment_id") == rest.id:
                                totl_amount = amont.get("amount")

                        if rest.reconciled_invoices_count == 1:
                            totl_amount = rest.amount

                        

                        worksheet.write(row, 3, rest.partner_id.name)
                        worksheet.write(row, 4, '{:,}'.format(int(totl_amount)))
                        worksheet.write(row, 5, inv.invoice_line_ids.account_id.code + inv.invoice_line_ids.account_id.name)
                        worksheet.write(row, 6, 'مرحل')

                        # totl_amount = inv.amount_total
                        # if inv.amount_total > rest.amount:
                        #     totl_amount = rest.amount
                        # if inv.amount_total < rest.amount    
                        tota_of_amount = tota_of_amount + int(totl_amount)
                        row = row + 1
                        date_check = rest.payment_date
                        count = count + 1
                        if inv.invoice_line_ids.account_id.name not in thislist:
                            thislist.append(inv.invoice_line_ids.account_id.name)
                            account_with_code.append(inv.invoice_line_ids.account_id.display_name)

                        n = range(len(thislist))

                        thislist
                        _logger.info("thislistnnnnnnnnnnn11111111111111#####**%s" %thislist)
                        for i in n: 
                            _logger.info("iiiiiiiiiiiiiiiiiii3333333333333#####**%s" %i)
                            if (i) == 0 and inv.invoice_line_ids.account_id.name == thislist[0]:
                                list_data_account_1 = list_data_account_1 + totl_amount

                            if (i) == 1 and inv.invoice_line_ids.account_id.name == thislist[1]:
                                list_data_account_2 = list_data_account_2 + totl_amount 

                            if (i) == 2 and inv.invoice_line_ids.account_id.name == thislist[2]:
                                list_data_account_3 = list_data_account_3 + totl_amount

                            if (i) == 3 and inv.invoice_line_ids.account_id.name == thislist[3]:
                                list_data_account_4 = list_data_account_4 + totl_amount 

                            if (i) == 4 and thislist[4] and inv.invoice_line_ids.account_id.name == thislist[4]:
                                list_data_account_5 = list_data_account_5 + totl_amount   

                            if (i) == 5 and thislist[5] and inv.invoice_line_ids.account_id.name == thislist[5]:
                                list_data_account_6 = list_data_account_6 + totl_amount                    
                        
                    # if rest.payment_date !=  date_check or date_check != "" 
                    else:
                        worksheet.write_merge(row, row, 0, 3, "المجموع الكلي", header_bold)
                        worksheet.write(row, 4, '{:,}'.format(int(tota_of_amount)),header_bold)
                        tota_of_amount = 0
                        row = row + 2
                        date_check = ""
                        count = 1



                        worksheet.write(row, 0, count)

                        worksheet.write(row, 1, rest.payment_date.strftime('%m/%d/%Y'))
                        if name != rest.name:
                            worksheet.write(row, 2, rest.name)
                        else:
                            worksheet.write_merge(row - 1, row, 2, 2, rest.name, tttyl)

                        name = rest.name

                        for amont in json.loads(inv.invoice_payments_widget).get("content"):
                            if amont.get("account_payment_id") == rest.id:
                                totl_amount = amont.get("amount")

                        if rest.reconciled_invoices_count == 1:
                            totl_amount = rest.amount

                        worksheet.write(row, 3, rest.partner_id.name)
                        worksheet.write(row, 4, '{:,}'.format(int(totl_amount)))
                        worksheet.write(row, 5, inv.invoice_line_ids.account_id.code + inv.invoice_line_ids.account_id.name)
                        worksheet.write(row, 6, 'مرحل')


                        
                        # totl_amount = inv.amount_total
                        # if inv.amount_total > rest.amount:
                            # totl_amount = rest.amount
                        # if inv.amount_total < rest.amount    
                        tota_of_amount = tota_of_amount + int(totl_amount)
                        row = row + 1
                        date_check = rest.payment_date
                        count = count + 1
                        if inv.invoice_line_ids.account_id.name not in thislist:
                            thislist.append(inv.invoice_line_ids.account_id.name)
                            account_with_code.append(inv.invoice_line_ids.account_id.display_name)

                        n = range(len(thislist))
                        
                        _logger.info("thislistnnnnnnnnnnn2222222222222222222#####**%s" %thislist)
                        for i in n: 
                            _logger.info("iiiiiiiiiiiiiiiiiii#####**%s" %i)
                            if (i) == 0 and inv.invoice_line_ids.account_id.name == thislist[0]:
                                list_data_account_1 = list_data_account_1 + totl_amount

                            if (i) == 1 and inv.invoice_line_ids.account_id.name == thislist[1]:
                                list_data_account_2 = list_data_account_2 + totl_amount 

                            if (i) == 2 and inv.invoice_line_ids.account_id.name == thislist[2]:
                                list_data_account_3 = list_data_account_3 + totl_amount

                            if (i) == 3 and inv.invoice_line_ids.account_id.name == thislist[3]:
                                list_data_account_4 = list_data_account_4 + totl_amount 

                            if (i) == 4 and thislist[4] and inv.invoice_line_ids.account_id.name == thislist[4]:
                                list_data_account_5 = list_data_account_5 + totl_amount   

                            if (i) == 5 and thislist[5] and inv.invoice_line_ids.account_id.name == thislist[5]:
                                list_data_account_6 = list_data_account_6 + totl_amount                    
                        

                    payment_amount = payment_amount - totl_amount
                    # _logger.info("payment_amountpayment_amount************133333333333#####**%s" %payment_amount)

                    account_active = self.env["account.account"].search([('id','=',inv.invoice_line_ids.account_id.id)])
                    if account_active:
                        total_of_amount_with_account_4395 = total_of_amount_with_account_4395 + int(totl_amount)
                # if inv.invoice_line_ids.account_id.code == "4351":
                #     total_of_amount_with_account_4351 = total_of_amount_with_account_4351 + int(inv.amount_total)
                # _logger.info("payment_amount888888888888888888888888882#####**%s" %payment_amount)
                if payment_amount > 0:
                    worksheet.write(row, 0, count)

                    worksheet.write(row, 1, rest.payment_date.strftime('%m/%d/%Y'))
                    if name != rest.name:
                        worksheet.write(row, 2, rest.name)
                    else:
                        worksheet.write_merge(row - 1, row, 2, 2, rest.name, header_bold)

                    name = rest.name

                    worksheet.write(row, 3, rest.partner_id.name)
                    worksheet.write(row, 4, payment_amount)
                    worksheet.write(row, 5, " ")
                    worksheet.write(row, 6, 'مرحل')
                    tota_of_amount = tota_of_amount + int(payment_amount)
                    row = row + 1
                    date_check = rest.payment_date
                    count = count + 1
            if not rest.reconciled_invoice_ids:
                _logger.info("rest.staterest.222222222222222222222#####**%s" %rest.name)
                if rest.state == "posted" and rest.payment_date ==  date_check or date_check == "" :
                    print("rest.payment_date@@@@@@@@@@@@@@@",rest.payment_date)
                    worksheet.write(row, 0, count)

                    worksheet.write(row, 1, rest.payment_date.strftime('%m/%d/%Y'))
                    if name != rest.name:
                        worksheet.write(row, 2, rest.name)
                    else:
                        worksheet.write_merge(row - 1, row, 2, 2, rest.name, header_bold)

                    name = rest.name

                    worksheet.write(row, 3, rest.partner_id.name)
                    worksheet.write(row, 4, rest.amount)
                    worksheet.write(row, 5, " ")
                    worksheet.write(row, 6, 'مرحل')
                    tota_of_amount = tota_of_amount + int(rest.amount)
                    row = row + 1
                    date_check = rest.payment_date
                    count = count + 1
                elif  rest.state == "cancelled" and rest.payment_date ==  date_check or date_check == "":
                    worksheet.write(row, 0, count,main_cell_total)
                    worksheet.write(row, 1, rest.payment_date.strftime('%m/%d/%Y'),main_cell_total)
                    worksheet.write(row, 2, rest.name,main_cell_total)
                    worksheet.write(row, 3, rest.partner_id.name , main_cell_total)
                    worksheet.write(row, 4, '', main_cell_total)
                    worksheet.write(row, 5, '', main_cell_total)
                    worksheet.write(row, 6, "ملغي", main_cell_total)
                    # tota_of_amount = tota_of_amount + int(inv.amount_total)
                    row = row + 1
                    date_check = rest.payment_date
                    count = count + 1
                else:
                    worksheet.write_merge(row, row, 0, 3, "المجموع الكلي", header_bold)
                    worksheet.write(row, 4, '{:,}'.format(int(totl_amount)),header_bold)
                    tota_of_amount = 0
                    row = row + 2
                    date_check = ""
                    count = 1



                    worksheet.write(row, 0, count) 

                    worksheet.write(row, 1, rest.payment_date.strftime('%m/%d/%Y'))
                    if name != rest.name:
                        worksheet.write(row, 2, rest.name)
                    else:
                        worksheet.write_merge(row - 1, row, 2, 2, rest.name, tttyl)

                    name = rest.name

                    for amont in json.loads(inv.invoice_payments_widget).get("content"):
                        if amont.get("account_payment_id") == rest.id:
                            totl_amount = amont.get("amount")

                    if rest.reconciled_invoices_count == 1:
                        totl_amount = rest.amount

                    worksheet.write(row, 3, rest.partner_id.name)
                    worksheet.write(row, 4, '{:,}'.format(rest.amount))
                    worksheet.write(row, 5, inv.invoice_line_ids.account_id.code + inv.invoice_line_ids.account_id.name)
                    worksheet.write(row, 6, 'مرحل')


                    
                    # totl_amount = inv.amount_total
                    # if inv.amount_total > rest.amount:
                        # totl_amount = rest.amount
                    # if inv.amount_total < rest.amount    
                    tota_of_amount = tota_of_amount + int(totl_amount)
                    row = row + 1
                    date_check = rest.payment_date
                    count = count + 1
                    if inv.invoice_line_ids.account_id.name not in thislist:
                        thislist.append(inv.invoice_line_ids.account_id.name)
                        account_with_code.append(inv.invoice_line_ids.account_id.display_name)

                    n = range(len(thislist))
                    
                    _logger.info("thislistnnnnnnnnnnn2222222222222222222#####**%s" %thislist)
                    for i in n: 
                        _logger.info("iiiiiiiiiiiiiiiiiii#####**%s" %i)
                        if (i) == 0 and inv.invoice_line_ids.account_id.name == thislist[0]:
                            list_data_account_1 = list_data_account_1 + totl_amount

                        if (i) == 1 and inv.invoice_line_ids.account_id.name == thislist[1]:
                            list_data_account_2 = list_data_account_2 + totl_amount 

                        if (i) == 2 and inv.invoice_line_ids.account_id.name == thislist[2]:
                            list_data_account_3 = list_data_account_3 + totl_amount

                        if (i) == 3 and inv.invoice_line_ids.account_id.name == thislist[3]:
                            list_data_account_4 = list_data_account_4 + totl_amount 

                        if (i) == 4 and thislist[4] and inv.invoice_line_ids.account_id.name == thislist[4]:
                            list_data_account_5 = list_data_account_5 + totl_amount   

                        if (i) == 5 and thislist[5] and inv.invoice_line_ids.account_id.name == thislist[5]:
                            list_data_account_6 = list_data_account_6 + totl_amount                    
                    

                payment_amount = payment_amount - totl_amount
                # _logger.info("payment_amountpayment_amount************133333333333#####**%s" %payment_amount)

                account_active = self.env["account.account"].search([('id','=',inv.invoice_line_ids.account_id.id)])
                if account_active:
                    total_of_amount_with_account_4395 = total_of_amount_with_account_4395 + int(totl_amount)
    
        print("thislist@@@@@@@@@@@@@@",thislist)            
        worksheet.write_merge(row, row, 0, 3, "المجموع الكلي", header_bold)
        worksheet.write(row, 4, '{:,}'.format(int(tota_of_amount)))

        # row = row + 4

        # worksheet.write_merge(row, row, 0, 3, "ايراد خدمات تعليمية 4351", main_cell_total_of_total)

        # worksheet.write_merge(row + 1, row + 1, 0, 3, "أيراد رسوم اخرى 4395", main_cell_total_of_total)


        # worksheet.write(row, 4, '{:,}'.format(total_of_amount_with_account_4351), main_cell_total_of_total)
        row = row + 4
        if list_data_account_1 > 0:
            worksheet.write_merge(row, row, 0, 3, account_with_code[0], main_cell_total_of_total)
            worksheet.write(row, 4, '{:,}'.format(list_data_account_1), main_cell_total_of_total)
            row = row + 1

        if list_data_account_2 > 0:
            worksheet.write_merge(row, row, 0, 3, account_with_code[1], main_cell_total_of_total)
            worksheet.write(row, 4, '{:,}'.format(list_data_account_2), main_cell_total_of_total)
            row = row + 1

        if list_data_account_3 > 0:
            worksheet.write_merge(row, row, 0, 3, account_with_code[2], main_cell_total_of_total)
            worksheet.write(row, 4, '{:,}'.format(list_data_account_3), main_cell_total_of_total)
            row = row + 1

        if list_data_account_4 > 0:
            worksheet.write_merge(row, row, 0, 3, account_with_code[3], main_cell_total_of_total)
            worksheet.write(row, 4, '{:,}'.format(list_data_account_4), main_cell_total_of_total)
            row = row + 1

        if list_data_account_5 > 0:
            worksheet.write_merge(row, row, 0, 3, account_with_code[4], main_cell_total_of_total)
            worksheet.write(row, 4, '{:,}'.format(list_data_account_5), main_cell_total_of_total)
            row = row + 1

        if list_data_account_6 > 0:
            worksheet.write_merge(row, row, 0, 3, account_with_code[5], main_cell_total_of_total)
            worksheet.write(row, 4, '{:,}'.format(list_data_account_6), main_cell_total_of_total)
            row = row + 1


        _logger.info("list_data_account_111111111111111#####**%s" %list_data_account_1)
        _logger.info("list_data_account_222222222222222#####**%s" %list_data_account_2)
        _logger.info("list_data_account_33333333333333333333#####**%s" %list_data_account_3)
        _logger.info("list_data_account_4444444444444444444#####**%s" %list_data_account_4)    
        _logger.info("list_data_account_5555555555555555555#####**%s" %list_data_account_5)

        _logger.info("account_with_code66666666666666666666666#####**%s" %account_with_code)

        

                        



        fp = io.BytesIO()
        print("fp@@@@@@@@@@@@@@@@@@",fp)
        wb.save(fp)
        print(wb)
        out = base64.encodebytes(fp.getvalue())
        attachment = {
                       'name': str(filename),
                       'display_name': str(filename),
                       'datas': out,
                       'type': 'binary'
                   }
        ir_id = self.env['ir.attachment'].create(attachment) 
        print("ir_id@@@@@@@@@@@@@@@@",ir_id)

        xlDecoded = base64.b64decode(out)

        # file_added = "/home/anuj/Desktop/workspace13/Student_report.xlsx"
        # with open(file_added, "wb") as binary_file:
        #     binary_file.write(xlDecoded)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        download_url = '/web/content/' + str(ir_id.id) + '?download=true'
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }
        
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
