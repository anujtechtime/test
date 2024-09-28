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
from datetime import date, datetime, timedelta
import html2text

_logger = logging.getLogger(__name__)


class almaaqal_request_transfering(models.Model):
    _inherit = 'res.partner'

    def print_transfer(self):
        # Generate PDF report
        report = self.env.ref('almaaqal_request_transfering.report_payment_receipt_request_of_transferring')

        pdf_content, _ = report.render_qweb_pdf(res_ids=self.ids)

        sale_ord = self.env["sale.order"].search([("partner_id","=",self.id),("year","=",self.year.id)],limit=1)
        count = 0
        for inv in sale_ord.sale_installment_line_ids:
            if count == 0 and inv.payment_status != 'paid':
                raise ValidationError('الدفعه الاولئ غير مدفوعه!')
            count = count + 1

        # Convert PDF to base64
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

        # Create attachment
        attachment = self.env['ir.attachment'].create({
            'name': 'Request_of_transferring_shift.pdf',
            'type': 'binary',
            'datas': pdf_base64,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf'
        })

        self.message_post(
            body="Request of transferring (PDF),",
            attachment_ids=[attachment.id]
        )


        return self.env.ref('almaaqal_request_transfering.report_payment_receipt_request_of_transferring').report_action(self)   

    def student_detailed_report(self):
        filename = 'جدول الاحصاء الصباحي.xls'
        string = 'جدول الاحصاء الصباحي.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string, cell_overwrite_ok=True)
        # worksheet.cols_right_to_left = True
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
                      font: bold on;  align: horiz centre; align: vert centre")


        main_cell_total_of_total = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour lime; align: horiz centre; align: vert centre")
        tttyl = xlwt.easyxf("align: horiz centre; align: vert centre")

        row = 0
        

        worksheet.write_merge(row, row, 0, 13, "جامعة المعقل", main_cell_total) #almaaqal university

        row = row + 1

        count = 0
        deptmt = ""
        level = ""
        shift = ""
        year = ""
        depp = ""
        shift_name = ""

        for dep in self:
            if count == 0:
                
                lev = dep.level
                shift = dep.shift

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

                deptmt = dep.department.department
                level = depp
                shift = shift_name
                year = dep.year.year
            count = count + 1

        worksheet.write_merge(row, row, 0, 13, deptmt, main_cell_total) #almaaqal university

        row = row + 1
        worksheet.write_merge(row, row, 0, 13, level + " - " + shift, main_cell_total) #almaaqal university

        row = row + 1
        worksheet.write_merge(row, row, 0, 13, year, main_cell_total) #almaaqal university

        row = row + 2
        col = 0


        worksheet.write_merge(row, row + 1, col, col, "ت", main_cell_total) #Serial
        col = col + 1
        worksheet.write_merge(row, row + 1, col, col, "الاسم", main_cell_total) #Student name in AR
        col = col + 1
        worksheet.write_merge(row, row + 1, col, col, "الحالة الدراسية", main_cell_total) #Student status
        col = col + 1
        worksheet.write_merge(row, row + 1, col, col, "الرقم الوزاري", main_cell_total) #Exam Number

        col = col + 1
        worksheet.write_merge(row, row + 1, col, col, "الرقم الجامعي", main_cell_total) #college Number

        col = col + 1
        worksheet.write_merge(row, row, col, col + 1, "موبايل", main_cell_total) #mobile Number
        # worksheet.write_merge(row + 1, row, col, col + 1, "موبايل", main_cell_total) #mobile Number

        worksheet.write(row + 1, col, ' الطالب', main_cell_total) #phone
        worksheet.write(row + 1, col + 1, 'ولي الامر', main_cell_total) #mobile date

        col = col + 2
        worksheet.write_merge(row, row + 1, col, col, "وثيقة سادس", main_cell_total) #file

        col = col + 1
        worksheet.write_merge(row, row, col, col + 5, "الاقساط الدراسية", main_cell_total) #Payment

        worksheet.write(row + 1, col, 'اول', main_cell_total) #installment
        worksheet.write(row + 1, col + 1, 'رقم الوصل ', main_cell_total) #invoice number

        col = col + 2

        worksheet.write(row + 1, col, 'اول', main_cell_total) #installment
        worksheet.write(row + 1, col + 1, 'رقم الوصل ', main_cell_total) #invoice number

        col = col + 2

        worksheet.write(row + 1, col, 'اول', main_cell_total) #installment
        worksheet.write(row + 1, col + 1, 'رقم الوصل ', main_cell_total) #invoice number

        # worksheet.write(row, 1, 'التاريخ', header_bold) #payment date
        # worksheet.write(row, 2, 'رقم الوصل', header_bold) #payment number
        # worksheet.write(row, 3, 'الاسم', header_bold) # Student Name
        # worksheet.write(row, 4, 'المبلغ', header_bold) # total amout
        # worksheet.write(row, 5, 'رقم الحساب', header_bold) # Account/invoice lines
        # worksheet.write(row, 6, 'الحالة', header_bold) # Status


        
        serial = 1
        row = row + 2
        for val in self:
            col = 0
            worksheet.write(row, col, serial, main_cell_total) #Serial
            serial = serial + 1
            col = col + 1
            worksheet.write(row, col, val.name, main_cell_total) #Student name in AR
            col = col + 1
            worksheet.write(row, col, val.Status, main_cell_total) #Student status
            col = col + 1
            worksheet.write(row, col, val.number_exam, main_cell_total) #Exam Number

            col = col + 1
            worksheet.write(row, col, val.college_number, main_cell_total) #college Number

            col = col + 1
            # worksheet.write_merge(row + 1, row, col, col + 1, "موبايل", main_cell_total) #mobile Number

            worksheet.write(row, col, val.phone, main_cell_total) #phone
            worksheet.write(row, col + 1, val.mobile, main_cell_total) #mobile date

            col = col + 2
            if val.file_upload:
                worksheet.write(row, col, "تم" , main_cell_total) #file
            if not val.file_upload:
                worksheet.write(row, col, "لم يتم" , main_cell_total) #file    

            col = col + 1

            sale_order  = self.env["sale.order"].search([("department","=",val.department.id),("level","=",val.level),("Subject","=",val.shift),("year","=",val.year.id)], limit=1)
            for dat in sale_order.sale_installment_line_ids:
                if dat.payment_status == "paid":
                    worksheet.write(row, col, 'سدد', main_cell_total) #installment
                if dat.payment_status == "not_paid":
                    worksheet.write(row, col, 'لم يسدد', main_cell_total) #installment  

                worksheet.write(row, col + 1, dat.invoice_id.name, main_cell_total) #invoice number
                col = col + 2
            row = row + 1
            # worksheet.write(row + 1, col, 'اول', main_cell_total) #installment
            # worksheet.write(row + 1, col + 1, 'رقم الوصل ', main_cell_total) #invoice number

            # col = col + 2

            # worksheet.write(row + 1, col, 'اول', main_cell_total) #installment
            # worksheet.write(row + 1, col + 1, 'رقم الوصل ', main_cell_total) #invoice number

        
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
        # worksheet.write(row + 1, 4, '{:,}'.format(total_of_amount_with_account_4395), main_cell_total_of_total)
