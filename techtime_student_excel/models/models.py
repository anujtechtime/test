# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
import pytz
import threading
from collections import OrderedDict, defaultdict
from datetime import date, datetime, timedelta
from geopy.geocoders import Nominatim
import xml.dom.minidom
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


class DataStatusValue(models.TransientModel):
    _name = 'status.value'
   

    Status = fields.Selection([('currecnt_student','Current student'),('succeeded','Succeeded'),('failed','Falied'),('transferred_from_us','Transferred From Us'),('graduated','Graduated')], string="Status")

    def action_confirm_change_status(self):
        print("res@@@@@@@@@@@@@@@@@@@@@@@@@@26666",self._context.get("active_id"))
        for idds in self._context.get("active_id"):
            print("idds@@@@@@@@@@@@@@@@@",idds)
            levels_sale_order = self.env["sale.order"].browse(int(idds))
            levels_sale_order.Status = self.Status
            levels_sale_order.partner_id.Status = self.Status
        # for ddts in self:
        #     ddts.level =  self.level

    @api.model
    def default_get(self, field_list):
        res = super(DataStatusValue, self).default_get(field_list)
        print("res@@@@@@@@@@@@@@@@@@@@@@@@@@2",self._context.get("active_id"))
        for idds in self._context.get("active_id"):
            print("idds@@@@@@@@@@@@@@@@@",idds)
        return res        



class DataLevelValue(models.TransientModel):
    _name = 'level.value'
   

    level = fields.Selection([('leve1','المرحلة الاولى'),('level2','المرحلة الثانية'),('level3','المرحلة الثالثة'),('level4','المرحلة الرابعة'),('level5','المرحلة الخامسة')], string="Level")
    year = fields.Many2one("year.year", string="Year")


    def action_confirm_change_level(self):
        print("res@@@@@@@@@@@@@@@@@@@@@@@@@@26666",self._context.get("active_id"))
        for idds in self._context.get("active_id"):
            print("idds@@@@@@@@@@@@@@@@@",idds)
            levels_sale_order = self.env["res.partner"].browse(int(idds))
            print("levels_sale_order@@@@@@@@@@@@@@@@@@@@@@@@",levels_sale_order)
            levels_sale_order.level = self.level
            levels_sale_order.year = self.year

            levels_sale_order.partner_id.level = self.level
            levels_sale_order.partner_id.year = self.year


        # for ddts in self:
        #     ddts.level =  self.level

    @api.model
    def default_get(self, field_list):
        res = super(DataLevelValue, self).default_get(field_list)
        print("res@@@@@@@@@@@@@@@@@@@@@@@@@@2",self._context.get("active_id"))
        for idds in self._context.get("active_id"):
            print("idds@@@@@@@@@@@@@@@@@",idds)
            # levels_sale_order = self.env["sale.order"].browse(int(idds))
            # print("levels_sale_order@@@@@@@@@@@@@@@@@@@@@@@@",levels_sale_order)
            # levels_sale_order.level = self.level
            # levels_sale_order.update({
            #     'level': self.level,
            # })
        # company = self.env.company
        # res.update({
        #     'company_id': company.id,
        #     'period_lock_date': company.period_lock_date,
        #     'fiscalyear_lock_date': company.fiscalyear_lock_date,
        # })
        return res        


class TechtimeStudentData(models.Model):
    _inherit = 'account.move'

    department = fields.Many2one("department.department", string="Department")
    payment_number_temp = fields.Char("Payment Number")

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.update({
                "college" : self.partner_id.college.id if self.partner_id.college else False,
                "student" : self.partner_id.student_type.id if self.partner_id.student_type else False,
                "department" : self.partner_id.department.id if self.partner_id.department else False,
                "Subject" : self.partner_id.shift if self.partner_id.shift else False,
                "level" : self.partner_id.level if self.partner_id.level else False,
                })


class TechtimeStudentPayment(models.Model):
    _inherit = 'account.payment'

    department = fields.Many2one("department.department", string="Department")

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.update({
                "college" : self.partner_id.college.id if self.partner_id.college else False,
                "student" : self.partner_id.student_type.id if self.partner_id.student_type else False,
                "department" : self.partner_id.department.id if self.partner_id.department else False,
                "Subject" : self.partner_id.shift if self.partner_id.shift else False,
                "level" : self.partner_id.level if self.partner_id.level else False,
                })   


class TechtimeStudentexcel(models.Model):
    _inherit = 'sale.order'


    Status = fields.Selection([('status4', 'مؤجل'),('status1','ترقين قيد'),('status2','طالب غير مباشر'),('status3','انسحاب'),('currecnt_student','Current student'),('succeeded','Succeeded'),('failed','Falied'),('transferred_from_us','Transferred From Us'),('graduated','Graduated')], string="Status")
    transferred_to_us = fields.Boolean("Transferred To Us ") 
    transfer_shift = fields.Boolean("Transferred Shift ")
    chckbox_data = fields.Boolean("نقل من كلية الى أخرى")
 

    @api.onchange('partner_id')
    def onchange_partner_id_warning(self):
        result = super(TechtimeStudentexcel, self).onchange_partner_id_warning()
        if self.partner_id:
            self.update({
                "year" : self.partner_id.year.id if self.partner_id.year else False, 
                "college" : self.partner_id.college.id if self.partner_id.college else False,
                "department" : self.partner_id.department.id if self.partner_id.department else False,
                "student" : self.partner_id.student_type.id if self.partner_id.student_type else False,
                "Subject" : self.partner_id.shift if self.partner_id.shift else False,
                "level" : self.partner_id.level if self.partner_id.level else False,
                "Status" : self.partner_id.Status if self.partner_id.Status else False,
                "chckbox_data" : self.partner_id.chckbox_data if self.partner_id.chckbox_data else False,
                })


        return result
 
#     _description = 'techtime_payroll_excel.techtime_payroll_excel'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


    # def action_confirm(self):
    #     result = super(TechtimeStudentexcel, self).action_confirm()

    #     if self.partner_id:
    #         self.partner_id.update({
    #             "year" : self.year.id,
    #             "college" : self.college.id,
    #             "department" : self.department.id,
    #             "student_type" : self.student.id,
    #             "shift" : self.Subject,
    #             "level" : self.level,
    #             "transferred_to_us" : self.transferred_to_us,
    #             "transfer_shift" : self.transfer_shift,
    #             "Status" : self.Status,
    #             "chckbox_data" : self.chckbox_data,
    #             }) 
    #     return result

    def action_confirm_change_contact(self):
        for ddts in self:
            if ddts.partner_id and ddts.state == "sale":
                data = ddts.partner_id.update({
                    "year" : ddts.year.id,
                    "college" : ddts.college.id,
                    "department" : ddts.department.id,
                    "student_type" : ddts.student.id,
                    "shift" : ddts.Subject,
                    "level" : ddts.level,
                    "transferred_to_us" : ddts.transferred_to_us,
                    "transfer_shift" : ddts.transfer_shift,
                    "Status" : ddts.Status,
                    "chckbox_data" : ddts.chckbox_data,
                    })
                print("data##########",data)

    def action_done_show_wizard_status(self):
        print("self._context##################",self._context.get("active_ids"))
        return {'type': 'ir.actions.act_window',
        'name': _('Change the Level Value'),
        'res_model': 'status.value',
        'target': 'new',
        'view_id': self.env.ref('techtime_student_excel.view_any_name_form_status_value').id,
        'view_mode': 'form',
        'context': {"active_id" : self._context.get("active_ids")}
        }
            


    def send_mis_report_sale_new(self):       
        filename = 'Student.xls'
        string = 'Student_report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string)
        header_bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")
        cell_format = xlwt.easyxf()
        filename = 'Student_Report_%s.xls' % date.today()
        rested = self.env['sale.order'].search([])
        row = 1
        border_normal = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; font: bold on; pattern: pattern solid, fore_colour gray25;')
        border_1 = xlwt.easyxf('borders: left 1, right 1, top 1, bottom 1;')
        border_2 = xlwt.easyxf('borders: left 2, right 2, top 2, bottom 2;')
        border_color_2 = xlwt.easyxf('borders: top_color blue, bottom_color blue, right_color blue, left_color blue, left 2, right 2, top 2, bottom 2; font: bold on; pattern: pattern solid, fore_colour gray25;')
        worksheet.col(0).width = 10000
        worksheet.col(1).width = 15000
        worksheet.col(2).width = 10000
        worksheet.row(0).height = 500
        # Student Name  
        # Membership Lines/Installment  
        # Membership Lines/#No  
        # Membership Lines/Invoice  
        # Membership Lines/Amount   
        # Membership Lines/Payment Status   
        # Membership Lines/Payment Date

        worksheet.write(0, 0, 'Student Name', border_color_2)
        worksheet.write(0, 1, 'College Number', border_color_2)
        worksheet.write(0, 2, 'Exam No', border_color_2)
        worksheet.write(0, 3, 'Year', border_color_2)
        worksheet.write(0, 4, 'College', border_color_2)
        worksheet.write(0, 5, 'Department', border_color_2)
        worksheet.write(0, 6, 'Student Type', border_color_2)
        worksheet.write(0, 7, 'Shift', border_color_2)
        worksheet.write(0, 8, 'Level', border_color_2)

        worksheet.write(0, 9, 'Transferred Shift', border_color_2)
        worksheet.write(0, 10, 'Transferred To Us', border_color_2)


        # v.onboard_date >= (datetime.today().date().replace(day=1) - relativedelta(months=1)) and v.onboard_date <= (datetime.today().date() - relativedelta(months=1))
        print("self############uuuuuuuuuuuuuuuuuuuu",self)
        for material_line_id in self:
            print("lllllllllllllllllllll",material_line_id)
            if material_line_id.Status == 'succeeded' or material_line_id.Status == 'failed' and material_line_id.year.year == '2022-2023':
                print("material_line_id##########",material_line_id.college)
                worksheet.write(row, 0, material_line_id.partner_id.name or '')
                worksheet.write(row, 1, material_line_id.college_number or '')
                worksheet.write(row, 2, material_line_id.student_no or '')
                worksheet.write(row, 3, material_line_id.year.year or '')
                worksheet.write(row, 4, material_line_id.college.college or '')
                worksheet.write(row, 5, material_line_id.department.department or '')
                worksheet.write(row, 6, material_line_id.student.Student or '')
                worksheet.write(row, 7, material_line_id.Subject or '')
                worksheet.write(row, 8, material_line_id.level or '')

                worksheet.write(row, 9, material_line_id.transfer_shift or '') 
                worksheet.write(row, 10, material_line_id.transferred_to_us or '') 
                row += 1    



        worksheet.write(0, 16, 'College', border_color_2)
        worksheet.write(0, 17, 'Level', border_color_2)
        

        worksheet.write(0, 18, 'Number Of Student Registered', border_color_2)
        worksheet.write(0, 19, 'Number Of Student Not Registered', border_color_2)

        row_paid = 1
        college_data = self.env["faculty.faculty"].search([])
        Registered_total = 0
        for coll in college_data:
            not_registered_level1 = 0
            not_registered_level2 = 0
            not_registered_level3 = 0
            not_registered_level4 = 0
            not_registered_level5 = 0
            registered_level1 = 0
            registered_level2 = 0
            registered_level3 = 0
            registered_level4 = 0
            registered_level5 = 0
            for material_line in self:
                print("lllllllllllllllllllll",material_line.partner_id)
                year_all = self.env["year.year"].search([],order='year asc')
                _logger.info("pincode************11111111111111#####**%s" %year_all)
                for yrs in year_all:
                    print("yrs$$$$$$$$$$$$$$$$$$$$$$$",yrs.year)
                    _logger.info("pincode************222222222222#####**%s" %yrs.year)
                print("yrs@@@@@@@@@@@@@@@@@@@@@@@@@@2$",yrs.year)
                sale_ord_level1 = self.env["sale.order"].search([('partner_id','=',material_line.partner_id.id),("year","=",yrs.id),('level','=','leve1'),('college','=',coll.id),('state','=','sale')])
                _logger.info("pincode************333333333333333333#####**%s" %sale_ord_level1)
                if sale_ord_level1:
                    registered_level1 = registered_level1 + 1
                

                sale_ord_level2 = self.env["sale.order"].search([('partner_id','=',material_line.partner_id.id),("year","=",yrs.id),('level','=','level2'),('college','=',coll.id),('state','=','sale')])
                _logger.info("pincode************333333333333333333#####**%s" %sale_ord_level2)
                if sale_ord_level2:
                    registered_level2 = registered_level2 + 1
                
                    

                sale_ord_level3 = self.env["sale.order"].search([('partner_id','=',material_line.partner_id.id),("year","=",yrs.id),('level','=','level3'),('college','=',coll.id),('state','=','sale')],limit=1)
                _logger.info("pincode************333333333333333333#####**%s" %sale_ord_level3)
                if sale_ord_level3:
                    registered_level3 = registered_level3 + 1
            
                    

                sale_ord_level4 = self.env["sale.order"].search([('partner_id','=',material_line.partner_id.id),("year","=",yrs.id),('level','=','level4'),('college','=',coll.id),('state','=','sale')],limit=1)
                _logger.info("pincode************333333333333333333#####**%s" %sale_ord_level4)
                if sale_ord_level4:
                    registered_level4 = registered_level4 + 1
            
                    

                sale_ord_level5 = self.env["sale.order"].search([('partner_id','=',material_line.partner_id.id),("year","=",yrs.id),('level','=','level5'),('college','=',coll.id),('state','=','sale')],limit=1)
                _logger.info("pincode************333333333333333333#####**%s" %sale_ord_level5)
                if sale_ord_level5:
                    registered_level5 = registered_level5 + 1


            
            Registered_total  = Registered_total + registered_level1 + registered_level2 + registered_level3 + registered_level4 + registered_level5        

            worksheet.write(row_paid, 16, coll.college or '')
            worksheet.write(row_paid + 1, 16, coll.college or '')
            worksheet.write(row_paid + 2, 16, coll.college or '')
            worksheet.write(row_paid + 3, 16, coll.college or '')
            worksheet.write(row_paid + 4, 16, coll.college or '')

            worksheet.write(row_paid, 17, 'Level1', border_color_2)
            worksheet.write(row_paid + 1, 17, 'Level2', border_color_2)
            worksheet.write(row_paid + 2, 17, 'Level3', border_color_2)
            worksheet.write(row_paid + 3, 17, 'Level4', border_color_2)
            worksheet.write(row_paid + 4, 17, 'Level5', border_color_2)

            worksheet.write(row_paid, 18, registered_level1 or '')
            worksheet.write(row_paid + 1, 18, registered_level2 or '')
            worksheet.write(row_paid + 2, 18, registered_level3 or '')
            worksheet.write(row_paid + 3, 18, registered_level4 or '')
            worksheet.write(row_paid + 4, 18, registered_level5 or '')

            worksheet.write(row_paid, 19, material_line.transferred_to_us or '')


            # Registered_total

            row_paid = row_paid + 6


        worksheet.write(row_paid, 18, Registered_total or '')
        _logger.info("row_paid************row_paid#####**%s" %row_paid)
            
        
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


    def send_mis_report_sale_college_report(self):  
        filename = 'Student.xls'
        string = 'Student_report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string)
        header_bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")
        cell_format = xlwt.easyxf()
        filename = 'Student_Report_%s.xls' % date.today()
        rested = self.env['sale.order'].search([])
        row = 1
        border_normal = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; font: bold on; pattern: pattern solid, fore_colour gray25;')
        border_1 = xlwt.easyxf('borders: left 1, right 1, top 1, bottom 1;')
        border_2 = xlwt.easyxf('borders: left 2, right 2, top 2, bottom 2;')
        border_color_2 = xlwt.easyxf('borders: top_color blue, bottom_color blue, right_color blue, left_color blue, left 2, right 2, top 2, bottom 2; font: bold on; pattern: pattern solid, fore_colour gray25;')
        worksheet.col(0).width = 10000
        worksheet.col(1).width = 15000
        worksheet.col(2).width = 10000
        worksheet.row(0).height = 500
        
        col = 1
        college_data = self.env["faculty.faculty"].search([])
        # print("college_data$$$$$$$$$$$$$$$$$$$$$$",college_data)
        Registered_total = 0
        for coll in college_data:
            not_registered_level1 = 0
            not_registered_level2 = 0
            not_registered_level3 = 0
            not_registered_level4 = 0
            not_registered_level5 = 0
            registered_level1 = 0
            registered_level2 = 0
            registered_level3 = 0
            registered_level4 = 0
            registered_level5 = 0
            # for material_line in self:
            # print("lllllllllllllllllllll",material_line.partner_id)
            year_all = self.env["year.year"].search([],order='year asc')
            student_type = self.env["level.level"].search([])
            # print("student_type###################",student_type)
            # _logger.info("student_type************11111111111111#####**%s" %student_type)
            for yrs in year_all:
                print("yrs$$$$$$$$$$$$$$$$$$$$$$$")
                # _logger.info("pincode************222222222222#####**%s" %yrs.year)
            # print("yrs@@@@@@@@@@@@@@@@@@@@@@@@@@2$",yrs.year)
            row = 1
            college_total_non_discount = 0
            student_total_data = 0
            for student in student_type:
                sale_ord_level1 = self.env["sale.order"].search([('student','=',student.id),("year","=",yrs.id),('college','=',coll.id),('state','=','sale')])
                # print("sale_ord_level1###################444444444444444",sale_ord_level1.mapped("installment_amount"))
                installment_amou = sale_ord_level1.mapped("installment_amount")

                for ddtsgs in sale_ord_level1:
                    installment_full_price = self.env["installment.details"].search([("year",'=',ddtsgs.year.id),('college','=',ddtsgs.college.id),('department','=',ddtsgs.department.id),('Student','=',8),('Subject','=',ddtsgs.Subject),('level','=',ddtsgs.level)],limit=1)
                    _logger.info("installment_full_price.installment************333333333333333333#####**%s" %installment_full_price.installment)
                    college_total_non_discount = college_total_non_discount + installment_full_price.installment
                print("data##################",sum(installment_amou))
                print("student##################",student.Student)


                _logger.info("pincode************333333333333333333#####**%s" %sum(installment_amou))
                _logger.info("student.Student************44444444444444444444444#####**%s" %student.Student)

                student_total_data = student_total_data + sum(installment_amou)
                _logger.info("pincode************55555555555555555555#####**%s" %coll.college)

                if col == 1:
                    worksheet.write(row, 0, student.Student or '')

                worksheet.write(row, col, sum(installment_amou) or '')
                row = row + 1
            worksheet.write(row + 1, col, student_total_data or '')    
            worksheet.write(0, col, coll.college or '')

            


            worksheet.write(row + 3, col, college_total_non_discount or '')

            col = col + 1
        worksheet.write(row + 3, 0, "الايراد التخميني بدون المنح والتخفيضات ")
        worksheet.write(row + 1, 0, 'مجموع المستلم')



            # worksheet.write(row, 0, material_line_id.partner_id.name or '')
            # worksheet.write(row, 0, material_line_id.partner_id.name or '')
            # worksheet.write(row, 0, material_line_id.partner_id.name or '')

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


    def send_mis_report_sale(self):
        filename = 'Student.xls'
        string = 'Student_report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string)
        header_bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")
        cell_format = xlwt.easyxf()
        filename = 'Student_Report_%s.xls' % date.today()
        rested = self.env['sale.order'].search([])
        row = 1
        border_normal = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; font: bold on; pattern: pattern solid, fore_colour gray25;')
        border_1 = xlwt.easyxf('borders: left 1, right 1, top 1, bottom 1;')
        border_2 = xlwt.easyxf('borders: left 2, right 2, top 2, bottom 2;')
        border_color_2 = xlwt.easyxf('borders: top_color blue, bottom_color blue, right_color blue, left_color blue, left 2, right 2, top 2, bottom 2; font: bold on; pattern: pattern solid, fore_colour gray25;')
        worksheet.col(0).width = 10000
        worksheet.col(1).width = 15000
        worksheet.col(2).width = 10000
        worksheet.row(0).height = 500
        # Student Name	
        # Membership Lines/Installment	
        # Membership Lines/#No	
        # Membership Lines/Invoice	
        # Membership Lines/Amount	
        # Membership Lines/Payment Status	
        # Membership Lines/Payment Date

        worksheet.write(0, 0, 'Student Name', border_color_2)
        worksheet.write(0, 1, 'College Number', border_color_2)
        worksheet.write(0, 2, 'Exam No', border_color_2)
        worksheet.write(0, 3, 'Year', border_color_2)
        worksheet.write(0, 4, 'College', border_color_2)
        worksheet.write(0, 5, 'Department', border_color_2)
        worksheet.write(0, 6, 'Student Type', border_color_2)
        worksheet.write(0, 7, 'Shift', border_color_2)
        worksheet.write(0, 8, 'Level', border_color_2)


        worksheet.write(0, 9, 'Sale Order', border_color_2)
        worksheet.write(0, 10, 'Invoice Number', header_bold)
        worksheet.write(0, 11, 'Amount', header_bold)
        worksheet.write(0, 12, 'Payment Status', header_bold)
        worksheet.write(0, 13, 'Payment Date', header_bold)
        # v.onboard_date >= (datetime.today().date().replace(day=1) - relativedelta(months=1)) and v.onboard_date <= (datetime.today().date() - relativedelta(months=1))
        print("self############",self)
        for material_line_id in self:
            print("material_line_id##########",material_line_id.college)
            worksheet.write(row, 0, material_line_id.partner_id.name or '')
            worksheet.write(row, 1, material_line_id.college_number or '')
            worksheet.write(row, 2, material_line_id.student_no or '')
            worksheet.write(row, 3, material_line_id.year.year or '')
            worksheet.write(row, 4, material_line_id.college.college or '')
            worksheet.write(row, 5, material_line_id.department.department or '')
            worksheet.write(row, 6, material_line_id.student.Student or '')
            worksheet.write(row, 7, material_line_id.Subject or '')
            worksheet.write(row, 8, material_line_id.level or '')
            worksheet.write(row, 9, material_line_id.name or '')
            for iit in material_line_id.sale_installment_line_ids:
                if iit.invoice_id.state != "cancel" and iit.amount_installment > 0:
                    worksheet.write(row, 10, iit.invoice_id.name or '')
                    worksheet.write(row, 11, iit.amount_installment or '')
                    worksheet.write(row, 12, iit.payment_status or '')
                    if iit.payment_date:
                        worksheet.write(row, 13, iit.payment_date.strftime("%m/%d/%Y") or '')
                    if not iit.payment_date:
                        worksheet.write(row, 13, '')    
                row += 1
            if not material_line_id.sale_installment_line_ids:    
                row += 1    
                print("row###############",row)
            print("worksheet###################",worksheet)    
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



class ResData(models.Model):
    _inherit = 'res.partner'

    contact_type = fields.Selection([("student","طالب"),("teacher", "مدرس")], string="Contact Type", tracking=True)

    chckbox_data_2 = fields.Boolean("نقل من جامعة المعقل")


    boolean_one = fields.Boolean(string="أبناء الهيئة التدريسية", tracking=True)
    boolean_two = fields.Boolean(string="أبناء أصحاب الشهادات العليا في وزارات أخرى", tracking=True)
    boolean_three = fields.Boolean(string="الوافدين", tracking=True)
    boolean_four = fields.Boolean(string="السجناء السياسيين", tracking=True)


    payment_number = fields.Many2one("account.payment",string="payment number", tracking=True)
    transferred_to_us = fields.Boolean("نقل الى جامعة المعقل", tracking=True)
    transfer_shift = fields.Boolean("Transferred Shift ", tracking=True)
    Status = fields.Selection([('status4', 'مؤجل'),('status1','ترقين قيد'),('status2','طالب غير مباشر'),('status3','انسحاب'),('currecnt_student','طالب حالي'),('succeeded','ناجح'),('failed','راسب'),('transferred_from_us','نقل من جامعة المعقل'),('graduated','متخرج')], string="Status", tracking=True)
    chckbox_data = fields.Boolean("نقل من كلية الى أخرى", tracking=True)


    year = fields.Many2one("year.year", string="Year", tracking=True)
    college = fields.Many2one("faculty.faculty", string="College", tracking=True)
    department = fields.Many2one("department.department", string="Department", tracking=True)
    student_type = fields.Many2one("level.level", string="Student Type", tracking=True)
    shift = fields.Selection([('morning','صباحي'),('afternoon','مسائي')], string="Shift", tracking=True)
    level = fields.Selection([('leve1','المرحلة الاولى'),('level2','المرحلة الثانية'),('level3','المرحلة الثالثة'),('level4','المرحلة الرابعة'),('level5','المرحلة الخامسة')], string="Level", tracking=True)
    number_of_years = fields.Char("Number Of Years", tracking=True)

    gender = fields.Selection([('male','ذكر'),('female','انثى')], string="Gender", tracking=True)
    nationalty = fields.Char("Nationalty", tracking=True)
    year_born = fields.Char("Year Born", tracking=True)
    Academic_Branch = fields.Integer("Academic Branch", tracking=True)
    year_of_graduation = fields.Integer("Year Of Graduation", tracking=True)
    final_result = fields.Char("Final Result", tracking=True)
    year_of_acceptance   = fields.Integer("Year Of Acceptance", tracking=True)    




    Round_of_Passing = fields.Char("Round of Passing", tracking=True)
    subject_that_has_been_resit = fields.Char("Subject that has been resit", tracking=True)
    name_of_school_graduated_from = fields.Char("Name of school graduated from", tracking=True)
    State_of_school_graduated_from = fields.Char("State of school graduated from", tracking=True)



    State_of_birth = fields.Char("State of birth", tracking=True)
    ID_number = fields.Integer("ID number", tracking=True)
    ID_issue_Date = fields.Date("ID issue Date", tracking=True)
    place_of_issuance = fields.Char("Place of issuance", tracking=True)
    Marital_status = fields.Selection([('married','Married'),('unmarried','Unmarried')], string="Marital status", tracking=True) 


    parent_name = fields.Char("Parent name", tracking=True)
    address = fields.Char("Address", tracking=True)
    Father_Job = fields.Char("Father Job", tracking=True)
    work_address_father = fields.Char("Work address", tracking=True)
    Mother_Job = fields.Char("Mother Job", tracking=True)
    work_address_mother = fields.Char("Work address", tracking=True)
    Phone_number_1_mother = fields.Integer("Phone number 1", tracking=True)
    Phone_number_2_mother = fields.Integer("Phone number 2", tracking=True)
    sibling_name = fields.Char("sibling name", tracking=True)
    relative_relation = fields.Char("Relative relation", tracking=True)
    address_mother = fields.Char("Address", tracking=True)
    phone_number_1 = fields.Integer("phone number 1", tracking=True)
    phone_number_2 = fields.Integer("phone_number 2", tracking=True)


    guarantor_name_gurantor  = fields.Char("Guarantor name", tracking=True)
    relative_relation_gurantor = fields.Char("Relative relation", tracking=True)
    address_gurantor = fields.Char("Address", tracking=True)
    phone_number_1_gurantor = fields.Char("phone number 1", tracking=True)
    phone_number_2_gurantor = fields.Char("phone number 2", tracking=True)


    relation = fields.Selection([('father','Father'),('mother','Mother'),('relative','Relative'),('guarantor','Guarantor')], string="Relation", tracking=True)
    type_of_relative = fields.Char("Type Of Relative", tracking=True)
    Father_Job = fields.Char("Father Job", tracking=True)
    work_address_father = fields.Char("Work address", tracking=True)


    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        result = super(ResData, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)

        # Disabling the import button for users who are not in import group
        if view_type == 'form':
            doc = etree.XML(result['arch'])
            # if not self.env.user.has_group('techtime_student_excel.group_manager_import_button'):
            #  # When the user is not part of the import group
            #     for node in doc.xpath("//tree"):
            #         # Set the import to false
            #         node.set('import', 'false')
            #     # for node in doc.xpath("//kanban"):
            #     #     # Set the import to false
            #     #     node.set('import', 'false')  

            if not self.env.user.has_group('techtime_student_excel.group_manager_edit_button'):
             # When the user is not part of the import group
                for node in doc.xpath("//form"):
                    # Set the import to false
                    node.set('edit', 'false')            
            result['arch'] = etree.tostring(doc)

        if view_type == 'kanban':
            doc = etree.XML(result['arch'])
            # if not self.env.user.has_group('techtime_student_excel.group_manager_import_button'):
            #  # When the user is not part of the import group
            #     for node in doc.xpath("//tree"):
            #         # Set the import to false
            #         node.set('import', 'false')
            #     # for node in doc.xpath("//kanban"):
            #     #     # Set the import to false
            #     #     node.set('import', 'false')  

            if not self.env.user.has_group('techtime_student_excel.group_manager_import_button'):
             # When the user is not part of the import group
                for node in doc.xpath("//kanban"):
                    # Set the import to false
                    node.set('import', 'false')            
            result['arch'] = etree.tostring(doc)    


            

        return result 

    
    def action_done_show_wizard_level(self):
        for ddtsh in self:
            payment_first = self.env['account.payment'].search([("partner_id",'=',ddtsh.id)],order='id asc', limit=1)
            if payment_first:
                ddtsh.payment_number = payment_first.id
                print("payment_first#################",payment_first)
        print("self._context##################",self._context.get("active_ids"))
        return {'type': 'ir.actions.act_window',
        'name': _('Change the Level Value'),
        'res_model': 'level.value',
        'target': 'new',
        'view_id': self.env.ref('techtime_student_excel.view_any_name_form_level_value').id,
        'view_mode': 'form',
        'context': {"active_id" : self._context.get("active_ids")}
        }




    def send_mis_report_sale_college_report(self):  
        filename = 'جدول الاحصاء الصباحي.xls'
        string = 'جدول الاحصاء الصباحي.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string)
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
        worksheet.col(0).width = 5000
        worksheet.col(1).width = 5000

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

        row = 0
        col = 2
        college_data = self.env["faculty.faculty"].search([])
        # print("college_data$$$$$$$$$$$$$$$$$$$$$$",college_data)
        Registered_total = 0
        format2 = xlwt.easyxf('font:bold True;align: horiz center')
        worksheet.write(1, 0, "الكلية" or '',header_bold)
        worksheet.write(1, 1, "القسم" or '', header_bold)
        for coll in college_data:
            data_total_all = 0
            not_registered_level1 = 0
            not_registered_level2 = 0
            not_registered_level3 = 0
            not_registered_level4 = 0
            not_registered_level5 = 0
            registered_level1 = 0
            registered_level2 = 0
            registered_level3 = 0
            registered_level4 = 0
            registered_level5 = 0
            # for material_line in self:
            # print("lllllllllllllllllllll",material_line.partner_id)
            year_all = self.env["year.year"].search([],order='year asc')
            student_type = ['leve1','level2','level3','level4','level5']
            # print("student_type###################",student_type)
            # _logger.info("student_type************11111111111111#####**%s" %student_type)
            for yrs in year_all:
                print("yrs$$$$$$$$$$$$$$$$$$$$$$$")
                # _logger.info("pincode************222222222222#####**%s" %yrs.year)
            print("yrs@@@@@@@@@@@@@@@@@@@@@@@@@@2$",yrs.year)

            department = self.env['department.department'].search([("college" ,"=", coll.id)]) 
            for ddept in department:
                worksheet.write(col ,0 , coll.college or '', main_cell_total)
                worksheet.write(col ,1 , ddept.department or '', main_cell_total)
                
                row = 2
                female_row = 3
                for student in student_type: 
                    sale_ord_level1_morning_male  = self.filtered(lambda picking:picking.level == student and picking.college.id == coll.id and picking.department.id == ddept.id and picking.shift == 'morning' and picking.gender == 'male')
                    sale_ord_level1_morning_female  = self.filtered(lambda picking:picking.level == student and picking.college.id == coll.id and picking.department.id == ddept.id and picking.shift == 'morning' and picking.gender == 'female')

                    # sale_ord_level1_morning_male = self.env["res.partner"].search([('level','=',student),('college','=',coll.id),('department','=',ddept.id),('shift','=','morning'),('gender','=','male')])
                   
                    # sale_ord_level1_morning_female = self.env["res.partner"].search([('level','=',student),('college','=',coll.id),('department','=',ddept.id),('shift','=','morning'),('gender','=','female')])

                    if student == 'leve1':
                        student = 'المرحلة الاولى'
                    if student == 'level2':
                        student = 'المرحلة الثانية'
                    if student == 'level3':
                        student = 'المرحلة الثالثة'
                    if student == 'level4':
                        student = 'المرحلة الرابعة'
                    if student == 'level5':
                        student = 'المرحلة الخامسة'

                    
                    if col == 2:
                        worksheet.write_merge(0, 0, row, row + 2, student or '', header_bold)
                        print("row@@@@@@@@@@@@@@@@@@@@",row)
                        # worksheet.write(0, row, student.Student or '')
                        
                        worksheet.write(1, row, "الذكور" or '', header_bold)
                        worksheet.write(1, row + 1, "الاناث" or '', header_bold)
                        worksheet.write(1, row + 2, "المجموع" or '', header_bold)


                    
                    worksheet.write(col, row, len(sale_ord_level1_morning_male.mapped("id")) or '', main_cell_total)
                    worksheet.write(col, row + 1, len(sale_ord_level1_morning_female.mapped("id")) or '', main_cell_total)
                    worksheet.write(col, row + 2, len(sale_ord_level1_morning_male.mapped("id")) + len(sale_ord_level1_morning_female.mapped("id")) or '', main_cell_total)
                    data_sale_morning = len(sale_ord_level1_morning_male.mapped("id")) + len(sale_ord_level1_morning_female.mapped("id"))
                    data_total_all = data_total_all + data_sale_morning
                    row = row + 3
                worksheet.write(col, row, data_total_all or '', main_cell_total)    
                col = col + 1
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
    

    def send_mis_report_sale_evening_shift(self):  
        filename = 'جدول الاحصاء المسائي.xls'
        string = 'جدول الاحصاء المسائي.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string)
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
        worksheet.col(0).width = 5000
        worksheet.col(1).width = 5000

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


        col = 2
        college_data = self.env["faculty.faculty"].search([])
        # print("college_data$$$$$$$$$$$$$$$$$$$$$$",college_data)
        Registered_total = 0
        format2 = xlwt.easyxf('font:bold True;align: horiz center')
        worksheet.write(1, 0, "الكلية" or '',header_bold)
        worksheet.write(1, 1, "القسم" or '', header_bold)
        for coll in college_data:
            data_total_all = 0
            not_registered_level1 = 0
            not_registered_level2 = 0
            not_registered_level3 = 0
            not_registered_level4 = 0
            not_registered_level5 = 0
            registered_level1 = 0
            registered_level2 = 0
            registered_level3 = 0
            registered_level4 = 0
            registered_level5 = 0
            # for material_line in self:
            # print("lllllllllllllllllllll",material_line.partner_id)
            year_all = self.env["year.year"].search([],order='year asc')
            student_type = ['leve1','level2','level3','level4','level5']
            # print("student_type###################",student_type)
            # _logger.info("student_type************11111111111111#####**%s" %student_type)
            for yrs in year_all:
                print("yrs$$$$$$$$$$$$$$$$$$$$$$$")
                # _logger.info("pincode************222222222222#####**%s" %yrs.year)
            print("yrs@@@@@@@@@@@@@@@@@@@@@@@@@@2$",yrs.year)

            department = self.env['department.department'].search([("college" ,"=", coll.id)]) 
            for ddept in department:
                worksheet.write(col ,0 , coll.college or '', main_cell_total)
                worksheet.write(col ,1 , ddept.department or '', main_cell_total)
                row = 2
                female_row = 3
                for student in student_type: 
                    sale_ord_level1_afternoon_male  = self.filtered(lambda picking:picking.level == student and picking.college.id == coll.id and picking.department.id == ddept.id and picking.shift == 'afternoon' and picking.gender == 'male')
                    sale_ord_level1_afternoon_female  = self.filtered(lambda picking:picking.level == student and picking.college.id == coll.id and picking.department.id == ddept.id and picking.shift == 'afternoon' and picking.gender == 'female')
                    # sale_ord_level1_afternoon_male = self.env["res.partner"].search([('level','=',student),('college','=',coll.id),('department','=',ddept.id),('shift','=','afternoon'),('gender','=','male')])
                   
                    # sale_ord_level1_afternoon_female = self.env["res.partner"].search([('level','=',student),('college','=',coll.id),('department','=',ddept.id),('shift','=','afternoon'),('gender','=','female')])


                    if student == 'leve1':
                        student = 'المرحلة الاولى'
                    if student == 'level2':
                        student = 'المرحلة الثانية'
                    if student == 'level3':
                        student = 'المرحلة الثالثة'
                    if student == 'level4':
                        student = 'المرحلة الرابعة'
                    if student == 'level5':
                        student = 'المرحلة الخامسة'
                    if col == 2:
                        worksheet.write_merge(0, 0, row, row + 2, student or '', header_bold)
                        # worksheet.write(0, row, student.Student or '')
                        # worksheet.write(1, row - 2, "College" or '')
                        # worksheet.write(1, row - 1, "Department" or '')
                        worksheet.write(1, row, "الذكور" or '',header_bold)
                        worksheet.write(1, row + 1, "الاناث" or '', header_bold)
                        worksheet.write(1, row + 2, "المجموع" or '', header_bold)

                    worksheet.write(col, row, len(sale_ord_level1_afternoon_male.mapped("id")) or '', main_cell_total)
                    worksheet.write(col, row + 1, len(sale_ord_level1_afternoon_female.mapped("id")) or '', main_cell_total)
                    worksheet.write(col, row + 2, len(sale_ord_level1_afternoon_male.mapped("id")) + len(sale_ord_level1_afternoon_female.mapped("id")) or '', main_cell_total)
                    data_sale_morning = len(sale_ord_level1_afternoon_male.mapped("id")) + len(sale_ord_level1_afternoon_female.mapped("id"))
                    data_total_all = data_total_all + data_sale_morning
                    row = row + 3
                
                # worksheet.write(col ,row + 1, coll.college or '', main_cell_total)
                # worksheet.write(col ,row, ddept.department or '', main_cell_total)
                worksheet.write(col, row, data_total_all or '', main_cell_total)
                col = col + 1




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
    

