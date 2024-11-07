# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import pytz
import threading
from collections import OrderedDict, defaultdict
import re

from datetime import date, datetime, timedelta
from geopy.geocoders import Nominatim
import xml.dom.minidom
import calendar
from translate import Translator
import convert_numbers
from bs4 import BeautifulSoup
import re
from prettytable import PrettyTable
import pandas as pd
from dateutil.relativedelta import relativedelta

import base64
import xlwt
import io
from lxml import etree
import html2text

import requests
import json
from odoo import api, fields, models, tools, SUPERUSER_ID

_logger = logging.getLogger(__name__)

class techtime_payrollEmployee(models.Model):
    _inherit = 'hr.employee'

    first_field = fields.Char("Specialization")

    certificate_first = fields.Selection([
        ('certificate1', 'دكتوراه'),
        ('certificate2', 'ماجستير'),
        ('certificate3', 'دبلوم عالي'),
        ('certificate4', 'بكالوريوس'),
        ('certificate5', 'دبلوم معهد'),
        ('certificate6', 'اعدادية'),
        ('certificate7', 'دون الاعدادية')], string='Certificate')


class techtime_payrollDepartment(models.Model):
    _inherit = 'hr.department'
    _order = 'sequence'

    sequence = fields.Integer("Sequence")

class techtime_payrollDepartment(models.Model):
    _inherit = 'account.move'

    year = fields.Many2one("year.year", string="Year")
    Status = fields.Selection([('status4', 'مؤجل'),('status1','ترقين قيد'),('status2','طالب غير مباشر'),('status3','انسحاب'),('currecnt_student','Current student'),('succeeded','Succeeded'),('failed','Falied'),('transferred_from_us','Transferred From Us'),('graduated','Graduated')], string="Status", related="partner_id.Status")

    def send_mis_report_for_department_new_data_level(self):
        filename = 'Department_level.xls'
        string = 'Department_level_report.xls'
        wb = xlwt.Workbook(encoding='utf-8')

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
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour ivory; align: horiz centre")


        main_cell_total_of_total = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour lime; align: horiz centre")


        header_bold_extra_tag = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour green; font: color white; align: horiz centre")

        header_bold_extra = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour red; font: color white; align: horiz centre")
        cell_format = xlwt.easyxf()
        filename = 'Department_level_Report_%s.xls' % date.today()

        main_cell = xlwt.easyxf('font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; align: horiz centre; font: bold 1,height 240;')
        

        row = 1
        call = 1

        department_data = self.env["department.department"].search([])
        level_name = ""
        for depp in  department_data:
            row = 2

            invoice_data_department_total = self.filtered(lambda picking: picking.department.id == depp.id and picking.state == "posted" and picking.amount_residual > 50000)


            worksheet = wb.add_sheet(depp.department,  cell_overwrite_ok=True)

            worksheet.col(0).width = 4500
            worksheet.col(2).width = 5500
            worksheet.col(3).width = 7500
            worksheet.col(4).width = 7500

            worksheet.cols_right_to_left = True

            level_data = ["leve1","level2", "level3", "level4", "level5"]

            # worksheet.write(row - 1, 0, depp.department, header_bold)
            worksheet.write_merge(row - 2, row - 2, 0, 3, date.today().strftime('%m/%d/%Y'), header_bold)

            worksheet.write_merge(row - 1, row - 1, 0, 3, depp.department  + "(" + str(len(invoice_data_department_total.mapped("id"))) + ")", header_bold)

            worksheet.write(row, 1, 'التسلسل', header_bold)

            worksheet.write(row, 2, 'رقم الفاتورة', header_bold)

            worksheet.write(row, 3, 'أسم الطالب', header_bold)

            worksheet.write(row, 4, 'حالة الطالب', header_bold)

            row = 3
            for level in level_data:

                if level == "leve1":
                    level_name = "المرحلة الاولى"
                if level == "level2":
                    level_name = "المرحلة الثانية"
                if level == "level3": 
                    level_name = "المرحلة الثالثة"
                if level == "level4":
                    level_name = "المرحلة الرابعة"
                if level == "level5":
                    level_name = "المرحلة الخامسة"

                

                print("level@@@@@@@@@@@@@",level)
                print("self$$$$$$$$$$$$$",self)

                status_data = ['currecnt_student','status1','status4','status2','status3','succeeded','failed','transferred_from_us','graduated']
                for status in status_data:
                    invoice_data = self.filtered(lambda picking: picking.partner_id.Status == status and  picking.department.id == depp.id and picking.state == "posted" and picking.amount_residual > 50000 and picking.level == level).sorted(key=lambda r: r.partner_id.name)
                    
                    sequence = 1

                    if invoice_data:
                        worksheet.write(row - 1, 0, level_name   + "(" + str(len(invoice_data.mapped("id"))) + ")" , header_bold)
                        for inv in invoice_data:
                            print("inhhhhhhhhhhhhhhhhhhh",inv.partner_id.name)
                            print("row@@@@@@@@@@@@@@wwwwwwwwww",row)
                            worksheet.write(row, 1, sequence, main_cell)

                            worksheet.write(row, 2, inv.name, main_cell)

                            worksheet.write(row, 3, inv.partner_id.name, main_cell)

                            status_data = ""

                            if status == "currecnt_student":
                                status_data  = "طالب حالي"
                            if status == "status1":
                                status_data  = "ترقين قيد"

                            if status == "status4":
                                status_data  = "مؤجل"
                                
                            if status == "status2":
                                status_data  = "طالب غير مباشر"
                            
                            if status == "status3":
                                status_data  = "انسحاب"

                            if status == "succeeded":
                                status_data  = "طالب ناجح"
                                
                            if status == "failed":
                                status_data  = "طالب راسب"
                                
                            if status == "transferred_from_us":
                                status_data  = "طالب منتقل من الجامعة"     

                            if status == "graduated":
                                status_data  = "طالب ناجح"                            

                            worksheet.write(row, 4, status_data, main_cell)

                            row = row + 1
                            print("row@@@@@@@@@@@@@@eeeeeeeeee",row)
                            sequence = sequence + 1
                        row = row + 3    
                        

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

        # file_added = "/home/anuj/Desktop/workspace13/payslip_report.xlsx"
        # with open(file_added, "wb") as binary_file:
        #     binary_file.write(xlDecoded)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        download_url = '/web/content/' + str(ir_id.id) + '?download=true'
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        } 


    
    def send_mis_report_for_department_new_data_level_without_fifty(self):
        filename = 'Department_level.xls'
        string = 'Department_level_report.xls'
        wb = xlwt.Workbook(encoding='utf-8')

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
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour ivory; align: horiz centre")


        main_cell_total_of_total = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour lime; align: horiz centre")


        header_bold_extra_tag = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour white; font: color white; align: horiz centre")

        header_bold_extra = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour red; font: color white; align: horiz centre")
        cell_format = xlwt.easyxf()
        filename = 'Department_level_Report_%s.xls' % date.today()

        main_cell = xlwt.easyxf('font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; align: horiz centre; font: bold 1,height 240;')
        

        row = 1
        call = 1

        department_data = self.env["department.department"].search([])
        level_name = ""
        for depp in  department_data:
            row = 2

            invoice_data_department_total = self.filtered(lambda picking: picking.department.id == depp.id and picking.state == "posted" and picking.invoice_payment_state != 'paid')


            worksheet = wb.add_sheet(depp.department,  cell_overwrite_ok=True)

            worksheet.col(0).width = 4500
            worksheet.col(2).width = 5500
            worksheet.col(3).width = 7500
            worksheet.col(4).width = 7500

            worksheet.cols_right_to_left = True

            level_data = ["leve1","level2", "level3", "level4", "level5"]

            # worksheet.write(row - 1, 0, depp.department, header_bold)
            worksheet.write_merge(row - 2, row - 2, 0, 3, date.today().strftime('%m/%d/%Y'), header_bold)

            worksheet.write_merge(row - 1, row - 1, 0, 3, depp.department  + "(" + str(len(invoice_data_department_total.mapped("id"))) + ")", header_bold)

            worksheet.write(row, 1, 'التسلسل', header_bold)

            worksheet.write(row, 2, 'رقم الفاتورة', header_bold)

            worksheet.write(row, 3, 'أسم الطالب', header_bold)

            worksheet.write(row, 4, 'حالة الطالب', header_bold)

            worksheet.write(row, 5, 'المبلغ المتبقي', header_bold)

            row = 3
            for level in level_data:
                if level == "leve1":
                    level_name = "المرحلة الاولى"
                if level == "level2":
                    level_name = "المرحلة الثانية"
                if level == "level3": 
                    level_name = "المرحلة الثالثة"
                if level == "level4":
                    level_name = "المرحلة الرابعة"
                if level == "level5":
                    level_name = "المرحلة الخامسة"
                print("level@@@@@@@@@@@@@",level)
                print("self$$$$$$$$$$$$$",self)
                status_data = ['currecnt_student','status1','status2','status4','status3','succeeded','failed','transferred_from_us','graduated']
                for status in status_data:
                    if status == "currecnt_student":
                        status_data  = "طالب حالي"

                    if status == "status1":
                        status_data  = "ترقين قيد"
                        main_cell = xlwt.easyxf('font: bold off, color black;\
                         borders: top_color black, bottom_color black, right_color black, left_color black,\
                                  left thin, right thin, top thin, bottom thin;\
                         pattern: pattern solid, fore_color yellow; align: horiz centre; font: bold 1,height 240;')
                    if status == "status2":
                        status_data  = "طالب غير مباشر"

                    if status == "status4":
                        status_data  = "مؤجل"    
                    
                    if status == "status3":
                        status_data  = "انسحاب"

                    if status == "succeeded":
                        status_data  = "طالب ناجح"
                        main_cell = xlwt.easyxf('font: bold off, color black;\
                         borders: top_color black, bottom_color black, right_color black, left_color black,\
                                  left thin, right thin, top thin, bottom thin;\
                         pattern: pattern solid, fore_color white; align: horiz centre; font: bold 1,height 240;')
                        
                    if status == "failed":
                        status_data  = "طالب راسب"
                        main_cell = xlwt.easyxf('font: bold off, color black;\
                         borders: top_color black, bottom_color black, right_color black, left_color black,\
                                  left thin, right thin, top thin, bottom thin;\
                         pattern: pattern solid, fore_color red; align: horiz centre; font: bold 1,height 240;')
                        
                    if status == "transferred_from_us":
                        status_data  = "طالب منتقل من الجامعة"     

                    if status == "graduated":
                        status_data  = "طالب ناجح"       
                        main_cell = xlwt.easyxf('font: bold off, color black;\
                         borders: top_color black, bottom_color black, right_color black, left_color black,\
                                  left thin, right thin, top thin, bottom thin;\
                         pattern: pattern solid, fore_color white; align: horiz centre; font: bold 1,height 240;')
                    invoice_data = self.filtered(lambda picking: picking.partner_id.Status == status and  picking.department.id == depp.id and picking.state == "posted" and picking.level == level and picking.invoice_payment_state != 'paid').sorted(key=lambda r: r.partner_id.name)
                
                    sequence = 1

                    if invoice_data:
                        worksheet.write(row - 1, 0, level_name   + "(" + str(len(invoice_data.mapped("id"))) + ")" , header_bold)
                        for inv in invoice_data:
                            print("inhhhhhhhhhhhhhhhhhhh",inv.partner_id.name)
                            print("row@@@@@@@@@@@@@@wwwwwwwwww",row)
                            worksheet.write(row, 1, sequence, main_cell)

                            worksheet.write(row, 2, inv.name, main_cell)

                            worksheet.write(row, 3, inv.partner_id.name, main_cell)

                            status_data = ""

                            if status == "currecnt_student":
                                status_data  = "طالب حالي"
                            if status == "status1":
                                status_data  = "ترقين قيد"
                            if status == "status2":
                                status_data  = "طالب غير مباشر"

                            if status == "status4":
                                status_data  = "مؤجل"    
                            
                            if status == "status3":
                                status_data  = "انسحاب"

                            if status == "succeeded":
                                status_data  = "طالب ناجح"
                                
                            if status == "failed":
                                status_data  = "طالب راسب"
                                
                            if status == "transferred_from_us":
                                status_data  = "طالب منتقل من الجامعة"     

                            if status == "graduated":
                                status_data  = "طالب ناجح"                            

                            worksheet.write(row, 4, status_data, main_cell)

                            worksheet.write(row, 5, inv.amount_residual, main_cell)

                            row = row + 1
                            print("row@@@@@@@@@@@@@@eeeeeeeeee",row)
                            sequence = sequence + 1
                        row = row + 3    
                        

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

        # file_added = "/home/anuj/Desktop/workspace13/payslip_report.xlsx"
        # with open(file_added, "wb") as binary_file:
        #     binary_file.write(xlDecoded)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        download_url = '/web/content/' + str(ir_id.id) + '?download=true'
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }        


    def send_mis_report_for_department_new_sheet(self):
        filename = 'Department.xls'
        string = 'Department_report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string)
        header_bold = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour gray25;")
        cell_format = xlwt.easyxf()
        filename = 'Department_Report_%s.xls' % date.today()
        rested = self.env['account.move'].search([])
        row = 2

        header_bold_extra_tag = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour green;")

        header_bold_extra = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour red;")

        main_cell_total_of_total = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour lime;")

        main_cell = xlwt.easyxf('font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; ')
        border_normal = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; font: bold on; pattern: pattern solid, fore_colour gray25;')
        border_1 = xlwt.easyxf('borders: left 1, right 1, top 1, bottom 1;')
        border_2 = xlwt.easyxf('borders: left 2, right 2, top 2, bottom 2;')
        border_color_2 = xlwt.easyxf('borders: top_color blue, bottom_color blue, right_color blue, left_color blue, left 2, right 2, top 2, bottom 2; font: bold on; pattern: pattern solid, fore_colour gray25;')
        worksheet.col(0).width = 7000
        worksheet.col(1).width = 4000
        worksheet.col(2).width = 4000

        worksheet.col(3).width = 4000
        worksheet.col(4).width = 4000
        worksheet.col(5).width = 4000
        worksheet.col(6).width = 4000

        department_data = self.env["department.department"].search([])
        employe_data = 0
        call = 1


        worksheet.write(call, 0, 'القسم', header_bold) #day deduction
        worksheet.write(call, 1, 'العدد الكلي ', header_bold) #day deduction amount

        worksheet.write(call, 2, 'مسددي القسط الأول 50%', header_bold) # wage

        worksheet.write(call, 3, 'مسددي القسط الثاني 25%', header_bold) #basic salary


        # worksheet.write(call, 4, 'Wage -الراتب الاسميUSD', header_bold)
        worksheet.write(call, 4, 'مسددي القسط الثالث 25% ', header_bold) #compensation

        worksheet.write(call, 5, 'الفرق بين العدد الكلي والمسجلين في القسط الأول ', header_bold) #allowance


        call = 2
        total_od_all = 0
        total_of_first = 0
        total_of_second = 0
        total_of_third = 0
        total_of_credit = 0
        for depp in  department_data:
            value_first_paid_invoice = 0
            invoices_paid_1 = self.env['account.move'].search([("department","=",depp.id),("invoice_origin","!=",False),("invoice_payment_state","=","paid")]).filtered(lambda picking: picking.account_installment_line_ids.number == 1)
            invoices_paid_2 = self.env['account.move'].search([("department","=",depp.id),("invoice_origin","!=",False),("invoice_payment_state","=","paid")]).filtered(lambda picking: picking.account_installment_line_ids.number == 2)
            invoices_paid_3 = self.env['account.move'].search([("department","=",depp.id),("invoice_origin","!=",False),("invoice_payment_state","=","paid")]).filtered(lambda picking: picking.account_installment_line_ids.number == 3)


            total_student = self.env["res.partner"].search([("department","=",depp.id)])

            total_credit = self.env["sale.order"].search(['|',("Status","=","status1"),("Status","=","status3"),("department","=",depp.id)])


            worksheet.write(call, 0, depp.department, main_cell)


            worksheet.write(call, 1, len(total_student.mapped("id")), main_cell) # employee

            total_od_all = total_od_all + len(total_student.mapped("id"))



            worksheet.write(call, 2, len(invoices_paid_1.mapped("id")), main_cell) # employee type

            total_of_first = total_of_first + len(invoices_paid_1.mapped("id"))


            worksheet.write(call, 3, len(invoices_paid_2.mapped("id")), main_cell) # certifiactae

            total_of_second = total_of_second + len(invoices_paid_2.mapped("id"))

            worksheet.write(call, 4, len(invoices_paid_3.mapped("id")), main_cell) # description

            total_of_third = total_of_third + len(invoices_paid_3.mapped("id"))


            worksheet.write(call, 5, len(total_credit.mapped("id")), main_cell)

            total_of_credit = total_of_credit + len(total_credit.mapped("id"))

            call  = call + 1


        worksheet.write(call + 1, 1, total_od_all, main_cell) # employee

        worksheet.write(call + 1, 2, total_of_first, main_cell) # employee type

        worksheet.write(call + 1, 3, total_of_second, main_cell) # certifiactae

        worksheet.write(call + 1, 4, total_of_third, main_cell) # description


        worksheet.write(call + 1, 5, total_of_credit, main_cell)    

        worksheet.write_merge(call + 3, call + 3, 0, 5, 'ملاحظة: الاعداد الموجودة في الحقل الأخير (الفرق) السبب في هذا الفرق بالعدد بين العدد الكلي للطلاب وعدد المسددين للدفعة الأولى هو ان بعض الطلبة سدد قسط وانتقل او انسحب او تم ترقين قيده', main_cell)


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

        # file_added = "/home/anuj/Desktop/workspace13/payslip_report.xlsx"
        # with open(file_added, "wb") as binary_file:
        #     binary_file.write(xlDecoded)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        download_url = '/web/content/' + str(ir_id.id) + '?download=true'
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }    


class TechAccount(models.Model):
    _inherit = 'account.move.line'

    balanace = fields.Float("Balance")    

    @api.onchange('credit','debit')
    def _inverse_balanace(self):
        for ffts in self:
            ffts.balanace = ffts.credit - ffts.debit





class techtime_payroll_excel(models.Model):
    _inherit = 'hr.payslip'
#     _description = 'techtime_payroll_excel.techtime_payroll_excel'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#hr.payslip
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

    def send_mis_report_techtime_data(self):
        filename = 'Payslip.xls'
        string = 'Payslip_report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string)
        header_bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")
        cell_format = xlwt.easyxf()
        filename = 'Payslip_Report_%s.xls' % date.today()
        rested = self.env['hr.payslip'].search([])
        row = 1
        border_normal = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; font: bold on; pattern: pattern solid, fore_colour gray25;')
        border_1 = xlwt.easyxf('borders: left 1, right 1, top 1, bottom 1;')
        border_2 = xlwt.easyxf('borders: left 2, right 2, top 2, bottom 2;')
        border_color_2 = xlwt.easyxf('borders: top_color blue, bottom_color blue, right_color blue, left_color blue, left 2, right 2, top 2, bottom 2; font: bold on; pattern: pattern solid, fore_colour gray25;')
        worksheet.col(0).width = 10000
        worksheet.col(1).width = 15000
        worksheet.col(2).width = 10000
        worksheet.row(0).height = 500
                   


        worksheet.write(0, 0, 'Payslip Name', border_color_2)
        worksheet.write(0, 1, 'Employee Name', border_color_2)
        worksheet.write(0, 2, 'Date From', border_color_2)
        worksheet.write(0, 3, 'Date To', header_bold)

        worksheet.write(0, 4, 'الراتب الكلي', header_bold)
        worksheet.write(0, 5, 'الراتب الاسمي1', header_bold)
        worksheet.write(0, 6, 'التعويضية1', header_bold)
        worksheet.write(0, 7, 'مجموع الاسمي والتعويضية', header_bold)
        worksheet.write(0, 8, 'الضريبة', header_bold)
        worksheet.write(0, 9, 'عدد الايام المستقطعة', header_bold)
        worksheet.write(0, 10, 'مبلغ الايام المستقطعة', header_bold)
        worksheet.write(0, 11, 'الضمان الاجتماعي', header_bold)
        worksheet.write(0, 12, 'التدريب والتأهيل', header_bold)
        worksheet.write(0, 13, 'مجموع الاستقطاعات', header_bold)
        worksheet.write(0, 14, 'صافي الراتب1', header_bold)
        # v.onboard_date >= (datetime.today().date().replace(day=1) - relativedelta(months=1)) and v.onboard_date <= (datetime.today().date() - relativedelta(months=1))
        for material_line_id in self:
            worksheet.write(row, 0, material_line_id.name or '')
            worksheet.write(row, 1, material_line_id.employee_id.name or '')
            worksheet.write(row, 2, material_line_id.date_from.strftime('%m/%d/%Y') or '')
            worksheet.write(row, 3, material_line_id.date_to.strftime('%m/%d/%Y') or '')

            for iit in material_line_id.line_ids:
                if iit.code == "WAGE":
                    worksheet.write(row, 4, iit.total or '')

                if iit.code == "BSCC":
                    worksheet.write(row, 5, iit.total or '')

                if iit.code == "CMPS":
                    worksheet.write(row, 6, iit.total or '')
                if iit.code == "WAG":
                    worksheet.write(row, 7, iit.total or '')
                if iit.code == "TAX":    
                    worksheet.write(row, 8, iit.total or '')
                if iit.code == "day2":    
                    worksheet.write(row, 9, iit.total or '')
                if iit.code == "DDTA":
                    worksheet.write(row, 10, iit.total or '')
                if iit.code == "SST":    
                    worksheet.write(row, 11, iit.total or '')
                if iit.code == "TRA":    
                    worksheet.write(row, 12, iit.total or '')
                if iit.code == "TTD":    
                    worksheet.write(row, 13, iit.total or '')
                if iit.code == "NTS":    
                    worksheet.write(row, 14, iit.total or '')    
            row += 1
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

        # file_added = "/home/anuj/Desktop/workspace13/payslip_report.xlsx"
        # with open(file_added, "wb") as binary_file:
        #     binary_file.write(xlDecoded)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        download_url = '/web/content/' + str(ir_id.id) + '?download=true'
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }        

        # df = pd.export_excel (r'/home/anuj/Desktop/workspace13/payslip_report.xlsx')
        # print (df)              


    def compute_sheet(self):
        for payslip in self:
            number = payslip.number or self.env["ir.sequence"].next_by_code(
                "salary.slip"
            )
            # delete old payslip lines
            payslip.line_ids.unlink()

            # set the list of contract for which the rules have to be applied
            # if we don't give the contract, then the rules to apply should be
            # for all current contracts of the employee
            contract_ids = payslip.contract_id.ids or self.get_contract(
                payslip.employee_id, payslip.date_from, payslip.date_to
            )
            lines = [
                (0, 0, line)
                for line in self._get_payslip_lines(contract_ids, payslip.id)
            ]
            payslip.write({"line_ids": lines, "number": number})
        # return payslip


    def send_mis_report_for_department(self):
        filename = 'Department.xls'
        string = 'Department_report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string)
        header_bold = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour gray25;")
        cell_format = xlwt.easyxf()
        filename = 'Department_Report_%s.xls' % date.today()
        rested = self.env['hr.payslip'].search([])
        row = 2

        header_bold_extra_tag = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour green; font: color white; align: horiz centre")

        header_bold_extra = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour red; font: color white; align: horiz centre")

        main_cell_total_of_total = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour lime;")

        main_cell = xlwt.easyxf('font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; ')
        border_normal = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; font: bold on; pattern: pattern solid, fore_colour gray25;')
        border_1 = xlwt.easyxf('borders: left 1, right 1, top 1, bottom 1;')
        border_2 = xlwt.easyxf('borders: left 2, right 2, top 2, bottom 2;')
        border_color_2 = xlwt.easyxf('borders: top_color blue, bottom_color blue, right_color blue, left_color blue, left 2, right 2, top 2, bottom 2; font: bold on; pattern: pattern solid, fore_colour gray25;')
        worksheet.col(0).width = 7000
        worksheet.col(1).width = 4000
        worksheet.col(2).width = 4000

        worksheet.col(3).width = 4000
        worksheet.col(4).width = 4000
        worksheet.col(5).width = 4000
        worksheet.col(6).width = 4000
        worksheet.col(7).width = 4000
        worksheet.col(8).width = 4000
        worksheet.col(9).width = 4000
        worksheet.col(10).width = 4000
        worksheet.col(11).width = 4000
        worksheet.col(12).width = 4000
        worksheet.col(13).width = 4000
        worksheet.col(14).width = 4000
        worksheet.col(15).width = 4000
        worksheet.col(16).width = 4000
        worksheet.col(17).width = 4000
        worksheet.col(18).width = 4000
        worksheet.col(19).width = 4000
        day_deduction_every_thing_total = 0
        day_deduction_amount_every_thing_total = 0
        total_wage_every_thing_total = 0
        total_basic_every_thing_total = 0
        compensation_every_thing_total = 0
        allowance_every_thing_total = 0
        total_day_all_every_thing_total = 0
        total_aeaa_every_thing_total = 0
        total_entitlements_every_thing_total = 0
        socailsecurity_every_thing_total = 0
        tax_every_thing_total = 0
        reded_every_thing_total = 0
        basded_every_thing_total = 0
        total_ded_every_thing_total = 0
        total_ded1_every_thing_total = 0
        total_ded2_every_thing_total = 0
        net_saled_every_thing_total = 0

        department_data = self.env["hr.department"].search([("parent_id",'=',False)])
        employe_data = 0
        call = 1

        worksheet.write_merge(call - 1, call - 1, 4, 9, 'المستحقات', header_bold_extra_tag)
        worksheet.write_merge(call - 1, call - 1, 10, 16, 'الاستقطاعات', header_bold_extra)

        worksheet.write(call, 1, 'عدد الايام المستقطعة', header_bold) #day deduction
        worksheet.write(call, 2, 'مبلغ الايام المستقطعة', header_bold) #day deduction amount

        worksheet.write(call, 3, 'الراتب الكلي', header_bold) # wage

        worksheet.write(call, 4, 'الراتب الاسمي', header_bold) #basic salary


        # worksheet.write(call, 4, 'Wage -الراتب الاسميUSD', header_bold)
        worksheet.write(call, 5, 'التعويضية', header_bold) #compensation

        worksheet.write(call, 6, 'التدريب والتأهيل', header_bold) #allowance

        worksheet.write(call, 7, 'مكافأت غير العاملين', header_bold) #allowance
        worksheet.write(call, 8, 'الاعانات', header_bold) #allowance

        worksheet.write(call, 9, 'مجموع الاستحقاقات', header_bold) #allowance

        

        # worksheet.write(call, 7, 'Basic', header_bold)
        worksheet.write(call, 10, 'الضمان الاجتماعي', header_bold) #socaial security
        worksheet.write(call, 11, 'الضريبة', header_bold) #tax
        


        
        worksheet.write(call, 12, 'استقطاع التقاعد', header_bold) #REDED
        worksheet.write(call, 13, 'استقطاعات جامعة البصرة ل I2', header_bold) #BASDED
        worksheet.write(call, 14, 'مجموع الاستقطاعات', header_bold) #total deduction

        worksheet.write(call, 15, 'م.تنفيذ البصره', header_bold) #total deduction
        worksheet.write(call, 16, 'استقطاع ايراد سلف', header_bold) #total deduction

        worksheet.write(call, 17, 'صافي الراتب', header_bold) # Net Salary
        for depp in  department_data:
            # print("depdepdepdepdepdepdepdepdepdepdep",dep.id)
            
            # print("rested##########################",rested)
            # worksheet.write(call, 0, depp.name, border_color_2)

            # worksheet.write(call, 1, 'رقم القصاصة', border_color_2)  # refernce 
            # # worksheet.write(call, 1, 'Payslip Name', border_color_2)

            # worksheet.write(call, 2, 'اسم الموظف', border_color_2) # employee


            # worksheet.write(call, 3, 'نوع الخدمة', border_color_2) # employee type

            # worksheet.write(call, 4, 'نوع الشهادة', border_color_2) # certifiactae



            # worksheet.write(call, 5, 'التفاصيل', header_bold) # description


            print("department_data#############",depp.id)
            print("parent_id$$$$$$$$$$$$$$$$$",depp.parent_id)

            partner_data = self.env["hr.department"].search([("parent_id",'=',depp.id)])
            print("depp###############",partner_data.mapped('id') + [depp.id])

            all_ids = [depp.id] + partner_data.mapped('id') 

            print("all_ids@@@@@@@@@@@@@@",all_ids)

            
            # partner_data = (4, depp.id)
            print("partner_data@@@@@@@@@@@@@",partner_data)
            day_deduction_total = 0
            total_basic_total = 0 
            total_wage_total = 0
            compensation_total = 0
            tax_total = 0
            day_deduction_total = 0
            day_deduction_amount_total = 0
            socailsecurity_total = 0
            allowance_total = 0
            reded_total = 0
            basded_total = 0
            total_ded_total = 0
            total_ded1_total = 0
            total_ded2_total = 0
            net_saled_total = 0
            total_day_all_total = 0
            total_aeaa_total = 0
            total_entitlements_total = 0
            certificate_total = 0
            for values_data in all_ids:
                dep = self.env["hr.department"].search([('id','=',values_data)])
                print("prixxxxxxxxxxxxxxxxxxxxxxx",self)
                # rested = self.env['hr.payslip'].search([('department','=',dep.id)])
                rested = self.filtered(lambda picking: picking.employee_id.department_id.id == dep.id)
                # v.onboard_date >= (datetime.today().date().replace(day=1) - relativedelta(months=1)) and v.onboard_date <= (datetime.today().date() - relativedelta(months=1))
                total_basic = 0 
                total_wage_data = 0
                compensation_data = 0
                tax_data = 0
                day_deduction_data = 0
                day_deduction_amount_data = 0
                socailsecurity_data = 0
                allowance_data = 0
                reded = 0
                basded = 0
                total_ded_data = 0
                total_ded1_data = 0
                total_ded2_data = 0
                net_saled_data = 0
                total_day_all_data = 0
                total_aeaa_data = 0
                total_entitlements_data = 0
                certificate_data = 0
                sequence = 1
                for material_line_id in rested:
                    # worksheet.write(row, 0, sequence or '')
                    # worksheet.write(row, 1, material_line_id.number or '')
                    # worksheet.write(row, 1, material_line_id.name or '')

                    # worksheet.write(row, 2, material_line_id.employee_id.name or '')

                    if material_line_id.contract_id.employ_type == 'option1':
                        employe_data = 'تعيين - متقاعد'
                    if material_line_id.contract_id.employ_type == 'option2':
                        employe_data = 'تعيين - غير متقاعد مشمول بالضمان'
                    if material_line_id.contract_id.employ_type == 'option3':
                        employe_data = 'اعارة'
                    if material_line_id.contract_id.employ_type == 'option4':
                        employe_data = 'محاضر خارجي'
                    if material_line_id.contract_id.employ_type == 'option5':
                        employe_data = 'اجر يومي'

                    # worksheet.write(row, 3, employe_data or '')


                    if material_line_id.employee_id.certificate_first == 'certificate1': 
                        certificate_data  = 'دكتوراه'
                    if material_line_id.employee_id.certificate_first == 'certificate2': 
                        certificate_data  = 'ماجستير'
                    if material_line_id.employee_id.certificate_first == 'certificate3': 
                        certificate_data  = 'دبلوم عالي'
                    if material_line_id.employee_id.certificate_first == 'certificate4': 
                        certificate_data  = 'بكالوريوس'
                    if material_line_id.employee_id.certificate_first == 'certificate5': 
                        certificate_data  = 'دبلوم معهد'
                    if material_line_id.employee_id.certificate_first == 'certificate6': 
                        certificate_data  = 'اعدادية'
                    if material_line_id.employee_id.certificate_first == 'certificate7': 
                        certificate_data  = 'دون الاعدادية'

                    # worksheet.write(row, 4, certificate_data or '')

                    


                    # worksheet.write(row, 5, re.sub('<[^>]*>', '', material_line_id.description) or '')

                    # worksheet.write(row, 6, "{:,.2f}".format(float(material_line_id.contract_id.day_deduction)) or '')

                    day_deduction_data = day_deduction_data + material_line_id.contract_id.day_deduction
                    # day_deduction_total = day_deduction_total + material_line_id.contract_id.day_deduction

                    # worksheet.write(row, 7, "{:,.2f}".format(float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction))) or '') 

                    day_deduction_amount_data = day_deduction_amount_data + float((((material_line_id.contract_id.wage + material_line_id.contract_id.training_field) / 30) * material_line_id.contract_id.day_deduction))
                    # day_deduction_amount_total = day_deduction_amount_total + float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction))
                          

                    # if material_line_id.contract_id.currency_id.id == 2:
                    #     worksheet.write(row, 4, str(material_line_id.contract_id.wage) + "$" or '')

                    # if material_line_id.contract_id.currency_id.id == 90:
                    # worksheet.write(row, 8, "{:,.2f}".format(float(material_line_id.contract_id.wage) + float(material_line_id.contract_id.training_field)) + "ع.د" or '')
                    total_wage_data = total_wage_data + (float(material_line_id.contract_id.wage) + float(material_line_id.contract_id.training_field))
                    # total_wage_total = total_wage_total + (float(material_line_id.contract_id.wage) + float(material_line_id.contract_id.training_field))
                    total_ent = 0
                    total_comp_ent = 0
                    total_all_ent = 0
                    total_all_day_all = 0
                    total_all_aeaa = 0
                    for iit in material_line_id.line_ids:
                        if iit.code == "BSCC":
                            # worksheet.write(row, 9, "{:,.2f}".format(float(iit.total)) or '')
                            total_basic = total_basic + iit.total
                            # total_basic_total = total_basic_total + iit.total
                            total_ent = iit.total
                        if iit.code == "CMPS":
                            # worksheet.write(row, 10, "{:,.2f}".format(float(iit.total)) or '')
                            compensation_data = compensation_data + iit.total
                            # compensation_total = compensation_total + iit.total
                            total_comp_ent = iit.total

                        if iit.code == "TRA" or iit.code == "TRAMU":    
                            # worksheet.write(row, 11, "{:,.2f}".format(float(iit.total)) or '')
                            allowance_data = allowance_data + iit.total
                            # allowance_total = allowance_total + iit.total
                            total_all_ent = iit.total

                        if iit.code == "DAYALL":
                            # worksheet.write(row, 12, "{:,.2f}".format(float(iit.total) - float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction))) or '')
                            total_day_all_data = total_day_all_data + (iit.total -float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction)))
                            total_all_day_all = (iit.total -float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction)))
                            # total_day_all_total = total_day_all_total + (iit.total -float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction)))

                        if iit.code == "AEAA":
                            # worksheet.write(row, 13, "{:,.2f}".format(float(iit.total)) or '')
                            total_aeaa_data = total_aeaa_data + iit.total
                            total_all_aeaa = iit.total
                            # total_aeaa_total = total_aeaa_total + iit.total  


                        total_entitlements =  total_ent + total_comp_ent + total_all_ent + total_all_day_all + total_all_aeaa
                        if iit.code == "NET2" or iit.code == "GROSS" or iit.code == "NTS" or iit.code == "NETS" or iit.code == "NTTS":
                            # total_entitlements =  total_ent + total_comp_ent + total_all_ent
                            # worksheet.write(row, 14, "{:,.2f}".format(float(total_entitlements)) or '')
                            total_entitlements_data = total_entitlements_data + total_entitlements
                            # total_entitlements_total = total_entitlements_total + iit.total
                                
                        # if iit.code == "WAG":    
                        #     worksheet.write(row, 7, iit.total or '')
                        if iit.code == "SST":    
                            # worksheet.write(row, 15, "{:,.2f}".format(float(iit.total)) or '')
                            socailsecurity_data = socailsecurity_data + iit.total
                            # socailsecurity_total = socailsecurity_total + iit.total
                        if iit.code == "TAX":
                            # worksheet.write(row, 16, "{:,.2f}".format(float(iit.total)) or '')
                            tax_data = tax_data + iit.total
                            # tax_total = tax_total + iit.total
                        

                            
                        

                        if iit.code == "REDED":    
                            # worksheet.write(row, 17, "{:,.2f}".format(float(iit.total)) or '')
                            reded = reded + iit.total
                            # reded_total = reded_total + iit.total
                            
                        if iit.code == "BASDED":    
                            # worksheet.write(row, 18, "{:,.2f}".format(float(iit.total)) or '')
                            basded = basded + iit.total
                            # basded_total = basded_total + iit.total

                        if iit.code == "TTD":    
                            # worksheet.write(row, 19, "{:,.2f}".format(float(iit.total)) or '')
                            total_ded_data = total_ded_data + iit.total
                            # total_ded_total = total_ded_total + iit.total

                        if iit.code == "ded":    
                            # worksheet.write(row, 19, "{:,.2f}".format(float(iit.total)) or '')
                            total_ded1_data = total_ded1_data + iit.total
                            # total_ded_total = total_ded_total + iit.total
                            

                        if iit.code == "ded222":    
                            # worksheet.write(row, 19, "{:,.2f}".format(float(iit.total)) or '')
                            total_ded2_data = total_ded2_data + iit.total
                            # total_ded_total = total_ded_total + iit.total        
                            
                        if iit.code == "NET2" or iit.code == "GROSS" or iit.code == "NTS" or iit.code == "NETS" or iit.code == "NTTS":    
                            # worksheet.write(row, 20, "{:,.2f}".format(float(iit.total)) or '')
                            net_saled_data = net_saled_data + iit.total
                            # net_saled_total = net_saled_total + iit.total

                    # row += 1
                    sequence = sequence + 1 


                # worksheet.write(row, 6, "{:,.2f}".format(day_deduction_data)) #day deduction
                # worksheet.write(row, 7, "{:,.2f}".format(day_deduction_amount_data)) #day deduction amount

                # worksheet.write(row, 8, "{:,.2f}".format(total_wage_data)) # wage

                # worksheet.write(row, 9, "{:,.2f}".format(total_basic)) #basic salary


                # # worksheet.write(call, 4, 'Wage -الراتب الاسميUSD', header_bold)
                # worksheet.write(row, 10, "{:,.2f}".format(compensation_data)) #compensation

                # worksheet.write(row, 11, "{:,.2f}".format(allowance_data)) #allowance


                # worksheet.write(row, 12, "{:,.2f}".format(total_day_all_data)) #allowance
                # worksheet.write(row, 13, "{:,.2f}".format(total_aeaa_data)) #allowance





                
                

                # worksheet.write(row, 14, "{:,.2f}".format(total_entitlements_data)) #total of above 3

                

                # # worksheet.write(call, 7, 'Basic', header_bold)
                # worksheet.write(row, 15, "{:,.2f}".format(socailsecurity_data)) #socaial security
                # worksheet.write(row, 16, "{:,.2f}".format(tax_data)) #tax
                


                # worksheet.write(row, 17, "{:,.2f}".format(reded)) #REDED
                # worksheet.write(row, 18, "{:,.2f}".format(basded)) #BASDED
                # worksheet.write(row, 19, "{:,.2f}".format(total_ded_data)) #total deduction

                # worksheet.write(row, 20, "{:,.2f}".format(net_saled_data)) # Net Salary
                # call = row + 2 
                # row += 3
                day_deduction_total = day_deduction_total + day_deduction_data
                day_deduction_amount_total = day_deduction_amount_total + day_deduction_amount_data
                total_wage_total = total_wage_total + total_wage_data
                total_basic_total = total_basic_total + total_basic
                compensation_total = compensation_total + compensation_data
                allowance_total = allowance_total + allowance_data
                total_day_all_total = total_day_all_total + total_day_all_data
                total_aeaa_total = total_aeaa_total + total_aeaa_data
                total_entitlements_total = total_entitlements_total + total_entitlements_data
                socailsecurity_total = socailsecurity_total + socailsecurity_data
                tax_total = tax_total + tax_data
                reded_total = reded_total + reded
                basded_total = basded_total + basded
                total_ded_total = total_ded_total + total_ded_data

                total_ded1_total = total_ded1_total + total_ded1_data
                total_ded2_total = total_ded2_total + total_ded2_data
                net_saled_total = net_saled_total + net_saled_data

            # worksheet.write(row, 0, "المجموع الكلي") #day deduction
            worksheet.write(row, 0, depp.name, border_color_2)

            worksheet.write(row, 1, "{:,.2f}".format(day_deduction_total),main_cell) #day deduction
            worksheet.write(row, 2, "{:,.2f}".format(day_deduction_amount_total),main_cell) #day deduction amount

            worksheet.write(row, 3, "{:,.2f}".format(total_wage_total),main_cell) # wage

            worksheet.write(row, 4, "{:,.2f}".format(total_basic_total),main_cell) #basic salary


            # worksheet.write(call, 4, 'Wage -الراتب الاسميUSD', header_bold)
            worksheet.write(row, 5, "{:,.2f}".format(compensation_total),main_cell) #compensation

            worksheet.write(row, 6, "{:,.2f}".format(allowance_total),main_cell) #allowance


            worksheet.write(row, 7, "{:,.2f}".format(total_day_all_total),main_cell) #allowance
            worksheet.write(row, 8, "{:,.2f}".format(total_aeaa_total),main_cell) #allowance





            
            

            worksheet.write(row, 9, "{:,.2f}".format(total_entitlements_total),main_cell) #total of above 3

            

            # worksheet.write(call, 7, 'Basic', header_bold)
            worksheet.write(row, 10, "{:,.2f}".format(socailsecurity_total),main_cell) #socaial security
            worksheet.write(row, 11, "{:,.2f}".format(tax_total),main_cell) #tax
            


            worksheet.write(row, 12, "{:,.2f}".format(reded_total),main_cell) #REDED
            worksheet.write(row, 13, "{:,.2f}".format(basded_total),main_cell) #BASDED
            worksheet.write(row, 14, "{:,.2f}".format(total_ded_total),main_cell) #total deduction

            worksheet.write(row, 15, "{:,.2f}".format(total_ded1_total),main_cell) #total deduction
            worksheet.write(row, 16, "{:,.2f}".format(total_ded2_total),main_cell) #total deduction



            worksheet.write(row, 17, "{:,.2f}".format(net_saled_total),main_cell) # Net Salary

            day_deduction_every_thing_total = day_deduction_every_thing_total + day_deduction_total
            day_deduction_amount_every_thing_total = day_deduction_amount_every_thing_total + day_deduction_amount_total
            total_wage_every_thing_total = total_wage_every_thing_total + total_wage_total
            total_basic_every_thing_total = total_basic_every_thing_total + total_basic_total
            compensation_every_thing_total = compensation_every_thing_total + compensation_total
            allowance_every_thing_total = allowance_every_thing_total + allowance_total
            total_day_all_every_thing_total = total_day_all_every_thing_total + total_day_all_total
            total_aeaa_every_thing_total = total_aeaa_every_thing_total + total_aeaa_total
            total_entitlements_every_thing_total = total_entitlements_every_thing_total + total_entitlements_total
            socailsecurity_every_thing_total = socailsecurity_every_thing_total + socailsecurity_total
            tax_every_thing_total = tax_every_thing_total + tax_total
            reded_every_thing_total = reded_every_thing_total + reded_total
            basded_every_thing_total = basded_every_thing_total + basded_total
            total_ded_every_thing_total = total_ded_every_thing_total + total_ded_total

            total_ded1_every_thing_total = total_ded1_every_thing_total + total_ded1_total
            total_ded2_every_thing_total = total_ded2_every_thing_total + total_ded2_total

            net_saled_every_thing_total = net_saled_every_thing_total + net_saled_total
            call = row + 2 + 1
            row += 3
            print("row@@@@@@@@@@@@@@@@@@@",row)
            for x in range(16):
                worksheet.write(row - 1, x, '',main_cell)
                worksheet.write(row - 2, x, '',main_cell)
            

        worksheet.write(row, 0, "المجموع الكلي",main_cell_total_of_total) #day deduction

        worksheet.write(row, 1, "{:,.2f}".format(day_deduction_every_thing_total),main_cell_total_of_total) #day deduction
        worksheet.write(row, 2, "{:,.2f}".format(day_deduction_amount_every_thing_total),main_cell_total_of_total) #day deduction amount

        worksheet.write(row, 3, "{:,.2f}".format(total_wage_every_thing_total),main_cell_total_of_total) # wage

        worksheet.write(row, 4, "{:,.2f}".format(total_basic_every_thing_total),main_cell_total_of_total) #basic salary


        # worksheet.write(call, 4, 'Wage -الراتب الاسميUSD', header_bold)
        worksheet.write(row, 5, "{:,.2f}".format(compensation_every_thing_total),main_cell_total_of_total) #compensation

        worksheet.write(row, 6, "{:,.2f}".format(allowance_every_thing_total),main_cell_total_of_total) #allowance


        worksheet.write(row, 7, "{:,.2f}".format(total_day_all_every_thing_total),main_cell_total_of_total) #allowance
        worksheet.write(row, 8, "{:,.2f}".format(total_aeaa_every_thing_total),main_cell_total_of_total) #allowance





        
        

        worksheet.write(row, 9, "{:,.2f}".format(total_entitlements_every_thing_total),main_cell_total_of_total) #total of above 3

        

        # worksheet.write(call, 7, 'Basic', header_bold)
        worksheet.write(row, 10, "{:,.2f}".format(socailsecurity_every_thing_total),main_cell_total_of_total) #socaial security
        worksheet.write(row, 11, "{:,.2f}".format(tax_every_thing_total),main_cell_total_of_total) #tax
        


        worksheet.write(row, 12, "{:,.2f}".format(reded_every_thing_total),main_cell_total_of_total) #REDED
        worksheet.write(row, 13, "{:,.2f}".format(basded_every_thing_total),main_cell_total_of_total) #BASDED
        worksheet.write(row, 14, "{:,.2f}".format(total_ded_every_thing_total),main_cell_total_of_total) #total deduction

        worksheet.write(row, 15, "{:,.2f}".format(total_ded1_every_thing_total),main_cell_total_of_total) #total deduction
        worksheet.write(row, 16, "{:,.2f}".format(total_ded2_every_thing_total),main_cell_total_of_total) #total deduction

        

        worksheet.write(row, 17, "{:,.2f}".format(net_saled_every_thing_total),main_cell_total_of_total) # Net Salary


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

        # file_added = "/home/anuj/Desktop/workspace13/payslip_report.xlsx"
        # with open(file_added, "wb") as binary_file:
        #     binary_file.write(xlDecoded)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        download_url = '/web/content/' + str(ir_id.id) + '?download=true'
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }    



    def send_mis_report(self):
        filename = 'Payslip.xls'
        string = 'Payslip_report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string)
        header_bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")

        header_bold_extra_tag = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour green;")

        header_bold_extra = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour red;")
        cell_format = xlwt.easyxf()
        filename = 'Payslip_Report_%s.xls' % date.today()
        rested = self.env['hr.payslip'].search([])
        row = 2
        border_normal = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; font: bold on; pattern: pattern solid, fore_colour gray25;')
        border_1 = xlwt.easyxf('borders: left 1, right 1, top 1, bottom 1;')
        border_2 = xlwt.easyxf('borders: left 2, right 2, top 2, bottom 2;')
        border_color_2 = xlwt.easyxf('borders: top_color blue, bottom_color blue, right_color blue, left_color blue, left 2, right 2, top 2, bottom 2; font: bold on; pattern: pattern solid, fore_colour gray25;')
        worksheet.col(0).width = 10000
        worksheet.col(1).width = 15000
        worksheet.col(2).width = 10000
        worksheet.row(0).height = 500

        department_data = self.env["hr.department"].search([("parent_id",'=',False)])

        call = 1
        for depp in  department_data:
            print("department_data#############",depp.id)
            print("parent_id$$$$$$$$$$$$$$$$$",depp.parent_id)

            partner_data = self.env["hr.department"].search([("parent_id",'=',depp.id)])
            print("depp###############",partner_data.mapped('id') + [depp.id])

            all_ids = [depp.id] + partner_data.mapped('id') 

            print("all_ids@@@@@@@@@@@@@@",all_ids)

            
            # partner_data = (4, depp.id)
            print("partner_data@@@@@@@@@@@@@",partner_data)
            day_deduction_total = 0
            total_basic_total = 0 
            total_wage_total = 0
            compensation_total = 0
            tax_total = 0
            day_deduction_total = 0
            day_deduction_amount_total = 0
            socailsecurity_total = 0
            allowance_total = 0
            reded_total = 0
            basded_total = 0
            total_ded_total = 0
            net_saled_total = 0
            total_day_all_total = 0
            total_aeaa_total = 0
            total_entitlements_total = 0
            certificate_total = 0
            for values_data in all_ids:
                dep = self.env["hr.department"].search([('id','=',values_data)])
                print("depdepdepdepdepdepdepdepdepdepdep",dep.id)
                # rested = self.env['hr.payslip'].search([('department','=',dep.id)])
                rested = self.filtered(lambda picking: picking.employee_id.department_id.id == dep.id)
                worksheet.write(call - 1, 0, dep.name, border_color_2)

                worksheet.write_merge(call - 1, call - 1, 9, 14, 'مجموع الاستحقاقات', header_bold_extra_tag)
                worksheet.write_merge(call - 1, call - 1, 15, 19, 'مجموع الاستقطاعات', header_bold_extra)

                worksheet.write(call, 1, 'رقم القصاصة', border_color_2)  # refernce 
                # worksheet.write(call, 1, 'Payslip Name', border_color_2)

                worksheet.write(call, 2, 'اسم الموظف', border_color_2) # employee


                worksheet.write(call, 3, 'نوع الخدمة', border_color_2) # employee type

                worksheet.write(call, 4, 'نوع الشهادة', border_color_2) # certifiactae



                worksheet.write(call, 5, 'التفاصيل', header_bold) # description

                worksheet.write(call, 6, 'عدد الايام المستقطعة', header_bold) #day deduction
                worksheet.write(call, 7, 'مبلغ الايام المستقطعة', header_bold) #day deduction amount

                worksheet.write(call, 8, 'الراتب الكلي', header_bold) # wage

                worksheet.write(call, 9, 'الراتب الاسمي', header_bold) #basic salary


                # worksheet.write(call, 4, 'Wage -الراتب الاسميUSD', header_bold)
                worksheet.write(call, 10, 'التعويضية', header_bold) #compensation

                worksheet.write(call, 11, 'التدريب والتأهيل', header_bold) #allowance

                worksheet.write(call, 12, 'مكافأت غير العاملين', header_bold) #allowance
                worksheet.write(call, 13, 'الاعانات', header_bold) #allowance

                worksheet.write(call, 14, 'مجموع الاستحقاقات', header_bold) #allowance

                

                # worksheet.write(call, 7, 'Basic', header_bold)
                worksheet.write(call, 15, 'الضمان الاجتماعي', header_bold) #socaial security
                worksheet.write(call, 16, 'الضريبة', header_bold) #tax
                


                
                worksheet.write(call, 17, 'استقطاع التقاعد', header_bold) #REDED
                worksheet.write(call, 18, 'استقطاعات جامعة البصرة ل I2', header_bold) #BASDED
                worksheet.write(call, 19, 'مجموع الاستقطاعات', header_bold) #total deduction

                worksheet.write(call, 20, 'صافي الراتب', header_bold) # Net Salary
                # v.onboard_date >= (datetime.today().date().replace(day=1) - relativedelta(months=1)) and v.onboard_date <= (datetime.today().date() - relativedelta(months=1))
                total_basic = 0 
                total_wage_data = 0
                compensation_data = 0
                tax_data = 0
                day_deduction_data = 0
                day_deduction_amount_data = 0
                socailsecurity_data = 0
                allowance_data = 0
                reded = 0
                basded = 0
                total_ded_data = 0
                net_saled_data = 0
                total_day_all_data = 0
                total_aeaa_data = 0
                total_entitlements_data = 0
                certificate_data = 0
                sequence = 1
                for material_line_id in rested:
                    worksheet.write(row, 0, sequence or '')
                    worksheet.write(row, 1, material_line_id.number or '')
                    # worksheet.write(row, 1, material_line_id.name or '')

                    worksheet.write(row, 2, material_line_id.employee_id.name or '')

                    if material_line_id.contract_id.employ_type == 'option1':
                        employe_data = 'تعيين - متقاعد'
                    if material_line_id.contract_id.employ_type == 'option2':
                        employe_data = 'تعيين - غير متقاعد مشمول بالضمان'
                    if material_line_id.contract_id.employ_type == 'option3':
                        employe_data = 'اعارة'
                    if material_line_id.contract_id.employ_type == 'option4':
                        employe_data = 'محاضر خارجي'
                    if material_line_id.contract_id.employ_type == 'option5':
                        employe_data = 'اجر يومي'

                    worksheet.write(row, 3, employe_data or '')


                    if material_line_id.employee_id.certificate_first == 'certificate1': 
                        certificate_data  = 'دكتوراه'
                    if material_line_id.employee_id.certificate_first == 'certificate2': 
                        certificate_data  = 'ماجستير'
                    if material_line_id.employee_id.certificate_first == 'certificate3': 
                        certificate_data  = 'دبلوم عالي'
                    if material_line_id.employee_id.certificate_first == 'certificate4': 
                        certificate_data  = 'بكالوريوس'
                    if material_line_id.employee_id.certificate_first == 'certificate5': 
                        certificate_data  = 'دبلوم معهد'
                    if material_line_id.employee_id.certificate_first == 'certificate6': 
                        certificate_data  = 'اعدادية'
                    if material_line_id.employee_id.certificate_first == 'certificate7': 
                        certificate_data  = 'دون الاعدادية'

                    worksheet.write(row, 4, certificate_data or '')

                    

                    if material_line_id.description:
                        worksheet.write(row, 5, re.sub('<[^>]*>', '', material_line_id.description) or '')

                    if not material_line_id.description:
                        worksheet.write(row, 5, material_line_id.description or '')

                    worksheet.write(row, 6, "{:,.2f}".format(float(material_line_id.contract_id.day_deduction)) or '')

                    day_deduction_data = day_deduction_data + material_line_id.contract_id.day_deduction
                    # day_deduction_total = day_deduction_total + material_line_id.contract_id.day_deduction

                    worksheet.write(row, 7, "{:,.2f}".format(float((((material_line_id.contract_id.wage + material_line_id.contract_id.training_field) / 30) * material_line_id.contract_id.day_deduction))) or '') 

                    day_deduction_amount_data = day_deduction_amount_data + float((((material_line_id.contract_id.wage + material_line_id.contract_id.training_field) / 30) * material_line_id.contract_id.day_deduction))
                    # day_deduction_amount_total = day_deduction_amount_total + float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction))
                          

                    # if material_line_id.contract_id.currency_id.id == 2:
                    #     worksheet.write(row, 4, str(material_line_id.contract_id.wage) + "$" or '')

                    # if material_line_id.contract_id.currency_id.id == 90:
                    worksheet.write(row, 8, "{:,.2f}".format(float(material_line_id.contract_id.wage) + float(material_line_id.contract_id.training_field)) + "ع.د" or '')
                    total_wage_data = total_wage_data + (float(material_line_id.contract_id.wage) + float(material_line_id.contract_id.training_field))
                    # total_wage_total = total_wage_total + (float(material_line_id.contract_id.wage) + float(material_line_id.contract_id.training_field))
                    total_ent = 0
                    total_comp_ent = 0
                    total_all_ent = 0
                    total_all_day_all = 0
                    total_all_aeaa = 0
                    for iit in material_line_id.line_ids:
                        if iit.code == "BSCC":
                            worksheet.write(row, 9, "{:,.2f}".format(float(iit.total)) or '')
                            total_basic = total_basic + iit.total
                            # total_basic_total = total_basic_total + iit.total
                            total_ent = iit.total
                        if iit.code == "CMPS":
                            worksheet.write(row, 10, "{:,.2f}".format(float(iit.total)) or '')
                            compensation_data = compensation_data + iit.total
                            # compensation_total = compensation_total + iit.total
                            total_comp_ent = iit.total

                        if iit.code == "TRA" or iit.code == "TRAMU":    
                            worksheet.write(row, 11, "{:,.2f}".format(float(iit.total)) or '')
                            allowance_data = allowance_data + iit.total
                            # allowance_total = allowance_total + iit.total
                            total_all_ent = iit.total

                        if iit.code == "DAYALL":
                            worksheet.write(row, 12, "{:,.2f}".format(float(iit.total) - float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction))) or '')
                            total_day_all_data = total_day_all_data + (iit.total -float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction)))
                            total_all_day_all = (iit.total -float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction)))
                            # total_day_all_total = total_day_all_total + (iit.total -float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction)))

                        if iit.code == "AEAA":
                            worksheet.write(row, 13, "{:,.2f}".format(float(iit.total)) or '')
                            total_aeaa_data = total_aeaa_data + iit.total
                            total_all_aeaa = iit.total
                            # total_aeaa_total = total_aeaa_total + iit.total  


                        total_entitlements =  total_ent + total_comp_ent + total_all_ent + total_all_day_all + total_all_aeaa    

                        if iit.code == "NET2" or iit.code == "GROSS" or iit.code == "NTS" or iit.code == "NETS" or iit.code == "NTTS" and total_entitlements > 0:
                            # total_entitlements =  total_ent + total_comp_ent + total_all_ent
                            worksheet.write(row, 14, "{:,.2f}".format(float(total_entitlements)) or '')
                            total_entitlements_data = total_entitlements_data + total_entitlements
                            # total_entitlements_total = total_entitlements_total + iit.total
                                
                        # if iit.code == "WAG":    
                        #     worksheet.write(row, 7, iit.total or '')
                        if iit.code == "SST":    
                            worksheet.write(row, 15, "{:,.2f}".format(float(iit.total)) or '')
                            socailsecurity_data = socailsecurity_data + iit.total
                            # socailsecurity_total = socailsecurity_total + iit.total
                        if iit.code == "TAX":
                            worksheet.write(row, 16, "{:,.2f}".format(float(iit.total)) or '')
                            tax_data = tax_data + iit.total
                            # tax_total = tax_total + iit.total
                        

                            
                        

                        if iit.code == "REDED":    
                            worksheet.write(row, 17, "{:,.2f}".format(float(iit.total)) or '')
                            reded = reded + iit.total
                            # reded_total = reded_total + iit.total
                            
                        if iit.code == "BASDED":    
                            worksheet.write(row, 18, "{:,.2f}".format(float(iit.total)) or '')
                            basded = basded + iit.total
                            # basded_total = basded_total + iit.total

                        if iit.code == "TTD":    
                            worksheet.write(row, 19, "{:,.2f}".format(float(iit.total)) or '')
                            total_ded_data = total_ded_data + iit.total
                            # total_ded_total = total_ded_total + iit.total
                            
                        if iit.code == "NET2" or iit.code == "GROSS" or iit.code == "NTS" or iit.code == "NETS" or iit.code == "NTTS":    
                            worksheet.write(row, 20, "{:,.2f}".format(float(iit.total)) or '')
                            net_saled_data = net_saled_data + iit.total
                            # net_saled_total = net_saled_total + iit.total

                    row += 1
                    sequence = sequence + 1 

                row = row + 2
                worksheet.write(row, 6, "{:,.2f}".format(day_deduction_data)) #day deduction
                worksheet.write(row, 7, "{:,.2f}".format(day_deduction_amount_data)) #day deduction amount

                worksheet.write(row, 8, "{:,.2f}".format(total_wage_data)) # wage

                worksheet.write(row, 9, "{:,.2f}".format(total_basic)) #basic salary


                # worksheet.write(call, 4, 'Wage -الراتب الاسميUSD', header_bold)
                worksheet.write(row, 10, "{:,.2f}".format(compensation_data)) #compensation

                worksheet.write(row, 11, "{:,.2f}".format(allowance_data)) #allowance


                worksheet.write(row, 12, "{:,.2f}".format(total_day_all_data)) #allowance
                worksheet.write(row, 13, "{:,.2f}".format(total_aeaa_data)) #allowance





                
                

                worksheet.write(row, 14, "{:,.2f}".format(total_entitlements_data)) #total of above 3

                

                # worksheet.write(call, 7, 'Basic', header_bold)
                worksheet.write(row, 15, "{:,.2f}".format(socailsecurity_data)) #socaial security
                worksheet.write(row, 16, "{:,.2f}".format(tax_data)) #tax
                


                worksheet.write(row, 17, "{:,.2f}".format(reded)) #REDED
                worksheet.write(row, 18, "{:,.2f}".format(basded)) #BASDED
                worksheet.write(row, 19, "{:,.2f}".format(total_ded_data)) #total deduction

                worksheet.write(row, 20, "{:,.2f}".format(net_saled_data)) # Net Salary


                day_deduction_total = day_deduction_total + day_deduction_data
                day_deduction_amount_total = day_deduction_amount_total + day_deduction_amount_data
                total_wage_total = total_wage_total + total_wage_data
                total_basic_total = total_basic_total + total_basic
                compensation_total = compensation_total + compensation_data
                allowance_total = allowance_total + allowance_data
                total_day_all_total = total_day_all_total + total_day_all_data
                total_aeaa_total = total_aeaa_total + total_aeaa_data
                total_entitlements_total = total_entitlements_total + total_entitlements_data
                socailsecurity_total = socailsecurity_total + socailsecurity_data
                tax_total = tax_total + tax_data
                reded_total = reded_total + reded
                basded_total = basded_total + basded
                total_ded_total = total_ded_total + total_ded_data
                net_saled_total = net_saled_total + net_saled_data
                
                call = row + 2 
                row += 4

            worksheet.write(row, 0, "المجموع الكلي") #day deduction

            worksheet.write(row, 6, "{:,.2f}".format(day_deduction_total)) #day deduction
            worksheet.write(row, 7, "{:,.2f}".format(day_deduction_amount_total)) #day deduction amount

            worksheet.write(row, 8, "{:,.2f}".format(total_wage_total)) # wage

            worksheet.write(row, 9, "{:,.2f}".format(total_basic_total)) #basic salary


            # worksheet.write(call, 4, 'Wage -الراتب الاسميUSD', header_bold)
            worksheet.write(row, 10, "{:,.2f}".format(compensation_total)) #compensation

            worksheet.write(row, 11, "{:,.2f}".format(allowance_total)) #allowance


            worksheet.write(row, 12, "{:,.2f}".format(total_day_all_total)) #allowance
            worksheet.write(row, 13, "{:,.2f}".format(total_aeaa_total)) #allowance





            
            

            worksheet.write(row, 14, "{:,.2f}".format(total_entitlements_total)) #total of above 3

            

            # worksheet.write(call, 7, 'Basic', header_bold)
            worksheet.write(row, 15, "{:,.2f}".format(socailsecurity_total)) #socaial security
            worksheet.write(row, 16, "{:,.2f}".format(tax_total)) #tax
            


            worksheet.write(row, 17, "{:,.2f}".format(reded_total)) #REDED
            worksheet.write(row, 18, "{:,.2f}".format(basded_total)) #BASDED
            worksheet.write(row, 19, "{:,.2f}".format(total_ded_total)) #total deduction

            worksheet.write(row, 20, "{:,.2f}".format(net_saled_total)) # Net Salary



            call = row + 2 + 1
            row += 3 + 1
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

        # file_added = "/home/anuj/Desktop/workspace13/payslip_report.xlsx"
        # with open(file_added, "wb") as binary_file:
        #     binary_file.write(xlDecoded)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        download_url = '/web/content/' + str(ir_id.id) + '?download=true'
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }    

        # df = pd.export_excel (r'/home/anuj/Desktop/workspace13/payslip_report.xlsx')
        # print (df)              
    

        # df = pd.export_excel (r'/home/anuj/Desktop/workspace13/payslip_report.xlsx')
        # print (df)              



    def send_mis_report_for_department_new(self):
        filename = 'Payslip.xls'
        string = 'Payslip_report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        
        translator= Translator(to_lang="Arabic")
        translation = translator.translate(calendar.month_name[date.today().month])



        header_bold = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour gray25; align: horiz centre")


        header_bold_main_header = xlwt.easyxf("font: bold on, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; align: horiz centre; align: vert centre")


        
        main_cell_total = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour ivory; align: horiz centre")


        main_cell_total_of_total = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour lime; align: horiz centre")


        header_bold_extra_tag = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour green; font: color white; align: horiz centre")

        header_bold_extra = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour red; font: color white; align: horiz centre")
        cell_format = xlwt.easyxf()
        filename = 'Payslip_Report_%s.xls' % date.today()
        rested = self.env['hr.payslip'].search([])
        row = 2
        border_normal = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; font: bold on; pattern: pattern solid, fore_colour gray25;')
        border_1 = xlwt.easyxf('borders: left 1, right 1, top 1, bottom 1;')
        border_2 = xlwt.easyxf('borders: left 2, right 2, top 2, bottom 2;')
        border_color_2 = xlwt.easyxf('borders: top_color blue, bottom_color blue, right_color blue, left_color blue, left 2, right 2, top 2, bottom 2; font: bold on; pattern: pattern solid, fore_colour gray25;')
        


        # worksheet.col(1).width = 15000
        # worksheet.col(2).width = 10000
        # worksheet.row(0).height = 500
        main_cell = xlwt.easyxf('font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; align: horiz centre')

        employe_data =0

        department_data = self.env["hr.department"].search([("parent_id",'=',False)])

        for depp in  department_data:
            worksheet = wb.add_sheet(depp.name, cell_overwrite_ok=True)

            worksheet.paper_size_code = 1

            worksheet.cols_right_to_left = True

            worksheet.col(0).width = 2500
            worksheet.col(2).width = 3000
            worksheet.col(1).width = 4500
            worksheet.col(3).width = 3000
            worksheet.col(4).width = 3000
            worksheet.col(5).width = 3000
            worksheet.col(6).width = 3000
            worksheet.col(7).width = 3000
            worksheet.col(8).width = 3000
            worksheet.col(9).width = 3000
            worksheet.col(10).width = 3000
            worksheet.col(11).width = 3000
            worksheet.col(12).width = 3000
            worksheet.col(13).width = 3000
            worksheet.col(14).width = 3000
            worksheet.col(15).width = 3000
            worksheet.col(16).width = 3000
            worksheet.col(17).width = 3000
            worksheet.col(18).width = 3000
            worksheet.col(19).width = 3000

            row = 6
            call = 4
            # print("department_data#############",depp.id)
            # print("parent_id$$$$$$$$$$$$$$$$$",depp.parent_id)

            partner_data = self.env["hr.department"].search([("parent_id",'=',depp.id)])
            # print("depp###############",partner_data.mapped('id') + [depp.id])

            all_ids = [depp.id] + partner_data.mapped('id') 

            # print("all_ids@@@@@@@@@@@@@@",all_ids)

            
            # partner_data = (4, depp.id)
            # print("partner_data@@@@@@@@@@@@@",partner_data)
            day_deduction_total = 0
            total_basic_total = 0 
            total_wage_total = 0
            compensation_total = 0
            tax_total = 0
            day_deduction_total = 0
            day_deduction_amount_total = 0
            socailsecurity_total = 0
            allowance_total = 0
            reded_total = 0
            basded_total = 0
            total_ded_total = 0
            total_ded1_total = 0
            total_ded2_total = 0

            net_saled_total = 0
            total_day_all_total = 0
            total_aeaa_total = 0
            total_entitlements_total = 0
            certificate_total = 0
            
            worksheet.write_merge(call - 4, call - 2 , 0, 2, "جامعة الاهلية / قسم الشؤون المالية", header_bold_main_header)
            
            for values_data in all_ids:
                dep = self.env["hr.department"].search([('id','=',values_data)])
                print("depdepdepdepdepdepdepdepdepdepdep",dep.id)

                # rested = self.env['hr.payslip'].search([('department','=',dep.id)])
                rested = self.filtered(lambda picking: picking.employee_id.department_id.id == dep.id).sorted(key=lambda r: r.employee_id.job_id.sequence)

                worksheet.write_merge(0, 2, 3, 13, (" رواتب " + depp.name + " لشهر " + " - " + translation + convert_numbers.english_to_arabic(date.today().year)), header_bold_main_header)
                worksheet.write(call - 1, 0, dep.name, header_bold)



                

                worksheet.write_merge(call - 1, call - 1, 5, 10, 'المستحقات', header_bold_extra_tag)
                worksheet.write_merge(call - 1, call - 1, 11, 18, 'الاستقطاعات', header_bold_extra)

                # worksheet.write(call, 1, 'رقم القصاصة', header_bold)  # refernce 
                # worksheet.write(call, 1, 'Payslip Name', border_color_2)

                worksheet.write(call, 1, 'اسم الموظف', header_bold) # employee

                worksheet.write(call, 2, 'التخصص الدقيق', header_bold)


                # worksheet.write(call, 3, 'نوع الخدمة', header_bold) # employee type

                # worksheet.write(call, 4, 'نوع الشهادة', header_bold) # certifiactae



                # worksheet.write(call, 5, 'التفاصيل', header_bold) # description

                worksheet.write(call, 3, 'الايام المستقطعة', header_bold) #day deduction
                worksheet.write(call, 4, 'مبلغ ألايام', header_bold) #day deduction amount

                worksheet.write(call, 5, 'الراتب الكلي', header_bold) # wage

                worksheet.write(call, 6, 'الراتب الاسمي', header_bold) #basic salary


                # worksheet.write(call, 4, 'Wage -الراتب الاسميUSD', header_bold)
                worksheet.write(call, 7, 'التعويضية', header_bold) #compensation

                worksheet.write(call, 8, 'التدريب والتأهيل', header_bold) #allowance

                worksheet.write(call, 9, 'م.غ العاملين', header_bold) #allowance
                worksheet.write(call, 10, 'الاعانات', header_bold) #allowance

                worksheet.write(call, 11, 'م.الاستحقاقات', header_bold) #allowance

                

                # worksheet.write(call, 7, 'Basic', header_bold)
                worksheet.write(call, 12, 'الضمان', header_bold) #socaial security
                worksheet.write(call, 13, 'الضريبة', header_bold) #tax
                


                
                worksheet.write(call, 14, 'استقطاع التقاعد', header_bold) #REDED
                worksheet.write(call, 15, 'جامعة البصرة', header_bold) #BASDED
                worksheet.write(call, 16, 'م.تنفيذ البصره', header_bold) #total deduction
                worksheet.write(call, 17, 'استقطاع ايراد سلف', header_bold) #total deduction

                worksheet.write(call, 18, 'م.الاستقطاعات', header_bold) #total deduction

                worksheet.write(call, 19, 'صافي الراتب', header_bold) # Net Salary

                
                # v.onboard_date >= (datetime.today().date().replace(day=1) - relativedelta(months=1)) and v.onboard_date <= (datetime.today().date() - relativedelta(months=1))
                total_basic = 0 
                total_wage_data = 0
                compensation_data = 0
                tax_data = 0
                day_deduction_data = 0
                day_deduction_amount_data = 0
                socailsecurity_data = 0
                allowance_data = 0
                reded = 0
                basded = 0
                total_ded_data = 0
                total_ded1_data = 0
                total_ded2_data = 0
                net_saled_data = 0
                total_day_all_data = 0
                total_aeaa_data = 0
                total_entitlements_data = 0
                certificate_data = 0
                sequence = 1
                for material_line_id in rested:
                    worksheet.write(row, 0, sequence or '',main_cell)
                    # worksheet.write(row, 1, material_line_id.number or '',main_cell)
                    # worksheet.write(row, 1, material_line_id.name or '',main_cell)

                    worksheet.write(row, 1, material_line_id.employee_id.name or '',main_cell)

                    if material_line_id.contract_id.employ_type == 'option1':
                        employe_data = 'تعيين - متقاعد'
                    if material_line_id.contract_id.employ_type == 'option2':
                        employe_data = 'تعيين - غير متقاعد مشمول بالضمان'
                    if material_line_id.contract_id.employ_type == 'option3':
                        employe_data = 'اعارة'
                    if material_line_id.contract_id.employ_type == 'option4':
                        employe_data = 'محاضر خارجي'
                    if material_line_id.contract_id.employ_type == 'option5':
                        employe_data = 'اجر يومي'

                    # worksheet.write(row, 3, employe_data or '',main_cell)


                    if material_line_id.employee_id.certificate_first == 'certificate1': 
                        certificate_data  = 'دكتوراه'
                    if material_line_id.employee_id.certificate_first == 'certificate2': 
                        certificate_data  = 'ماجستير'
                    if material_line_id.employee_id.certificate_first == 'certificate3': 
                        certificate_data  = 'دبلوم عالي'
                    if material_line_id.employee_id.certificate_first == 'certificate4': 
                        certificate_data  = 'بكالوريوس'
                    if material_line_id.employee_id.certificate_first == 'certificate5': 
                        certificate_data  = 'دبلوم معهد'
                    if material_line_id.employee_id.certificate_first == 'certificate6': 
                        certificate_data  = 'اعدادية'
                    if material_line_id.employee_id.certificate_first == 'certificate7': 
                        certificate_data  = 'دون الاعدادية'

                    # worksheet.write(row, 4, certificate_data or '',main_cell)

                    

                    # if material_line_id.description:
                    #     worksheet.write(row, 5, re.sub('<[^>]*>', '', material_line_id.description) or '',main_cell)

                    # if not material_line_id.description:
                    #     worksheet.write(row, 5, material_line_id.description or '',main_cell)
                    worksheet.write(row, 2, material_line_id.employee_id.first_field or '', main_cell)

                    worksheet.write(row, 3, "{:,.2f}".format(float(material_line_id.contract_id.day_deduction)) or '',main_cell)

                    day_deduction_data = day_deduction_data + material_line_id.contract_id.day_deduction
                    day_deduction_total = day_deduction_total + material_line_id.contract_id.day_deduction

                    worksheet.write(row, 4, "{:,.2f}".format(float((((material_line_id.contract_id.wage + material_line_id.contract_id.training_field) / 30) * material_line_id.contract_id.day_deduction))) or '',main_cell) 

                    day_deduction_amount_data = day_deduction_amount_data + float((((material_line_id.contract_id.wage + material_line_id.contract_id.training_field) / 30) * material_line_id.contract_id.day_deduction))
                    day_deduction_amount_total = day_deduction_amount_total + float((((material_line_id.contract_id.wage + material_line_id.contract_id.training_field) / 30) * material_line_id.contract_id.day_deduction))
                          

                    # if material_line_id.contract_id.currency_id.id == 2:
                    #     worksheet.write(row, 4, str(material_line_id.contract_id.wage) + "$" or '',main_cell)

                    # if material_line_id.contract_id.currency_id.id == 90:
                    worksheet.write(row, 5, "{:,.2f}".format(float(material_line_id.contract_id.wage) + float(material_line_id.contract_id.training_field)) + "ع.د" or '',main_cell)
                    total_wage_data = total_wage_data + (float(material_line_id.contract_id.wage) + float(material_line_id.contract_id.training_field))
                    total_wage_total = total_wage_total + (float(material_line_id.contract_id.wage) + float(material_line_id.contract_id.training_field))
                    total_ent = 0
                    total_comp_ent = 0
                    total_all_ent = 0
                    total_all_day_all = 0
                    total_all_aeaa = 0
                    for iit in material_line_id.line_ids:
                        if iit.code == "BSCC":
                            worksheet.write(row, 6, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            total_basic = total_basic + iit.total
                            total_basic_total = total_basic_total + iit.total
                            total_ent = iit.total
                        if not total_basic:
                            worksheet.write(row, 6, '',main_cell)  
                        if iit.code == "CMPS":
                            worksheet.write(row, 7, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            compensation_data = compensation_data + iit.total
                            compensation_total = compensation_total + iit.total
                            total_comp_ent = iit.total
                        if not compensation_data:
                            worksheet.write(row, 7, '',main_cell)  

                        if iit.code == "TRA" or iit.code == "TRAMU":    
                            worksheet.write(row, 8, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            allowance_data = allowance_data + iit.total
                            allowance_total = allowance_total + iit.total
                            total_all_ent = iit.total
                        if not allowance_data:
                            worksheet.write(row, 8, '',main_cell)    

                        if iit.code == "DAYALL":
                            worksheet.write(row, 9, "{:,.2f}".format(float(iit.total) - float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction))) or '',main_cell)
                            total_day_all_data = total_day_all_data + (iit.total -float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction)))
                            total_day_all_total = total_day_all_total + (iit.total -float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction)))
                            total_all_day_all = (iit.total -float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction)))
                        if not total_day_all_data:
                            worksheet.write(row, 9, '',main_cell)
                        if iit.code == "AEAA":
                            worksheet.write(row, 10, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            total_aeaa_data = total_aeaa_data + iit.total
                            total_aeaa_total = total_aeaa_total + iit.total  
                            total_all_aeaa = iit.total
                        if not total_aeaa_data:
                            worksheet.write(row, 10, '',main_cell)


                        total_entitlements =  total_ent + total_comp_ent + total_all_ent + total_all_day_all + total_all_aeaa
                        print("total_entitlements@@@@@@@@@@@@@@@@@@",total_entitlements)
                        if iit.code == "NET2" or iit.code == "GROSS" or iit.code == "NTS" or iit.code == "NETS" or iit.code == "NTTS" and total_entitlements > 0:
                            print("total_entitlements222222222222222222222222",total_entitlements)
                            worksheet.write(row, 11, "{:,.2f}".format(float(total_entitlements)) or '',main_cell)
                            total_entitlements_data = total_entitlements_data + total_entitlements
                            total_entitlements_total = total_entitlements_total + total_entitlements
                                
                        if not total_entitlements_data:
                            worksheet.write(row, 11, '',main_cell)        
                        # if iit.code == "WAG":    
                        #     worksheet.write(row, 7, iit.total or '',main_cell)
                        if iit.code == "SST":    
                            worksheet.write(row, 12, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            socailsecurity_data = socailsecurity_data + iit.total
                            socailsecurity_total = socailsecurity_total + iit.total

                        if not socailsecurity_data:
                            worksheet.write(row, 12, '',main_cell) 

                        if iit.code == "TAX":
                            worksheet.write(row, 13, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            tax_data = tax_data + iit.total
                            tax_total = tax_total + iit.total

                        if not tax_data:
                            worksheet.write(row, 13, '',main_cell) 

                        if iit.code == "REDED":    
                            worksheet.write(row, 14, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            reded = reded + iit.total
                            reded_total = reded_total + iit.total
                            
                        if not reded:
                            worksheet.write(row, 14, '',main_cell)


                        if iit.code == "BASDED":    
                            worksheet.write(row, 15, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            basded = basded + iit.total
                            basded_total = basded_total + iit.total

                        if not basded:
                            worksheet.write(row, 15, '',main_cell)

                        if iit.code == "ded":    
                            worksheet.write(row, 16, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            total_ded1_data = total_ded1_data + iit.total
                            total_ded1_total = total_ded1_total + iit.total
                            
                        if not total_ded1_data:
                            worksheet.write(row, 16, '',main_cell)
                            
                        if iit.code == "ded222":    
                            worksheet.write(row, 17, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            total_ded2_data = total_ded2_data + iit.total
                            total_ded2_total = total_ded2_total + iit.total
                            
                        if not total_ded2_data:
                            worksheet.write(row, 17, '',main_cell)        

                        if iit.code == "TTD":    
                            worksheet.write(row, 18, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            total_ded_data = total_ded_data + iit.total
                            total_ded_total = total_ded_total + iit.total
                            
                        if not total_ded_data:
                            worksheet.write(row, 18, '',main_cell)

                        if iit.code == "NET2" or iit.code == "GROSS" or iit.code == "NTS" or iit.code == "NETS" or iit.code == "NTTS":    
                            worksheet.write(row, 19, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            net_saled_data = net_saled_data + iit.total
                            net_saled_total = net_saled_total + iit.total

                        if not net_saled_data:
                            worksheet.write(row, 19, '',main_cell)    

                        

                    row += 1
                    sequence = sequence + 1 

                for x in range(17):
                    worksheet.write(row, x, '',main_cell)
                    worksheet.write(row + 1, x, '',main_cell)
                row = row + 2
                worksheet.write(row, 0, '',main_cell_total)
                worksheet.write(row, 1, '',main_cell_total)

                worksheet.write(row, 3, "{:,.2f}".format(day_deduction_data),main_cell_total) #day deduction
                worksheet.write(row, 4, "{:,.2f}".format(day_deduction_amount_data),main_cell_total) #day deduction amount

                worksheet.write(row, 5, "{:,.2f}".format(total_wage_data),main_cell_total) # wage

                worksheet.write(row, 6, "{:,.2f}".format(total_basic),main_cell_total) #basic salary


                # worksheet.write(call, 4, 'Wage -الراتب الاسميUSD', header_bold)
                worksheet.write(row, 7, "{:,.2f}".format(compensation_data),main_cell_total) #compensation

                worksheet.write(row, 8, "{:,.2f}".format(allowance_data),main_cell_total) #allowance


                worksheet.write(row, 9, "{:,.2f}".format(total_day_all_data),main_cell_total) #allowance
                worksheet.write(row, 10, "{:,.2f}".format(total_aeaa_data),main_cell_total) #allowance

                worksheet.write(row, 11, "{:,.2f}".format(total_entitlements_data),main_cell_total) #total of above 3

                # worksheet.write(call, 7, 'Basic', header_bold)
                worksheet.write(row, 12, "{:,.2f}".format(socailsecurity_data),main_cell_total) #socaial security
                worksheet.write(row, 13, "{:,.2f}".format(tax_data),main_cell_total) #tax

                worksheet.write(row, 14, "{:,.2f}".format(reded),main_cell_total) #REDED
                worksheet.write(row, 15, "{:,.2f}".format(basded),main_cell_total) #BASDED
                worksheet.write(row, 16, "{:,.2f}".format(total_ded1_data),main_cell_total) #total deduction
                worksheet.write(row, 17, "{:,.2f}".format(total_ded2_data),main_cell_total) #total deduction
                worksheet.write(row, 18, "{:,.2f}".format(total_ded_data),main_cell_total) #total deduction

                worksheet.write(row, 19, "{:,.2f}".format(net_saled_data),main_cell_total) # Net Salary
                call = row + 3
                row += 4

            print("depp@@@@@@@@@@@@@@@@@@@@@@",depp)
            worksheet.write(row - 1, 0, "المجموع الكلي", main_cell_total_of_total) #day deduction

            worksheet.write(row - 1, 1, '',main_cell_total_of_total)

            worksheet.write(row - 1, 3, "{:,.2f}".format(day_deduction_total),main_cell_total_of_total) #day deduction
            worksheet.write(row - 1, 4, "{:,.2f}".format(day_deduction_amount_total),main_cell_total_of_total) #day deduction amount

            worksheet.write(row - 1, 5, "{:,.2f}".format(total_wage_total),main_cell_total_of_total) # wage

            worksheet.write(row - 1, 6, "{:,.2f}".format(total_basic_total),main_cell_total_of_total) #basic salary

            # worksheet.write(call, 4, 'Wage -الراتب الاسميUSD', header_bold)
            worksheet.write(row - 1, 7, "{:,.2f}".format(compensation_total),main_cell_total_of_total) #compensation

            worksheet.write(row - 1, 8, "{:,.2f}".format(allowance_total),main_cell_total_of_total) #allowance

            worksheet.write(row - 1, 9, "{:,.2f}".format(total_day_all_total),main_cell_total_of_total) #allowance
            worksheet.write(row - 1, 10, "{:,.2f}".format(total_aeaa_total),main_cell_total_of_total) #allowance

            worksheet.write(row - 1, 11, "{:,.2f}".format(total_entitlements_total),main_cell_total_of_total) #total of above 3

            # worksheet.write(call, 7, 'Basic', header_bold)
            worksheet.write(row - 1, 12, "{:,.2f}".format(socailsecurity_total),main_cell_total_of_total) #socaial security
            worksheet.write(row - 1, 13, "{:,.2f}".format(tax_total),main_cell_total_of_total) #tax
            worksheet.write(row - 1, 14, "{:,.2f}".format(reded_total),main_cell_total_of_total) #REDED
            worksheet.write(row - 1, 15, "{:,.2f}".format(basded_total),main_cell_total_of_total) #BASDED
            worksheet.write(row - 1, 16, "{:,.2f}".format(total_ded1_total),main_cell_total_of_total) #total deduction
            worksheet.write(row - 1, 17, "{:,.2f}".format(total_ded2_total),main_cell_total_of_total) #total deduction
            worksheet.write(row - 1, 18, "{:,.2f}".format(total_ded_total),main_cell_total_of_total) #total deduction
            worksheet.write(row - 1, 19, "{:,.2f}".format(net_saled_total),main_cell_total_of_total) # Net Salary

            call = row + 2 + 1
            row += 3 + 1
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

        # file_added = "/home/anuj/Desktop/workspace13/payslip_report.xlsx"
        # with open(file_added, "wb") as binary_file:
        #     binary_file.write(xlDecoded)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        download_url = '/web/content/' + str(ir_id.id) + '?download=true'
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }



class PayrollExcelBatch(models.Model):
    _inherit = 'res.partner'
    
    batch = fields.Char("Batch")

class PayrollExcel(models.Model):
    _inherit = 'hr.payslip.run'


    def send_mis_report(self):
        print("self@@@@@@@@@@@@@@",self)
        filename = 'Payslip.xls'
        string = 'Payslip_report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string)
        header_bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")
        cell_format = xlwt.easyxf()
        filename = 'Payslip_Report_%s.xls' % date.today()
        rested = self.env['hr.payslip'].search([])
        row = 1
        border_normal = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; font: bold on; pattern: pattern solid, fore_colour gray25;')
        border_1 = xlwt.easyxf('borders: left 1, right 1, top 1, bottom 1;')
        border_2 = xlwt.easyxf('borders: left 2, right 2, top 2, bottom 2;')
        border_color_2 = xlwt.easyxf('borders: top_color blue, bottom_color blue, right_color blue, left_color blue, left 2, right 2, top 2, bottom 2; font: bold on; pattern: pattern solid, fore_colour gray25;')
        worksheet.col(0).width = 10000
        worksheet.col(1).width = 15000
        worksheet.col(2).width = 10000
        worksheet.row(0).height = 500
        worksheet.write(0, 0, 'Reference', border_color_2)
        worksheet.write(0, 1, 'Payslip Name', border_color_2)

        worksheet.write(0, 2, 'Employe Name-اسم     الموظف', border_color_2)
        worksheet.write(0, 3, 'Description', header_bold)
        worksheet.write(0, 4, 'Wage -الراتب الاسميUSD', header_bold)
        worksheet.write(0, 5, 'Wage -الراتب الاسميIQD', header_bold)

        worksheet.write(0, 6, 'Basic Salary', header_bold)
        worksheet.write(0, 7, 'Compensation', header_bold)
        worksheet.write(0, 8, 'Basic', header_bold)
        worksheet.write(0, 9, 'Social Security', header_bold)
        worksheet.write(0, 10, 'TAX', header_bold)
        worksheet.write(0, 11, 'Day Deduction', header_bold)


        worksheet.write(0, 12, 'Allowance', header_bold)
        worksheet.write(0, 13, 'REDED', header_bold)
        worksheet.write(0, 14, 'BASEDED', header_bold)
        worksheet.write(0, 15, 'Total Deduction', header_bold)



        worksheet.write(0, 16, 'Net Salary', header_bold)
        # v.onboard_date >= (datetime.today().date().replace(day=1) - relativedelta(months=1)) and v.onboard_date <= (datetime.today().date() - relativedelta(months=1))
        for material_line_id in self.slip_ids:
            worksheet.write(row, 0, material_line_id.number or '')
            worksheet.write(row, 1, material_line_id.name or '')

            worksheet.write(row, 2, material_line_id.employee_id.name or '')
            worksheet.write(row, 3, material_line_id.employee_id.job_id.name or '')
            if material_line_id.contract_id.currency_id.id == 2:
                worksheet.write(row, 4, str(material_line_id.contract_id.wage) + "$" or '')

            if material_line_id.contract_id.currency_id.id == 90:
                worksheet.write(row, 5, str(material_line_id.contract_id.wage) + "ع.د" or '')

            for iit in material_line_id.line_ids:
                if iit.code == "CMPS":
                    worksheet.write(row, 6, iit.total or '')
                if iit.code == "WAG":    
                    worksheet.write(row, 7, iit.total or '')
                if iit.code == "SST":    
                    worksheet.write(row, 8, iit.total or '')
                if iit.code == "TAX":
                    worksheet.write(row, 9, iit.total or '')
                if iit.code == "day2":    
                    worksheet.write(row, 10, iit.total or '')
                if iit.code == "TRA"  or iit.code == "DAYALL"  or iit.code == "AEAA":    
                    worksheet.write(row, 11, iit.total or '')

                if iit.code == "REDED":    
                    worksheet.write(row, 12, iit.total or '')
                    
                if iit.code == "BASEDED":    
                    worksheet.write(row, 13, iit.total or '')
                    
                if iit.code == "TTD":    
                    worksheet.write(row, 14, iit.total or '')
                    

                if iit.code == "NET2" or iit.code == "GROSS" or iit.code == "NTS" or iit.code == "NETS" or iit.code == "AEAA":    
                    worksheet.write(row, 15, iit.total or '')
            row += 1
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

        # file_added = "/home/anuj/Desktop/workspace13/payslip_report.xlsx"
        # with open(file_added, "wb") as binary_file:
        #     binary_file.write(xlDecoded)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        download_url = '/web/content/' + str(ir_id.id) + '?download=true'
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }    

        