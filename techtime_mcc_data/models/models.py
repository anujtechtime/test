# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.http import request
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

import logging
_logger = logging.getLogger(__name__)


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

class techtime_mcc_data(models.Model):
    _name = 'techtime_mcc_data.techtime_mcc_data'
    _description = 'techtime_mcc_data.techtime_mcc_data'

    name = fields.Char("Year")

class techtime_new_data(models.Model):
    _name = 'new.work'
    _description = 'new.work'

    name = fields.Char("نافذة القبول")        

class DataDDFHrEmployee(models.Model):
    _inherit = "hr.employee"

    iban = fields.Char("IBAN")
    Account_number = fields.Char("Account Number")


    wedding_date = fields.Date("Wedding Date")
    date_divource = fields.Date("Date Divource")
    husband_id = fields.Char("Husband Id")
    date_of_death = fields.Date("Date_Of Death")
    house_wife = fields.Selection([('yes','Yes'),('no','No')], string="House Wife")
    husband_working = fields.Selection([('yes','Yes'),('no','No')], string="Husband Working")
    merge_salary = fields.Char("Merge Salary")
    field_1 = fields.Float("1أ ) مجموع الرواتب والاجور المدفوع خلال سنة")



    field_2 = fields.Float("1ب) مجموع المخصصات للملابس والسكن والاقامة والطعام والنقل والخطورة المدفوعة خلال  السنة بالنسبة لمستخدمي القطاع الخاص واجمالي المخصصات المستخدمة من قبل موظفي الدولة والقطاع العام والمختلط")
    field_3 = fields.Float("1 ج) مجموع المخصصات والمزايا الاخرى الخاضعة للضريبة المدفوعة خلال السنة ")
    field_4 = fields.Float("1د) مزايا عينية ")
    field_5 = fields.Float("1هـ) مكافئات مدفوعة للمنتسب ومدخولات اخرى من صاحب العمل")
    field_6 = fields.Float("1و) مدخولات اضافية من الاولاد ومن دمج دخل الزوجة (الزوج) عند تحقق الشروط")

    total_of_above_field = fields.Float("اجمالي الدخل (1)")

    field_7 = fields.Float("2أ) مجموع السماح القانوني . المستحق خلال السنة")
    field_8 = fields.Float("2ب) التوقيفات التقاعدية والضمان الاجتماعي المدفوع خلال السنة ")
    field_9 = fields.Float("2ج) التنزيلات الواردة في المادة ( الثامنة ) من قانون ضريبة الدخل رقم 113 لسنة 1982٭")
    field_10 = fields.Float("2د) المبلغ من (1ب) بما لايتجاوز 30%  من المبلغ في السطر (1أ)")

    total_of_above_2 = fields.Float("اجمالي التنزيلات  (2)")

    grand_total = fields.Float("جامعة المعقل الأهلية")

    @api.onchange('field_2','field_3','field_4','field_5','field_6')
    def _inverse_fields_data(self):
        for ddts in self:
            self.total_of_above_field = self.field_2 + self.field_3 + self.field_4 + self.field_5 + self.field_6

    @api.onchange('field_7', 'field_8', 'field_9', 'field_10')
    def _inverse_fields_data_2(self):
        for ddts in self:
            self.total_of_above_2 = self.field_7 + self.field_8 + self.field_9 + self.field_10    


    @api.onchange('total_of_above_field','total_of_above_2')
    def _inverse_total_of_above_field(self):
        for ddts in self:
            self.grand_total = self.total_of_above_field - self.total_of_above_2
    
            





class DataHrEmployee(models.Model):
    _inherit = "hr.job"

    sequence = fields.Char("Sequence")


class DataMphine(models.Model):
    _inherit = "res.partner"

    remark_data_change = fields.One2many("level.value","res_part",store = True)

    rfid = fields.Char("RFID")

    data_one = fields.Many2one("new.work", string="نافذة القبول")


    attachment = fields.Many2many("ir.attachment",  string="Attachment")

    year_of_acceptance_1 = fields.Many2one("techtime_mcc_data.techtime_mcc_data", string="Year of acceptance")
    file_upload = fields.Binary(string='File', attachment=True)
    attachment_upload = fields.Binary(string='Attachment', attachment=True)

    year_of_graduation = fields.Char("Year Of Graduation")
    academic_branch = fields.Char("Academi Branch")

    notes_data = fields.Text("Notes", track_visibility=True)
    data_date_value = fields.Date("Date", track_visibility=True)
    sequence_num = fields.Char("Sequence", track_visibility=True)


    field_one_1 = fields.Boolean("استضافة من الجامعة")
    fields_one_2 = fields.Boolean("استضافة الى الجامعة")


    def report_for_export_image(self):
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
        
        status_yu = ""

        row = 1
        call = 1
        worksheet = wb.add_sheet(string)
        worksheet.cols_right_to_left = True
        worksheet.col(0).width = 10000
        worksheet.col(1).width = 10000
        worksheet.col(2).width = 10000
        worksheet.col(3).width = 10000
        worksheet.col(4).width = 10000
        worksheet.col(5).width = 10000
        worksheet.col(6).width = 10000
        print("self@@@@@@@@@@@@@",self)

        # department_data = self.env["department.department"].search([])
        level_data = ["leve1","level2", "level3", "level4", "level5"]
        shift_data = ['morning', 'afternoon'] 
        level_name = ""
        worksheet.write(row, 0, 'أسم الطالب', header_bold)

        worksheet.write(row, 1, 'الحالة', header_bold)

        worksheet.write(row, 2, 'السنة الدراسية', header_bold)

        worksheet.write(row, 3, 'الكلية', header_bold)

        worksheet.write(row, 4, 'القسم', header_bold)

        worksheet.write(row, 5, "المرحلة ونوع الدراسة" , header_bold) 

        worksheet.write(row, 6, 'الرقم الجامعي', header_bold)

        worksheet.write(row, 7, 'RFID', header_bold)

        worksheet.write(row, 8, 'رقم الهوية', header_bold)

        worksheet.write(row, 9, 'المواليد', header_bold)

        worksheet.write(row, 10, 'الاسم بالانكليزية', header_bold)

        

        



        row = row + 1
        for lev in  level_data:
            for shift in shift_data:
                data_student = self.filtered(lambda picking: picking.level == lev and picking.shift == shift)
                print("data_student@@@@@@@@@@@@@@@@@@@@@@@@@",data_student)
                if lev == 'leve1':
                    depp = 'المرحلة الاولى'
                if lev == 'level2':
                    depp = 'المرحلة الثانية'
                if lev == 'level3':
                    depp = 'المرحلة الثالثة'
                if lev == 'level4':
                    depp = 'المرحلة الرابعة'
                if lev == 'level5':
                    depp = 'المرحلة الخامسة'


                if shift == 'morning':
                    shift_name = 'صباحي'
                if shift == 'afternoon':    
                    shift_name = 'مسائي'
                # worksheet.write(row, 0, "المرحلة ونوع الدراسة" , header_bold)  

                

                

                for res_partner in data_student:

                    if res_partner.Status == 'status4':
                        status_yu =  'مؤجل'
                    if res_partner.Status == 'status1':
                        status_yu = 'ترقين قيد'
                    if res_partner.Status == 'status2':
                        status_yu = 'طالب غير مباشر'
                    if res_partner.Status == 'status3':
                        status_yu = 'انسحاب'
                    if res_partner.Status == 'currecnt_student':
                        status_yu = 'طالب حالي'
                    if res_partner.Status == 'succeeded':
                        status_yu = 'طالب ناجح'
                    if res_partner.Status == 'failed':
                        status_yu = 'راسب'
                    if res_partner.Status == 'transferred_from_us':
                        status_yu = 'انتقل من جامعة المعقل '
                    if res_partner.Status == 'graduated':
                        status_yu = 'طالب متخرج'

                    # worksheet.write(row, 0, str(depp) + " - " + str(shift_name) , main_cell_total)

                    worksheet.write(row, 0, res_partner.display_name or '', main_cell_total)    #student 

                    worksheet.write(row, 1, status_yu or '', main_cell_total)  #status
                    worksheet.write(row, 2, res_partner.year.year or '', main_cell_total) 
                    worksheet.write(row, 3, res_partner.college.college or '', main_cell_total)
                    worksheet.write(row, 4, res_partner.department.department or '', main_cell_total)


                    worksheet.write(row, 5, str(depp) + " - " + str(shift_name) , main_cell_total)


                    worksheet.write(row, 6, res_partner.college_number or '', main_cell_total)
                    worksheet.write(row, 7, res_partner.rfid or '', main_cell_total)

                    worksheet.write(row, 8, res_partner.batch_number or '', main_cell_total)

                    worksheet.write(row, 9, res_partner.year_born or '', main_cell_total)

                    worksheet.write(row, 10, res_partner.name_english or '', main_cell_total)
                    row = row + 1
                # row = row + 1

            
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



    def send_mis_report_sale_student_data_report(self):  
        filename = 'جدول الاحصاء الصباحي.xls'
        string = 'جدول الاحصاء الصباحي.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string)
        worksheet.cols_right_to_left = True
        header_bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")
        cell_format = xlwt.easyxf()
        filename = 'Student_Report_%s.xls' % date.today()
        rested = self.env['sale.order'].search([])
        data_one = self.env["new.work"].search([])
        row = 1
        border_normal = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; font: bold on; pattern: pattern solid, fore_colour gray25;')
        border_1 = xlwt.easyxf('borders: left 1, right 1, top 1, bottom 1;')
        border_2 = xlwt.easyxf('borders: left 2, right 2, top 2, bottom 2;')
        border_color_2 = xlwt.easyxf('borders: top_color blue, bottom_color blue, right_color blue, left_color blue, left 2, right 2, top 2, bottom 2; font: bold on; pattern: pattern solid, fore_colour gray25;')
        # worksheet.col(0).width = 10000
        # worksheet.col(1).width = 15000
        # worksheet.col(2).width = 10000

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

        
        col = 0

        worksheet.write(0, 0, 'الكلية / القسم', header_bold) #Department
        worksheet.write(0, 1, 'المرحلة الدراسية', header_bold) #level
        worksheet.write(0, 2, 'نوع الدراسة', header_bold) #Shift

        worksheet.write(0, 3, 'الطلبة المقبولين/المسجلين', header_bold)  #Current students
        worksheet.write(0, 4, 'طالب حالي', header_bold) #Shift

        worksheet.write(0, 5, 'طالب غير مباشر', header_bold) #Status 3
        worksheet.write(0, 6, 'الطلبة المنسحبين ', header_bold) #status 4
        worksheet.write(0, 7, '  الطلبة المرقنين', header_bold) #status 2

        worksheet.write(0, 8, 'مؤجلين', header_bold) #status 2

        worksheet.write(0, 9, 'الطلبة الراسبين', header_bold) #failed
        worksheet.write(0, 10, 'نقل من الجامعة', header_bold) #trasferred from us
        worksheet.write(0, 11, 'نقل الى الجامعة', header_bold) #trasferred to us
        worksheet.write(0, 12, 'استضافة من الجامعة', header_bold) #new field
        worksheet.write(0, 13, 'استضافة الى الجامعة', header_bold) #new field
        worksheet.write(0, 14, 'الطلبة الفعليين', header_bold) #remaning status exept last 3 status- current students
        

        colld = 15
        for ddts in data_one:
            worksheet.write(0, colld, ddts.name, header_bold) #data_one
            colld = colld + 1

          
        worksheet.write(0, colld, 'ذكور', header_bold) #Male
        worksheet.write(0, colld + 1, 'اناث', header_bold) #Female
        worksheet.write(0, colld + 2, 'المجموع', header_bold) #Total Data_one 



        level_type = ['leve1','level2','level3','level4','level5']
        shift_data = ['morning', 'afternoon']
        lev_1 = ''
        shift_name = ''
        total_field_one_1 = 0
        total_fields_one_2 = 0

        department = self.env["department.department"].search([])
        for dept in department:
            depart_data  = self.filtered(lambda picking:picking.department.id == dept.id)
            if depart_data:
                # worksheet.write(row, 0, dept.department or '')
                if dept.department in  ("طب الاسنان", "الصيدلة"):
                    worksheet.write_merge(row, row + 4, 0, 0, dept.department, main_cell_total)
                elif dept.department not in  ("طب الاسنان", "الصيدلة"):
                    worksheet.write_merge(row, row + 9, 0, 0, dept.department, main_cell_total)
                total_of_currecnt = 0

                total_of_all_status = 0

                total_of_status_2 = 0
                total_of_status_3 = 0
                total_of_status_4 = 0
                total_of_status_5 = 0
                total_of_failed = 0
                total_transferred_from_us = 0
                total_transferred_to_us = 0
                total_total_of_all = 0
                total_gender_male_data = 0
                gender_female_data = 0
                total_gender_female_data = 0
                total_total_of_data_one = 0
                total_field_one_1 = 0
                total_fields_one_2 = 0
                

                for lev in level_type:
                    if lev == 'leve1':
                        lev_1 = 'المرحلة الاولى'
                    if lev == 'level2':
                        lev_1 = 'المرحلة الثانية'
                    if lev == 'level3':
                        lev_1 = 'المرحلة الثالثة'
                    if lev == 'level4':
                        lev_1 = 'المرحلة الرابعة'
                    if lev == 'level5':
                        lev_1 = 'المرحلة الخامسة'

                    # worksheet.write_merge(row, row + 1, 1, 1, lev_1, main_cell_total)
                    if dept.department in  ("طب الاسنان", "الصيدلة"):
                        worksheet.write_merge(row, row, 1, 1, lev_1, main_cell_total)  
                    elif dept.department not in  ("طب الاسنان", "الصيدلة"):
                        worksheet.write_merge(row, row + 1, 1, 1, lev_1, main_cell_total)    
                    # worksheet.write(row, 1, lev_1 or '')    

                    for shift in shift_data:
                        total_of_all = 0
                        last_three_status = 0


                        if dept.department in  ("طب الاسنان", "الصيدلة") and shift == "afternoon":
                            print("data")

                        else:    
                            if shift == 'morning':
                                shift_name = 'صباحي'
                            if shift == 'afternoon':    
                                shift_name = 'مسائي'


                            worksheet.write(row, 2, shift_name or '', main_cell_total)

                            all_status_data = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.shift == shift)

                            currecnt_status_data = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.shift == shift and picking.Status == "currecnt_student")

                            status_2_data = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.shift == shift and picking.Status == "status2")

                            status_3_data = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.shift == shift and picking.Status == "status3")


                            status_5_data = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.shift == shift and picking.Status == "status1")

                            status_4_data = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.shift == shift and picking.Status == "status4")


                            failed = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.shift == shift and picking.Status == "failed")

                            transferred_to_us = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.shift == shift and picking.transferred_to_us == True) 
                            transferred_from_us = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.shift == shift and picking.chckbox_data_2 == True)
                            print("currecnt_status_data@@@@@@@@@@@",currecnt_status_data)
                            print("row@@@@@@@@@@@@@@@",row)

                            worksheet.write(row, 3, len(all_status_data.mapped('id')) or '', main_cell_total)

                            total_of_all_status = total_of_all_status + len(all_status_data.mapped('id')) 

                            worksheet.write(row, 4, len(currecnt_status_data.mapped('id')) or '', main_cell_total)

                            total_of_currecnt = total_of_currecnt + len(currecnt_status_data.mapped('id'))


                            worksheet.write(row, 5, len(status_2_data.mapped('id')) or '', main_cell_total)

                            total_of_status_2 = total_of_status_2 + len(status_2_data.mapped('id'))

                            worksheet.write(row, 6, len(status_3_data.mapped('id')) or '', main_cell_total)

                            total_of_status_3 = total_of_status_3 + len(status_3_data.mapped('id'))
                            worksheet.write(row, 7, len(status_5_data.mapped('id')) or '', main_cell_total)

                            total_of_status_5 = total_of_status_5 + len(status_5_data.mapped('id'))

                            worksheet.write(row, 8, len(status_4_data.mapped('id')) or '', main_cell_total)

                            total_of_status_4 = total_of_status_4 + len(status_4_data.mapped('id'))



                            worksheet.write(row, 9, len(failed.mapped('id')) or '', main_cell_total)

                            total_of_failed = total_of_failed + len(failed.mapped('id'))



                            worksheet.write(row, 10, len(transferred_from_us.mapped('id')) or '', main_cell_total)
                            total_transferred_from_us = total_transferred_from_us + len(transferred_from_us.mapped('id'))

                            worksheet.write(row, 11, len(transferred_to_us.mapped('id')) or '', main_cell_total)
                            total_transferred_to_us = total_transferred_to_us + len(transferred_to_us.mapped('id'))

                            field_one_1 = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.shift == shift and picking.field_one_1 == True) 
                            worksheet.write(row, 12, len(field_one_1.mapped('id')) or '', main_cell_total)
                            total_field_one_1 = total_field_one_1 + len(field_one_1.mapped('id'))
                            
                            fields_one_2 = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.shift == shift and picking.fields_one_2 == True)
                            worksheet.write(row, 13, len(fields_one_2.mapped('id')) or '', main_cell_total)

                            total_fields_one_2 = total_fields_one_2 + len(fields_one_2.mapped('id'))

                            last_three_status = len(status_2_data.mapped('id')) + len(status_3_data.mapped('id')) + len(status_5_data.mapped('id')) + len(failed.mapped('id')) + len(status_4_data.mapped('id')) 

                            total_of_all = len(all_status_data.mapped('id')) - last_three_status

                            total_total_of_all = total_total_of_all + total_of_all


                            worksheet.write(row, 14, len(currecnt_status_data.mapped('id')), main_cell_total)

                            total_of_data_one = 0
                            colld = 15
                            for ddts in data_one:
                                data_one_data = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.shift == shift and picking.data_one.id == ddts.id and picking.Status == "currecnt_student")  
                                # data_one_data_fields_one_2 = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.shift == shift and picking.data_one.id == ddts.id and picking.fields_one_2 == True and picking.transferred_to_us == True and picking.Status == "currecnt_student" and picking.chckbox_data_2 == False)  
                                worksheet.write(row, colld, len(data_one_data.mapped("id")), main_cell_total) #data_one
                                total_of_data_one = total_of_data_one + len(data_one_data.mapped("id"))
                                colld = colld + 1

                            gender_male_data = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.shift == shift and picking.gender == 'male' and picking.Status == "currecnt_student")
                            worksheet.write(row, colld, len(gender_male_data.mapped("id")), main_cell_total)
                            total_gender_male_data = total_gender_male_data + len(gender_male_data.mapped("id"))

                            gender_female_data = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.shift == shift and picking.gender == 'female' and  picking.Status == "currecnt_student") 
                            worksheet.write(row, colld + 1, len(gender_female_data.mapped("id")), main_cell_total)

                            total_gender_female_data = total_gender_female_data + len(gender_female_data.mapped("id"))

                            worksheet.write(row, colld + 2, total_of_data_one, main_cell_total)

                            total_total_of_data_one = total_total_of_data_one + total_of_data_one  

                            row = row + 1

                # worksheet.write(row, 0, )
                worksheet.write_merge(row, row, 0, 2, "المجمــــــــــــــــــــــــــــــــوع", main_cell_total_of_total)  

                worksheet.write(row, 3, total_of_all_status, main_cell_total_of_total)

                worksheet.write(row, 4, total_of_currecnt, main_cell_total_of_total)

                worksheet.write(row, 5, total_of_status_2, main_cell_total_of_total)
                worksheet.write(row, 6, total_of_status_3, main_cell_total_of_total)
                worksheet.write(row, 7, total_of_status_5, main_cell_total_of_total)
                worksheet.write(row, 8, total_of_status_4, main_cell_total_of_total)
                worksheet.write(row, 9, total_of_failed, main_cell_total_of_total)
                worksheet.write(row, 10, total_transferred_from_us, main_cell_total_of_total)
                worksheet.write(row, 11, total_transferred_to_us, main_cell_total_of_total)
                worksheet.write(row, 12, total_field_one_1, main_cell_total_of_total)
                worksheet.write(row, 13, total_fields_one_2, main_cell_total_of_total)
                worksheet.write(row, 14, total_of_currecnt, main_cell_total_of_total)
                colld = 15
                for ddts in data_one:
                    ttl_data_one_data = self.filtered(lambda picking:picking.department.id == dept.id and picking.data_one.id == ddts.id)
                    worksheet.write(row, colld,len(ttl_data_one_data.mapped("id")) , main_cell_total_of_total)

                    colld = colld + 1
                worksheet.write(row, colld, total_gender_male_data, main_cell_total_of_total)
                worksheet.write(row, colld + 1, total_gender_female_data, main_cell_total_of_total)
                worksheet.write(row, colld + 2, total_total_of_data_one, main_cell_total_of_total)
                
                row = row + 1
            row = row + 1
        # row = row + 1
        worksheet.write_merge(row, row + 3, 0, 0, 'الكليات', main_cell_total)

        for lev in level_type:
            if lev == 'leve1':
                lev_1 = 'المرحلة الاولى'
            if lev == 'level2':
                lev_1 = 'المرحلة الثانية'
            if lev == 'level3':
                lev_1 = 'المرحلة الثالثة'
            if lev == 'level4':
                lev_1 = 'المرحلة الرابعة'
            if lev == 'level5':
                lev_1 = 'المرحلة الخامسة'


                


            worksheet.write(row, 1, lev_1 or '', main_cell_total)
            worksheet.write(row, 2, "صباحي / مسائي" or '', main_cell_total)

            all_status_data_1 = self.filtered(lambda picking:picking.level == lev)

            currecnt_status_data_1 = self.filtered(lambda picking:picking.level == lev and picking.Status == 'currecnt_student')

            status_2_data_1 = self.filtered(lambda picking:picking.level == lev and picking.Status == 'status2') 

            status_3_data_1 = self.filtered(lambda picking:picking.level == lev and picking.Status == 'status3') 

            status_4_data_1 = self.filtered(lambda picking:picking.level == lev and picking.Status == 'status4') 


            status_5_data_1 =  self.filtered(lambda picking:picking.level == lev and picking.Status == 'status1') 
            failed_1 = self.filtered(lambda picking:picking.level == lev and picking.Status == 'failed') 

            transferred_to_us_1 =  self.filtered(lambda picking:picking.level == lev and picking.transferred_to_us == True)
            transferred_from_us_1 = self.filtered(lambda picking:picking.level == lev and picking.chckbox_data_2 == True) 

            worksheet.write(row, 3, len(all_status_data_1.mapped('id')) or '', main_cell_total)

            worksheet.write(row, 4, len(currecnt_status_data_1.mapped('id')) or '', main_cell_total)

            worksheet.write(row, 5, len(status_2_data_1.mapped('id')) or '', main_cell_total)

            worksheet.write(row, 6, len(status_3_data_1.mapped('id')) or '', main_cell_total)

            worksheet.write(row, 7, len(status_5_data_1.mapped('id')) or '', main_cell_total)

            worksheet.write(row, 8, len(status_4_data_1.mapped('id')) or '', main_cell_total)

            worksheet.write(row, 9, len(failed_1.mapped('id')) or '', main_cell_total)


            worksheet.write(row, 10, len(transferred_from_us_1.mapped('id')) or '', main_cell_total)

            worksheet.write(row, 11, len(transferred_to_us_1.mapped('id')) or '', main_cell_total)

            field_one_1 =  self.filtered(lambda picking:picking.level == lev and picking.field_one_1 == True) 
            worksheet.write(row, 12, len(field_one_1.mapped('id')) or '', main_cell_total)
            total_field_one_1 = total_field_one_1 + len(field_one_1.mapped('id'))
            
            fields_one_2 = self.filtered(lambda picking:picking.level == lev and picking.fields_one_2 == True) 
            worksheet.write(row, 13, len(fields_one_2.mapped('id')) or '', main_cell_total)

            total_fields_one_2 = total_fields_one_2 + len(fields_one_2.mapped('id'))


            last_three_status_1 = len(status_2_data_1.mapped('id')) + len(status_3_data_1.mapped('id')) + len(status_5_data_1.mapped('id')) + len(status_4_data_1.mapped('id'))

            total_of_all_1 = len(all_status_data_1.mapped('id')) - last_three_status_1


            worksheet.write(row, 14, len(currecnt_status_data_1.mapped('id')) or '', main_cell_total)


            total_of_data_one_1 = 0
            colld = 15
            for ddts in data_one:
                data_one_data_1 = self.filtered(lambda picking:picking.level == lev and picking.data_one.id == ddts.id) 
                worksheet.write(row, colld, len(data_one_data_1.mapped("id")), main_cell_total) #data_one
                total_of_data_one_1 = total_of_data_one_1 + len(data_one_data_1.mapped("id"))
                colld = colld + 1

            gender_female_data_1 = self.filtered(lambda picking:picking.level == lev and picking.gender == 'male')
            worksheet.write(row, colld, len(gender_female_data_1.mapped("id")), main_cell_total)

            gender_female_data_1 = self.filtered(lambda picking:picking.level == lev and picking.gender == 'female')
            worksheet.write(row, colld + 1, len(gender_female_data_1.mapped("id")), main_cell_total)


            worksheet.write(row, colld + 2, total_of_data_one_1, main_cell_total)
            print("row$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",row)
            row = row + 1

        
        currecnt_status_data_2 = self.filtered(lambda picking:picking.Status == "currecnt_student")

        status_2_data_2 = self.filtered(lambda picking:picking.Status == "status2")

        status_3_data_2 = self.filtered(lambda picking:picking.Status == "status3")


        status_4_data_2 = self.filtered(lambda picking:picking.Status == "status4")


        status_5_data_2 = self.filtered(lambda picking:picking.Status == "status1")
        failed_2 = self.filtered(lambda picking:picking.Status == "failed")

        transferred_to_us_2 =  self.filtered(lambda picking:picking.transferred_to_us == True)
        transferred_from_us_2 = self.filtered(lambda picking:picking.chckbox_data_2 == True)

        worksheet.write_merge(row, row, 0, 2, "المجمــــــــــــــــــــــــــــــــوع", main_cell_total_of_total)

        worksheet.write(row, 3, len(self.mapped('id')) or '', main_cell_total_of_total)

        worksheet.write(row, 4, len(currecnt_status_data_2.mapped('id')) or '', main_cell_total_of_total)

        worksheet.write(row, 5, len(status_2_data_2.mapped('id')) or '', main_cell_total_of_total)

        worksheet.write(row, 6, len(status_3_data_2.mapped('id')) or '', main_cell_total_of_total)

        worksheet.write(row, 7, len(status_4_data_2.mapped('id')) or '', main_cell_total_of_total)

        worksheet.write(row, 8, len(status_5_data_2.mapped('id')) or '', main_cell_total_of_total)


        worksheet.write(row, 9, len(failed_2.mapped('id')) or '', main_cell_total_of_total)


        worksheet.write(row, 10, len(transferred_from_us_2.mapped('id')) or '', main_cell_total_of_total)

        worksheet.write(row, 11, len(transferred_to_us_2.mapped('id')) or '', main_cell_total_of_total)


        field_one_1_2 = self.filtered(lambda picking:picking.field_one_1 == True)
        worksheet.write(row, 12, len(field_one_1_2.mapped('id')) or '', main_cell_total_of_total)
        
        fields_one_2_2 =  self.filtered(lambda picking:picking.fields_one_2 == True)
        worksheet.write(row, 13, len(fields_one_2_2.mapped('id')) or '', main_cell_total_of_total)




        last_three_status_2 = len(status_2_data_2.mapped('id')) + len(status_3_data_2.mapped('id')) + len(status_5_data_2.mapped('id')) + len(status_4_data_2.mapped('id'))

        total_of_all_2 = len(self.mapped('id')) - last_three_status_2


        worksheet.write(row, 14, len(currecnt_status_data_2.mapped('id')) or '', main_cell_total_of_total)


        total_of_data_one_2 = 0
        colld = 15
        for ddts in data_one:
            data_one_data_2 = self.filtered(lambda picking:picking.data_one.id == ddts.id)
            worksheet.write(row, colld, len(data_one_data_2.mapped("id")), main_cell_total_of_total) #data_one
            total_of_data_one_2 = total_of_data_one_2 + len(data_one_data_2.mapped("id"))
            colld = colld + 1

        gender_female_data_2 =  self.filtered(lambda picking:picking.gender == 'male')
        worksheet.write(row, colld, len(gender_female_data_2.mapped("id")), main_cell_total_of_total)

        gender_female_data_2 =  self.filtered(lambda picking:picking.gender == 'female')
        worksheet.write(row, colld + 1, len(gender_female_data_2.mapped("id")), main_cell_total_of_total)


        worksheet.write(row, colld + 2, total_of_data_one_2, main_cell_total_of_total)
        print("row$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",row)
        row = row + 1    



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



    def get_college_data(self):
        print("self################",self)
        print("request@@@@@@@@@@@@@@@",request)
        dct = {}

        college_value = request.env["faculty.faculty"].sudo().search([])
        print("college_value@@@@@@@@@@",college_value)
        dicts = []
        for coll in college_value:
            dct = {
            'college_name' : coll.college,
            'college_id' : coll.id
            }
            dicts.append(dct)
        return dicts

    def get_new_data(self):
        print("self################",self)
        print("request@@@@@@@@@@@@@@@",request)
        dct = {}

        college_value = request.env["new.work"].sudo().search([])
        print("college_value@@@@@@@@@@",college_value)
        dicts = []
        for coll in college_value:
            dct = {
            'new_name' : coll.name,
            'new_id' : coll.id
            }
            dicts.append(dct)
        return dicts    

    def get_year_acceptance_data(self):
        print("self################",self)
        print("request@@@@@@@@@@@@@@@",request)
        dct = {}

        college_value = request.env["techtime_mcc_data.techtime_mcc_data"].sudo().search([])
        print("college_value@@@@@@@@@@",college_value)
        dicts = []
        for coll in college_value:
            dct = {
            'year_acceptance_name' : coll.name,
            'year_acceptance_id' : coll.id
            }
            dicts.append(dct)
        return dicts

    def get_student_type_data(self):
        print("self################",self)
        print("request@@@@@@@@@@@@@@@",request)
        dct = {}

        college_value = request.env["level.level"].sudo().search([])
        print("college_value@@@@@@@@@@",college_value)
        dicts = []
        for coll in college_value:
            dct = {
            'student_name' : coll.Student,
            'student_id' : coll.id
            }
            dicts.append(dct)
        return dicts    


    def get_department_data(self):
        print("self################",self)
        print("request@@@@@@@@@@@@@@@",request)
        dct = {}

        college_value = request.env["department.department"].sudo().search([])
        print("college_value@@@@@@@@@@",college_value)
        dicts = []
        for coll in college_value:
            dct = {
            'department_name' : coll.department,
            'department_id' : coll.id
            }
            dicts.append(dct)
        return dicts 

    def get_year_data(self):
        print("self################",self)
        print("request@@@@@@@@@@@@@@@",request)
        dct = {}

        college_value = request.env["year.year"].sudo().search(['|',('active','=',True),('active','=',False)])
        print("college_value@@@@@@@@@@",college_value)
        dicts = []
        for coll in college_value:
            dct = {
            'year_name' : coll.year,
            'year_id' : coll.id
            }
            dicts.append(dct)
        return dicts        

class CrmTeamDateAccount(models.Model):

    _inherit = "purchase.order.line"

    qty_received = fields.Float("Received Qty", related="product_qty", inverse='_inverse_qty_received', compute_sudo=True, store=True, digits='Product Unit of Measure')


class DataLevelValueData(models.TransientModel):
    _inherit = 'level.value'


    res_part = fields.Many2one("res.partner")   
    notes_data = fields.Text("Notes", track_visibility=True)
    data_date_value = fields.Date("Date", track_visibility=True)
    sequence_num = fields.Char("Sequence", track_visibility=True)
    attachment = fields.Many2many("ir.attachment",  string="Attachment")

    Status = fields.Selection([('currecnt_student','Current student'),('succeeded','Succeeded'),('failed','Falied'),('transferred_from_us','Transferred From Us'),('graduated','Graduated')], string="Status")
    contact_type = fields.Selection([("student","طالب"),("teacher", "مدرس")], string="Contact Type", tracking=True)

    def action_confirm_change_level(self):
        print("res@@@@@@@@@@@@@@@@@@@@@@@@@@26666",self._context.get("active_id"))
        for idds in self._context.get("active_id"):
            print("idds@@@@@@@@@@@@@@@@@",idds)
            levels_sale_order = self.env["res.partner"].browse(int(idds))
            # print("levels_sale_order@@@@@@@@@@@@@@@@@@@@@@@@",levels_sale_order)
            _logger.info("eeeeeeeeeeeeeeeeeeee************11111111111111#####**%s" %self.id)
            # levels_sale_order.remark_data_change  = (4, self.id)
            self.res_part = levels_sale_order.id
            if self.level:
                levels_sale_order.level = self.level
                # levels_sale_order.partner_id.level = self.level

            if self.year:    
                levels_sale_order.year = self.year
                # levels_sale_order.partner_id.year = self.year

            if self.Status:    
                levels_sale_order.Status = self.Status
                # levels_sale_order.partner_id.Status = self.Status
                
            if self.contact_type:
                levels_sale_order.contact_type = self.contact_type
            if self.notes_data:
                levels_sale_order.notes_data = self.notes_data
            if self.data_date_value:
                levels_sale_order.data_date_value = self.data_date_value
            if self.sequence_num:
                levels_sale_order.sequence_num = self.sequence_num

            if self.attachment:
                levels_sale_order.attachment =  [(6, 0, self.attachment.mapped("id"))]
                # for pdf in self.attachment:
                #     attachments.append(pdf.id)

                levels_sale_order.message_post(attachment_ids=self.attachment.mapped("id"))           

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

    compensation1 = fields.Float("Compensation One")

    training_field = fields.Float("Training")


    married_with_house_wife = fields.Boolean("Married Male with house wife")
    married_with_working_wife = fields.Boolean("Married Male with working wife")

    married_with_non_working_husband = fields.Boolean("Married Female with non-working husband")
    married_with_working_husband = fields.Boolean("Married Female with working husband")



    single_male = fields.Boolean("Single Male")

    male_female_with_children = fields.Integer("Female with No. of children")

    divorced_male = fields.Boolean("Divorced Male")

    # sinle_female = fields.Boolean("Single Female")

    divorced_female = fields.Boolean("Divorced Female")

    if_age_is_above_63 = fields.Boolean("Age is above 63")

    tota_before = fields.Float("Total after")

    total_salary = fields.Float("Total Salary")



    # tax = fields.Float("Tax")
    # tax_other = fields.Float("Tax Other")
    # traning = fields.Float("Traning")
    # allowance = fields.Float("Allowance")
    day_deduction = fields.Float("Day-Deduction")

    basic_salary_one = fields.Float("Basic Salary")
    compensation_one = fields.Float("Compensation")

    # result = 0
    # if inputs.deductiondays and inputs.deductiondays.amount:
    #  result = contract.compensation1 - (contract.wage / 30 * inputs.deductiondays.amount)
    # if result < 0:
    #  result = contract.basic_salary - (contract.wage / 30 * inputs.deductiondays.amount)

    def change_the_day_deduction(self):
        for ddt in self:
            ddt.day_deduction = 0
            ddt._inverse_wage()


    @api.onchange('wage','compensation','day_deduction','social_security','married_with_house_wife','married_with_working_wife','married_with_non_working_husband','married_with_working_husband','single_male','male_female_with_children','divorced_male','sinle_female','divorced_female','if_age_is_above_63')
    def _inverse_wage(self):
        self.total_salary = 0
        if self.wage and self.day_deduction < 30:
            self.basic_salary = float(self.wage) * 0.77 - (((self.wage/30) * self.day_deduction) * 0.77)
            self.compensation = float(self.wage) * 0.23  - (((self.wage/30) * self.day_deduction) * 0.23) 
            self.basic_salary_one = float(self.wage) * 0.77 - (((self.wage/30) * self.day_deduction) * 0.77)
            self.compensation_one = float(self.wage) * 0.23  - (((self.wage/30) * self.day_deduction) * 0.23)
            self.social_security = float(self.basic_salary) * 0.05 
            self.compensation1 = float(self.wage) * 0.23  - (((self.wage/30) * self.day_deduction) * 0.23)
            if self.employ_type != 'option1':
                self.total_salary = self.social_security + self.compensation
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
                    self.total_salary = self.total_salary + self.male_female_with_children * 16666    
    
                if self.divorced_male:
                    self.total_salary = self.total_salary + 208333 # 

                if self.divorced_female:
                    self.total_salary = self.total_salary + 266666
                
                if self.if_age_is_above_63:
                    self.total_salary = self.total_salary + 25000  

            if self.employ_type == 'option1':
                self.total_salary = self.compensation
                if self.married_with_house_wife:
                    self.total_salary = self.compensation + 375000
                if self.married_with_working_wife:
                    self.total_salary = self.compensation + 208333
                if self.married_with_non_working_husband:
                    self.total_salary = self.compensation + 416666
                if self.married_with_working_husband:
                    self.total_salary = self.compensation + 208333  # 828,000.00 + 208333 = 1036333
                if self.single_male:
                    self.total_salary = self.compensation + 208333 

                if self.male_female_with_children: # 0 + 16666 = 16666
                    self.total_salary = self.total_salary + self.male_female_with_children * 16666   
                if self.divorced_male:
                    self.total_salary = self.total_salary + 208333 

                if self.divorced_female:
                    self.total_salary = self.total_salary + 266666
                
                if self.if_age_is_above_63:
                    self.total_salary = self.total_salary + 25000     
            



            value_data = self.basic_salary + self.compensation - self.total_salary 

            if value_data > 1000000:
                self.tota_before =  ((value_data - 83333) * 0.15) + 5833 #((2563667 - 83333) * 0.15) + 5833 = 377883.1

            if value_data > 500000 and value_data <= 1000000:
                self.tota_before =  ((value_data - 41666) * 0.10) + 1666

            if value_data > 250000 and value_data <= 500000:
                self.tota_before =  ((value_data - 20833) * 0.05) + 625 

            if value_data > 0 and value_data <= 250000:
                self.tota_before =  value_data * 0.03  

        else:
            self.total_salary = 0 
            self.tota_before = 0 
            self.basic_salary = 0
            self.compensation = 0
            self.social_security = 0
            self.compensation1 = 0                    


class CrmTeamSaleOrderccount(models.Model):

    _inherit = "sale.order"

    invoice_count_new = fields.Integer("Invoice data New ", readonly=False)

    @api.onchange('invoice_count_new','invoice_count')
    def _inverse_invoice_count_new(self):
        _logger.info("eeeeeeeeeeeeeeeeeeee************11111111111111#####**%s" %self)
        for ddts in self:
            ddts.invoice_count_new = ddts.invoice_count

    def send_mis_report_sale_student_data_report(self):  
        filename = 'جدول الاحصاء الصباحي.xls'
        string = 'جدول الاحصاء الصباحي.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string)
        worksheet.cols_right_to_left = True
        header_bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")
        cell_format = xlwt.easyxf()
        filename = 'Student_Report_%s.xls' % date.today()
        rested = self.env['sale.order'].search([])
        data_one = self.env["new.work"].search([])
        row = 1
        border_normal = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; font: bold on; pattern: pattern solid, fore_colour gray25;')
        border_1 = xlwt.easyxf('borders: left 1, right 1, top 1, bottom 1;')
        border_2 = xlwt.easyxf('borders: left 2, right 2, top 2, bottom 2;')
        border_color_2 = xlwt.easyxf('borders: top_color blue, bottom_color blue, right_color blue, left_color blue, left 2, right 2, top 2, bottom 2; font: bold on; pattern: pattern solid, fore_colour gray25;')
        # worksheet.col(0).width = 10000
        # worksheet.col(1).width = 15000
        # worksheet.col(2).width = 10000

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

        
        col = 0

        worksheet.write(0, 0, 'الكلية / القسم', header_bold) #Department
        worksheet.write(0, 1, 'المرحلة الدراسية', header_bold) #level
        worksheet.write(0, 2, 'نوع الدراسة', header_bold) #Shift
        worksheet.write(0, 3, 'الطلبة المقبولين/المسجلين', header_bold)  #Current students
        worksheet.write(0, 4, 'طالب غير مباشر', header_bold) #Status 3
        worksheet.write(0, 5, 'الطلبة المنسحبين', header_bold) #status 4
        worksheet.write(0, 6, 'مؤجلين  الطلبة المرقنين', header_bold) #status 2
        worksheet.write(0, 7, 'الطلبة الراسبين', header_bold) #failed
        worksheet.write(0, 8, 'نقل من الجامعة', header_bold) #trasferred from us
        worksheet.write(0, 9, 'نقل الى الجامعة', header_bold) #trasferred to us
        worksheet.write(0, 10, 'استضافة من الجامعة', header_bold) #new field
        worksheet.write(0, 11, 'استضافة الى الجامعة', header_bold) #new field
        worksheet.write(0, 12, 'الطلبة الفعليين', header_bold) #remaning status exept last 3 status- current students
        

        colld = 13
        for ddts in data_one:
            worksheet.write(0, colld, ddts.name, header_bold) #data_one
            colld = colld + 1

          
        worksheet.write(0, colld, 'ذكور', header_bold) #Male
        worksheet.write(0, colld + 1, 'اناث', header_bold) #Female
        worksheet.write(0, colld + 2, 'المجموع', header_bold) #Total Data_one 



        level_type = ['leve1','level2','level3','level4']
        shift_data = ['morning', 'afternoon']
        lev_1 = ''
        shift_name = ''

        department = self.env["department.department"].search([])
        for dept in department:
            depart_data  = self.filtered(lambda picking:picking.department.id == dept.id)
            if depart_data:
                # worksheet.write(row, 0, dept.department or '')
                if dept.department in  ("طب الاسنان", "الصيدلة"):
                    worksheet.write_merge(row, row + 3, 0, 0, dept.department, main_cell_total)
                elif dept.department not in  ("طب الاسنان", "الصيدلة"):
                    worksheet.write_merge(row, row + 7, 0, 0, dept.department, main_cell_total)
                total_of_currecnt = 0

                total_of_status_2 = 0
                total_of_status_4 = 0
                total_of_status_5 = 0
                total_of_failed = 0
                total_transferred_from_us = 0
                total_transferred_to_us = 0
                total_total_of_all = 0
                total_gender_male_data = 0
                gender_female_data = 0
                total_gender_female_data = 0
                total_total_of_data_one = 0
                total_field_one_1 = 0
                total_fields_one_2 = 0
                

                for lev in level_type:
                    if lev == 'leve1':
                        lev_1 = 'المرحلة الاولى'
                    if lev == 'level2':
                        lev_1 = 'المرحلة الثانية'
                    if lev == 'level3':
                        lev_1 = 'المرحلة الثالثة'
                    if lev == 'level4':
                        lev_1 = 'المرحلة الرابعة'
                    if lev == 'level5':
                        lev_1 = 'المرحلة الخامسة'

                    # worksheet.write_merge(row, row + 1, 1, 1, lev_1, main_cell_total)
                    if dept.department in  ("طب الاسنان", "الصيدلة"):
                        worksheet.write_merge(row, row, 1, 1, lev_1, main_cell_total)  
                    elif dept.department not in  ("طب الاسنان", "الصيدلة"):
                        worksheet.write_merge(row, row + 1, 1, 1, lev_1, main_cell_total)    
                    # worksheet.write(row, 1, lev_1 or '')    

                    for shift in shift_data:
                        total_of_all = 0
                        last_three_status = 0


                        if dept.department in  ("طب الاسنان", "الصيدلة") and shift == "afternoon":
                            print("data")

                        else:    
                            if shift == 'morning':
                                shift_name = 'صباحي'
                            if shift == 'afternoon':    
                                shift_name = 'مسائي'


                            worksheet.write(row, 2, shift_name or '', main_cell_total)

                            currecnt_status_data = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.Subject == shift and picking.Status == "currecnt_student")

                            status_2_data = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.Subject == shift and picking.Status == "status2")

                            status_4_data = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.Subject == shift and picking.Status == "status3")


                            status_5_data = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.Subject == shift and picking.Status == "status1")
                            failed = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.Subject == shift and picking.Status == "failed")

                            transferred_to_us = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.Subject == shift and picking.partner_id.transferred_to_us == True) 
                            transferred_from_us = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.Subject == shift and picking.partner_id.transfer_shift == True)
                            print("currecnt_status_data@@@@@@@@@@@",currecnt_status_data)
                            print("row@@@@@@@@@@@@@@@",row)
                            worksheet.write(row, 3, len(currecnt_status_data.mapped('id')) or '', main_cell_total)

                            total_of_currecnt = total_of_currecnt + len(currecnt_status_data.mapped('id'))


                            worksheet.write(row, 4, len(status_2_data.mapped('id')) or '', main_cell_total)

                            total_of_status_2 = total_of_status_2 + len(status_2_data.mapped('id'))

                            worksheet.write(row, 5, len(status_4_data.mapped('id')) or '', main_cell_total)

                            total_of_status_4 = total_of_status_4 + len(status_4_data.mapped('id'))
                            worksheet.write(row, 6, len(status_5_data.mapped('id')) or '', main_cell_total)

                            total_of_status_5 = total_of_status_5 + len(status_5_data.mapped('id'))



                            worksheet.write(row, 7, len(failed.mapped('id')) or '', main_cell_total)

                            total_of_failed = total_of_failed + len(failed.mapped('id'))



                            worksheet.write(row, 8, len(transferred_from_us.mapped('id')) or '', main_cell_total)
                            total_transferred_from_us = total_transferred_from_us + len(transferred_from_us.mapped('id'))

                            worksheet.write(row, 9, len(transferred_to_us.mapped('id')) or '', main_cell_total)
                            total_transferred_to_us = total_transferred_to_us + len(transferred_to_us.mapped('id'))

                            field_one_1 = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.Subject == shift and picking.partner_id.field_one_1 == True) 
                            worksheet.write(row, 10, len(field_one_1.mapped('id')) or '', main_cell_total)
                            total_field_one_1 = total_field_one_1 + len(field_one_1.mapped('id'))
                            
                            fields_one_2 = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.Subject == shift and picking.partner_id.fields_one_2 == True)
                            worksheet.write(row, 11, len(fields_one_2.mapped('id')) or '', main_cell_total)

                            total_fields_one_2 = total_fields_one_2 + len(fields_one_2.mapped('id'))

                            last_three_status = len(status_2_data.mapped('id')) + len(status_4_data.mapped('id')) + len(status_5_data.mapped('id'))

                            total_of_all = len(currecnt_status_data.mapped('id')) - last_three_status

                            total_total_of_all = total_total_of_all + total_of_all


                            worksheet.write(row, 12, total_of_all or '', main_cell_total)

                            total_of_data_one = 0
                            colld = 13
                            for ddts in data_one:
                                data_one_data = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.Subject == shift and picking.partner_id.data_one.id == ddts.id)
                                worksheet.write(row, colld, len(data_one_data.mapped("id")), main_cell_total) #data_one
                                total_of_data_one = total_of_data_one + len(data_one_data.mapped("id"))
                                colld = colld + 1

                            gender_male_data = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.Subject == shift and picking.partner_id.gender == 'male')
                            worksheet.write(row, colld, len(gender_male_data.mapped("id")), main_cell_total)
                            total_gender_male_data = total_gender_male_data + len(gender_male_data.mapped("id"))

                            gender_female_data = self.filtered(lambda picking:picking.level == lev and picking.department.id == dept.id and picking.Subject == shift and picking.partner_id.gender == 'female') 
                            worksheet.write(row, colld + 1, len(gender_female_data.mapped("id")), main_cell_total)

                            total_gender_female_data = total_gender_female_data + len(gender_female_data.mapped("id"))

                            worksheet.write(row, colld + 2, total_of_data_one, main_cell_total)

                            total_total_of_data_one = total_total_of_data_one + total_of_data_one  

                            row = row + 1

                # worksheet.write(row, 0, )
                worksheet.write_merge(row, row, 0, 2, "المجمــــــــــــــــــــــــــــــــوع", main_cell_total_of_total)  
                worksheet.write(row, 3, total_of_currecnt, main_cell_total_of_total)

                worksheet.write(row, 4, total_of_status_2, main_cell_total_of_total)
                worksheet.write(row, 5, total_of_status_4, main_cell_total_of_total)
                worksheet.write(row, 6, total_of_status_5, main_cell_total_of_total)
                worksheet.write(row, 7, total_of_failed, main_cell_total_of_total)
                worksheet.write(row, 8, total_transferred_from_us, main_cell_total_of_total)
                worksheet.write(row, 9, total_transferred_to_us, main_cell_total_of_total)
                worksheet.write(row, 10, total_field_one_1, main_cell_total_of_total)
                worksheet.write(row, 11, total_fields_one_2, main_cell_total_of_total)
                worksheet.write(row, 12, total_total_of_all, main_cell_total_of_total)
                colld = 13
                for ddts in data_one:
                    ttl_data_one_data = self.filtered(lambda picking:picking.department.id == dept.id and picking.partner_id.data_one.id == ddts.id)
                    worksheet.write(row, colld,len(ttl_data_one_data.mapped("id")) , main_cell_total_of_total)

                    colld = colld + 1
                worksheet.write(row, colld, total_gender_male_data, main_cell_total_of_total)
                worksheet.write(row, colld + 1, total_gender_female_data, main_cell_total_of_total)
                worksheet.write(row, colld + 2, total_total_of_data_one, main_cell_total_of_total)
                
                row = row + 1
            row = row + 1
        # row = row + 1
        worksheet.write_merge(row, row + 3, 0, 0, 'الكليات', main_cell_total)

        for lev in level_type:
            if lev == 'leve1':
                lev_1 = 'المرحلة الاولى'
            if lev == 'level2':
                lev_1 = 'المرحلة الثانية'
            if lev == 'level3':
                lev_1 = 'المرحلة الثالثة'
            if lev == 'level4':
                lev_1 = 'المرحلة الرابعة'
            if lev == 'level5':
                lev_1 = 'المرحلة الخامسة'


                


            worksheet.write(row, 1, lev_1 or '', main_cell_total)
            worksheet.write(row, 2, "صباحي / مسائي" or '', main_cell_total)
            currecnt_status_data_1 = self.filtered(lambda picking:picking.level == lev and picking.Status == 'currecnt_student')

            status_2_data_1 = self.filtered(lambda picking:picking.level == lev and picking.Status == 'status2') 

            status_4_data_1 = self.filtered(lambda picking:picking.level == lev and picking.Status == 'status3') 


            status_5_data_1 =  self.filtered(lambda picking:picking.level == lev and picking.Status == 'status1') 
            failed_1 = self.filtered(lambda picking:picking.level == lev and picking.Status == 'failed') 

            transferred_to_us_1 =  self.filtered(lambda picking:picking.level == lev and picking.partner_id.transferred_to_us == True)
            transferred_from_us_1 = self.filtered(lambda picking:picking.level == lev and picking.partner_id.transfer_shift == True) 
            worksheet.write(row, 3, len(currecnt_status_data_1.mapped('id')) or '', main_cell_total)

            worksheet.write(row, 4, len(status_2_data_1.mapped('id')) or '', main_cell_total)

            worksheet.write(row, 5, len(status_4_data_1.mapped('id')) or '', main_cell_total)

            worksheet.write(row, 6, len(status_5_data_1.mapped('id')) or '', main_cell_total)

            worksheet.write(row, 7, len(failed_1.mapped('id')) or '', main_cell_total)


            worksheet.write(row, 8, len(transferred_from_us_1.mapped('id')) or '', main_cell_total)

            worksheet.write(row, 9, len(transferred_to_us_1.mapped('id')) or '', main_cell_total)

            field_one_1 =  self.filtered(lambda picking:picking.level == lev and picking.partner_id.field_one_1 == True) 
            worksheet.write(row, 10, len(field_one_1.mapped('id')) or '', main_cell_total)
            total_field_one_1 = total_field_one_1 + len(field_one_1.mapped('id'))
            
            fields_one_2 = self.filtered(lambda picking:picking.level == lev and picking.partner_id.fields_one_2 == True) 
            worksheet.write(row, 11, len(fields_one_2.mapped('id')) or '', main_cell_total)

            total_fields_one_2 = total_fields_one_2 + len(fields_one_2.mapped('id'))


            last_three_status_1 = len(status_2_data_1.mapped('id')) + len(status_4_data_1.mapped('id')) + len(status_5_data_1.mapped('id'))

            total_of_all_1 = len(currecnt_status_data_1.mapped('id')) - last_three_status_1


            worksheet.write(row, 12, total_of_all_1 or '', main_cell_total)


            total_of_data_one_1 = 0
            colld = 13
            for ddts in data_one:
                data_one_data_1 = self.filtered(lambda picking:picking.level == lev and picking.partner_id.data_one.id == ddts.id) 
                worksheet.write(row, colld, len(data_one_data_1.mapped("id")), main_cell_total) #data_one
                total_of_data_one_1 = total_of_data_one_1 + len(data_one_data_1.mapped("id"))
                colld = colld + 1

            gender_female_data_1 = self.filtered(lambda picking:picking.level == lev and picking.partner_id.gender == 'male')
            worksheet.write(row, colld, len(gender_female_data_1.mapped("id")), main_cell_total)

            gender_female_data_1 = self.filtered(lambda picking:picking.level == lev and picking.partner_id.gender == 'female')
            worksheet.write(row, colld + 1, len(gender_female_data_1.mapped("id")), main_cell_total)


            worksheet.write(row, colld + 2, total_of_data_one_1, main_cell_total)
            print("row$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",row)
            row = row + 1

        
        currecnt_status_data_2 = self.filtered(lambda picking:picking.Status == "currecnt_student")

        status_2_data_2 = self.filtered(lambda picking:picking.Status == "status2")

        status_4_data_2 = self.filtered(lambda picking:picking.Status == "status3")


        status_5_data_2 = self.filtered(lambda picking:picking.Status == "status1")
        failed_2 = self.filtered(lambda picking:picking.Status == "failed")

        transferred_to_us_2 =  self.filtered(lambda picking:picking.partner_id.transferred_to_us == True)
        transferred_from_us_2 = self.filtered(lambda picking:picking.partner_id.transfer_shift == True)

        worksheet.write_merge(row, row, 0, 2, "المجمــــــــــــــــــــــــــــــــوع", main_cell_total_of_total)
        worksheet.write(row, 3, len(currecnt_status_data_2.mapped('id')) or '', main_cell_total_of_total)

        worksheet.write(row, 4, len(status_2_data_2.mapped('id')) or '', main_cell_total_of_total)

        worksheet.write(row, 5, len(status_4_data_2.mapped('id')) or '', main_cell_total_of_total)

        worksheet.write(row, 6, len(status_5_data_2.mapped('id')) or '', main_cell_total_of_total)

        worksheet.write(row, 7, len(failed_2.mapped('id')) or '', main_cell_total_of_total)


        worksheet.write(row, 8, len(transferred_from_us_2.mapped('id')) or '', main_cell_total_of_total)

        worksheet.write(row, 9, len(transferred_to_us_2.mapped('id')) or '', main_cell_total_of_total)


        field_one_1_2 = self.filtered(lambda picking:picking.partner_id.field_one_1 == True)
        worksheet.write(row, 10, len(field_one_1_2.mapped('id')) or '', main_cell_total_of_total)
        
        fields_one_2_2 =  self.filtered(lambda picking:picking.partner_id.fields_one_2 == True)
        worksheet.write(row, 11, len(fields_one_2_2.mapped('id')) or '', main_cell_total_of_total)




        last_three_status_2 = len(status_2_data_2.mapped('id')) + len(status_4_data_2.mapped('id')) + len(status_5_data_2.mapped('id'))

        total_of_all_2 = len(currecnt_status_data_2.mapped('id')) - last_three_status_2


        worksheet.write(row, 12, total_of_all_2 or '', main_cell_total_of_total)


        total_of_data_one_2 = 0
        colld = 13
        for ddts in data_one:
            data_one_data_2 = self.filtered(lambda picking:picking.partner_id.data_one.id == ddts.id)
            worksheet.write(row, colld, len(data_one_data_2.mapped("id")), main_cell_total_of_total) #data_one
            total_of_data_one_2 = total_of_data_one_2 + len(data_one_data_2.mapped("id"))
            colld = colld + 1

        gender_female_data_2 =  self.filtered(lambda picking:picking.partner_id.gender == 'male')
        worksheet.write(row, colld, len(gender_female_data_2.mapped("id")), main_cell_total_of_total)

        gender_female_data_2 =  self.filtered(lambda picking:picking.partner_id.gender == 'female')
        worksheet.write(row, colld + 1, len(gender_female_data_2.mapped("id")), main_cell_total_of_total)


        worksheet.write(row, colld + 2, total_of_data_one_2, main_cell_total_of_total)
        print("row$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",row)
        row = row + 1    



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




class ContraDataDept(models.Model):
    _inherit="account.move"

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


class ContraPayslipDateAccount(models.Model):
    _inherit="hr.payslip"

    description = fields.Html("Description")

    Account_number = fields.Char("Account Number", related="employee_id.Account_number")

    department = fields.Many2one("hr.department", related="employee_id.department_id", store=True)

    net_salary = fields.Float("Net Salary",compute="_value_pc", store=True)

    def action_payslip_done(self):
        res = super(ContraPayslipDateAccount, self).action_payslip_done()
        for record in self:
            for line in record.line_ids:
                if line.category_id.id == 5:
                    record.net_salary = line.amount
        return res            

    @api.depends('net_salary')
    def _value_pc(self):
        for record in self:
            for line in record.line_ids:
                if line.category_id.name == 'Net':
                    record.net_salary = line.total

    def change_the_value_payslip(self):
        for ddtt in self:
            ddtt.state = 'done'

    def change_the_value_verify(self):
        for ddtt in self:
            ddtt.state = 'verify'        



    def send_mis_report_sale_payslip_data(self):
        filename = 'Payslip.xls'
        string = 'Payslip.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string)
        header_bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")
        cell_format = xlwt.easyxf()
        filename = 'payslip_%s.xls' % date.today()
        rested = self.env['sale.order'].search([])
        row = 2
        border_normal = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; font: bold on; pattern: pattern solid, fore_colour gray25;')
        border_1 = xlwt.easyxf('borders: left 1, right 1, top 1, bottom 1;')
        border_2 = xlwt.easyxf('borders: left 2, right 2, top 2, bottom 2;')
        border_color_2 = xlwt.easyxf('borders: top_color blue, bottom_color blue, right_color blue, left_color blue, left 2, right 2, top 2, bottom 2; font: bold on; pattern: pattern solid, fore_colour gray25;')
        
        header_bold_extra_tag = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour green; font: color white; align: horiz centre")

        header_bold_extra = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25; font: color black; align: horiz centre")

        main_cell_total_of_total = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; ")

        

        worksheet.col(0).width = 5000
        worksheet.col(1).width = 5000
        worksheet.col(2).width = 5000
        worksheet.row(0).height = 500
        # Student Name  
        # Membership Lines/Installment  
        # Membership Lines/#No  
        # Membership Lines/Invoice  
        # Membership Lines/Amount   
        # Membership Lines/Payment Status   
        # Membership Lines/Payment Date
        worksheet.write(0, 0, 'Department Name', header_bold_extra)
        worksheet.write(0, 1, 'Employee Name', header_bold_extra)
        worksheet.write(0, 2, 'Date From', header_bold_extra)
        worksheet.write(0, 3, 'Date To', header_bold_extra)
        worksheet.write(0, 4, 'Description', header_bold_extra)
        worksheet.write(0, 5, 'Day Deduction', header_bold_extra)

        # v.onboard_date >= (datetime.today().date().replace(day=1) - relativedelta(months=1)) and v.onboard_date <= (datetime.today().date() - relativedelta(months=1))
        print("self############",self)
        department = self.env["hr.department"].search([])
        for value in department:
            rest = self.filtered(lambda picking: picking.department.id == value.id)
            if rest:
                worksheet.write(row - 1, 0, str(value.name) + "(" + str(len(rest.mapped("id"))) + ")" or '', main_cell_total_of_total)
            for material_line_id in rest:
                worksheet.write(row, 1, material_line_id.employee_id.name or '' , main_cell_total_of_total)
                worksheet.write(row, 2, material_line_id.date_from.strftime('%m/%d/%Y') or '' , main_cell_total_of_total)
                worksheet.write(row, 3, material_line_id.date_to.strftime('%m/%d/%Y') or '' , main_cell_total_of_total)
                if material_line_id.description:
                    worksheet.write(row, 4, re.sub('<[^>]*>', '', material_line_id.description) or '' , main_cell_total_of_total)
                else:    
                    worksheet.write(row, 4, '' , main_cell_total_of_total)    

                worksheet.write(row, 5, material_line_id.contract_id.day_deduction or '' , main_cell_total_of_total)   
                row += 1 

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



