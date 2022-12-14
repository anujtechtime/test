# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import pytz
import threading
from collections import OrderedDict, defaultdict
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

        worksheet.write(0, 2, 'Employe Name-??????     ????????????', border_color_2)
        worksheet.write(0, 3, 'Jop ID-??????????????', header_bold)
        worksheet.write(0, 4, 'Basic -???????????? ????????????USD', header_bold)
        worksheet.write(0, 5, 'Basic -???????????? ????????????IQD', header_bold)
        worksheet.write(0, 6, 'Incentives-??????????????', header_bold)
        worksheet.write(0, 7, 'bonus-????????????????', header_bold)
        worksheet.write(0, 8, 'DEDUCTION-????????????????', header_bold)
        worksheet.write(0, 9, 'Social Security', header_bold)
        worksheet.write(0, 10, 'Deduction Amount', header_bold)
        worksheet.write(0, 11, 'over time', header_bold)
        worksheet.write(0, 12, 'Net IQD', header_bold)
        worksheet.write(0, 13, 'Net USD', header_bold)
        # v.onboard_date >= (datetime.today().date().replace(day=1) - relativedelta(months=1)) and v.onboard_date <= (datetime.today().date() - relativedelta(months=1))
        for material_line_id in self:
            worksheet.write(row, 0, material_line_id.number or '')
            worksheet.write(row, 1, material_line_id.name or '')

            worksheet.write(row, 2, material_line_id.employee_id.name or '')
            worksheet.write(row, 3, material_line_id.employee_id.job_id.name or '')
            if material_line_id.contract_id.currency_id.id == 2:
                worksheet.write(row, 4, str(material_line_id.contract_id.wage) + "$" or '')

            if material_line_id.contract_id.currency_id.id == 90:
                worksheet.write(row, 5, str(material_line_id.phone1) + "??.??" or '')

            for iit in material_line_id.line_ids:
                if iit.code == "INC":
                    worksheet.write(row, 6, iit.total or '')
                if iit.code == "BONUS":
                    worksheet.write(row, 7, iit.total or '')
                if iit.code == "DEDUCTION":    
                    worksheet.write(row, 8, iit.total or '')
                if iit.code == "SOCIAL":    
                    worksheet.write(row, 9, iit.total or '')
                if iit.code == "DEDUCTIONAMOUNT":
                    worksheet.write(row, 10, iit.total or '')
                if iit.code == "OVERTIME":    
                    worksheet.write(row, 11, iit.total or '')
                if iit.code == "NET":    
                    worksheet.write(row, 12, iit.total or '')
                if iit.code == "NETUSD":    
                    worksheet.write(row, 13, iit.total or '')
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
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
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

        worksheet.write(0, 2, 'Employe Name-??????     ????????????', border_color_2)
        worksheet.write(0, 3, 'Jop ID-??????????????', header_bold)
        worksheet.write(0, 4, 'Basic -???????????? ????????????USD', header_bold)
        worksheet.write(0, 5, 'Basic -???????????? ????????????IQD', header_bold)
        worksheet.write(0, 6, 'Incentives-??????????????', header_bold)
        worksheet.write(0, 7, 'bonus-????????????????', header_bold)
        worksheet.write(0, 8, 'DEDUCTION-????????????????', header_bold)
        worksheet.write(0, 9, 'Social Security', header_bold)
        worksheet.write(0, 10, 'Deduction Amount', header_bold)
        worksheet.write(0, 11, 'over time', header_bold)
        worksheet.write(0, 12, 'Net IQD', header_bold)
        worksheet.write(0, 13, 'Net USD', header_bold)
        # v.onboard_date >= (datetime.today().date().replace(day=1) - relativedelta(months=1)) and v.onboard_date <= (datetime.today().date() - relativedelta(months=1))
        for material_line_id in self.slip_ids:
            worksheet.write(row, 0, material_line_id.number or '')
            worksheet.write(row, 1, material_line_id.name or '')

            worksheet.write(row, 2, material_line_id.employee_id.name or '')
            worksheet.write(row, 3, material_line_id.employee_id.job_id.name or '')
            if material_line_id.contract_id.currency_id.id == 2:
                worksheet.write(row, 4, str(material_line_id.contract_id.wage) + "$" or '')

            if material_line_id.contract_id.currency_id.id == 90:
                worksheet.write(row, 5, str(material_line_id.phone1) + "??.??" or '')

            for iit in material_line_id.line_ids:
                if iit.code == "INC":
                    worksheet.write(row, 6, iit.total or '')
                if iit.code == "BONUS":
                    worksheet.write(row, 7, iit.total or '')
                if iit.code == "DEDUCTION":    
                    worksheet.write(row, 8, iit.total or '')
                if iit.code == "SOCIAL":    
                    worksheet.write(row, 9, iit.total or '')
                if iit.code == "DEDUCTIONAMOUNT":
                    worksheet.write(row, 10, iit.total or '')
                if iit.code == "OVERTIME":    
                    worksheet.write(row, 11, iit.total or '')
                if iit.code == "NET":    
                    worksheet.write(row, 12, iit.total or '')
                if iit.code == "NETUSD":    
                    worksheet.write(row, 13, iit.total or '')
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
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        download_url = '/web/content/' + str(ir_id.id) + '?download=true'
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }    

