# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import io
import json
import base64
import xlwt
from datetime import date, datetime, timedelta

class DueStudentWizard(models.TransientModel):
    _name = 'due.student.wizard'

    
    requested_costumer = fields.Many2many("res.partner",string="Customer")
    date_start = fields.Date("Date Start")
    date_end = fields.Date("Date End")

    def action_done(self):
        print("@@@@@@@@@@@@@@",self)
        filename = 'profit_report.xls'
        string = 'profit_report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string, cell_overwrite_ok=True)
        # worksheet.cols_right_to_left = True
        header_bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")
        cell_format = xlwt.easyxf()
        filename = 'Student_Report_%s.xls' % date.today()
        rested = self.env['sale.order'].search([])
        row = 1
        border_normal = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; font: bold on;')
        border_1 = xlwt.easyxf('borders: left 1, right 1, top 1, bottom 1;')
        border_2 = xlwt.easyxf('borders: left 2, right 2, top 2, bottom 2;')
        border_color_2 = xlwt.easyxf('borders: top_color blue, bottom_color blue, right_color blue, left_color blue, left 2, right 2, top 2, bottom 2; font: bold on; pattern: pattern solid, fore_colour gray25;')
        # worksheet.col(0).width = 10000
        # worksheet.col(1).width = 15000
        # worksheet.col(2).width = 10000
        worksheet.col(1).width = 15000
        worksheet.col(2).width = 15000

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
        col = 0
        count = 1

        
        
        worksheet.write(row, 0, 'Student Name', header_bold) #sequence
        worksheet.write(row, 1, 'Exam Number', header_bold) #sequence


        row = 1

        invoice_data = self.env["account.move"].search([("invoice_payment_state","=","not_paid"),("type","=","out_invoice")]) 
        print("invoice_data@@@@@@@@@@@@@@@@@@@@@@",list(set(invoice_data.mapped("partner_id.id"))))
        lst = []
        invoice_id = list(set(invoice_data.mapped("partner_id.id")))
        
        partner_i = self.env["res.partner"].search([("id","in",invoice_id)])

        print("partner_i##############",partner_i)
        
        for pr in partner_i:
            worksheet.write(row, col, pr.display_name, border_normal) #sequence
            worksheet.write(row, col + 1, pr.number_exam, border_normal) #sequence
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