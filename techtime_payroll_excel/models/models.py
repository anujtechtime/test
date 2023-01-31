# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import pytz
import threading
from collections import OrderedDict, defaultdict
import re

from datetime import date, datetime, timedelta
from psycopg2 import sql
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


class techtime_payroll_excel(models.Model):
    _inherit = 'hr.payslip'
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


    def send_mis_report(self):
        filename = 'Payslip.xls'
        string = 'Payslip_report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string)
        header_bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")
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

        department_data = self.env["hr.department"].search([])
        call = 1
        for dep in  department_data:
            rested = self.env['hr.payslip'].search([('department','=',dep.id)])
            worksheet.write(call - 1, 0, dep.name, border_color_2)

            worksheet.write(call, 0, 'رقم القصاصة', border_color_2)  # refernce 
            # worksheet.write(call, 1, 'Payslip Name', border_color_2)

            worksheet.write(call, 1, 'اسم الموظف', border_color_2) # employee
            worksheet.write(call, 2, 'التفاصيل', header_bold) # description

            worksheet.write(call, 3, 'الراتب الكلي', header_bold) # wage

            worksheet.write(call, 4, 'الراتب الاسمي', header_bold) #basic salary


            # worksheet.write(call, 4, 'Wage -الراتب الاسميUSD', header_bold)
            worksheet.write(call, 5, 'التعويضية', header_bold) #compensation

            # worksheet.write(call, 7, 'Basic', header_bold)
            worksheet.write(call, 6, 'الضمان الاجتماعي', header_bold) #socaial security
            worksheet.write(call, 7, 'الضريبة', header_bold) #tax
            worksheet.write(call, 8, 'عدد الايام المستقطعة', header_bold) #day deduction
            worksheet.write(call, 9, 'مبلغ الايام المستقطعة', header_bold) #day deduction amount


            worksheet.write(call, 10, 'التدريب والتأهيل', header_bold) #allowance
            worksheet.write(call, 11, 'استقطاع التقاعد', header_bold) #REDED
            worksheet.write(call, 12, 'استقطاعات جامعة البصرة ل I2', header_bold) #BASDED
            worksheet.write(call, 13, 'مجموع الاستقطاعات', header_bold) #total deduction

            worksheet.write(call, 14, 'صافي الراتب', header_bold) # Net Salary
            # v.onboard_date >= (datetime.today().date().replace(day=1) - relativedelta(months=1)) and v.onboard_date <= (datetime.today().date() - relativedelta(months=1))
            for material_line_id in rested:
                worksheet.write(row, 0, material_line_id.number or '')
                # worksheet.write(row, 1, material_line_id.name or '')

                worksheet.write(row, 1, material_line_id.employee_id.name or '')
                worksheet.write(row, 2, re.sub('<[^>]*>', '', material_line_id.description) or '')
                # if material_line_id.contract_id.currency_id.id == 2:
                #     worksheet.write(row, 4, str(material_line_id.contract_id.wage) + "$" or '')

                # if material_line_id.contract_id.currency_id.id == 90:
                worksheet.write(row, 3, "{:,.2f}".format(float(material_line_id.contract_id.wage) + float(material_line_id.contract_id.training_field)) + "ع.د" or '')
                total_basic = 0 
                compensation_data = 0
                tax_data = 0
                day_deduction_data = 0
                day_deduction_amount_data = 0
                allowance_data = 0
                reded = 0
                basded = 0
                total_ded_data = 0
                for iit in material_line_id.line_ids:
                    if iit.code == "BSCC":
                        worksheet.write(row, 4, "{:,.2f}".format(float(iit.total)) or '')
                        total_basic = total_basic + iit.total
                    if iit.code == "CMPS":
                        worksheet.write(row, 5, "{:,.2f}".format(float(iit.total)) or '')
                        compensation_data = compensation_data + iit.total
                    # if iit.code == "WAG":    
                    #     worksheet.write(row, 7, iit.total or '')
                    if iit.code == "SST":    
                        worksheet.write(row, 6, "{:,.2f}".format(float(iit.total)) or '')
                        socailsecurity_data = socailsecurity_data + iit.total
                    if iit.code == "TAX":
                        worksheet.write(row, 7, "{:,.2f}".format(float(iit.total)) or '')
                        tax_data = tax_data + iit.total
                    if iit.code == "day2":    
                        worksheet.write(row, 8, "{:,.2f}".format(float(iit.total)) or '')
                        day_deduction_data = day_deduction_data + iit.total

                    if iit.code == "DDTA":    
                        worksheet.write(row, 9, "{:,.2f}".format(float(iit.total)) or '')  
                        day_deduction_amount_data = day_deduction_amount_data + iit.total  

                        
                    if iit.code == "TRA"  or iit.code == "DAYALL"  or iit.code == "AEAA" or iit.code == "TRAMU":    
                        worksheet.write(row, 10, "{:,.2f}".format(float(iit.total)) or '')
                        allowance_data = allowance_data + iit.total

                    if iit.code == "REDED":    
                        worksheet.write(row, 11, "{:,.2f}".format(float(iit.total)) or '')
                        reded = reded + iit.total
                        
                    if iit.code == "BASDED":    
                        worksheet.write(row, 12, "{:,.2f}".format(float(iit.total)) or '')
                        basded = basded + iit.total
                        
                    if iit.code == "TTD":    
                        worksheet.write(row, 13, "{:,.2f}".format(float(iit.total)) or '')
                        total_ded_data = total_ded_data + iit.total
                        
                    if iit.code == "NET2" or iit.code == "GROSS" or iit.code == "NTS" or iit.code == "NETS" or iit.code == "NTTS":    
                        worksheet.write(row, 14, "{:,.2f}".format(float(iit.total)) or '')
                        net_saled_data = net_saled_data + iit.total
                row += 1
            call = row + 2 
            row += 3   
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

        