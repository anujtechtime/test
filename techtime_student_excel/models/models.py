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


class TechtimeStudentexcel(models.Model):
    _inherit = 'sale.order'
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
