# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import io
import json
import base64
import xlwt
from datetime import date, datetime, timedelta
from lxml import etree

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
        
        partner_i = self.env["res.partner"].search([("id","in",invoice_id),("college.res_user","in",[self.env.uid])])

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


class ResPart(models.Model):
    _inherit = "res.partner"

    student_discipline = fields.Many2many("student.discipline",store = True, track_visibility=True) 

    @api.onchange('student_discipline')
    def _on_student_discipline(self):
        print("result@@@@@@@@@@@@@@@@eeeeeeeeeee",self.student_discipline)

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super(ResPart, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        
    #     if self.env.user.has_group('almaaqal_student_unpaid.group_student_decipline_read'):  # Replace with your group
    #         doc = etree.XML(res['arch'])

    #         print("doc@@@@@@@@@@@@@@@",doc)
    #         for node in doc.xpath("//page[@name='student_discipline']/group/field[@name='student_discipline']"):
    #             node.set('invisible', '1')  # Hide field
    #         res['arch'] = etree.tostring(doc, encoding='unicode')
        
    #     return res    

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ResPart, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        # if self.env.user.id == self.id:  # For logged-in user condition
        if self.env.user.has_group('almaaqal_student_unpaid.group_student_decipline_write'):    
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='student_discipline']"):
                node.set('readonly', '1')  # Set the field to readonly
                node.set('can_write','false')
                node.set('can_create','false')
                modifiers = {'readonly': True}
                node.set('modifiers', json.dumps(modifiers))
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

class StudentDecipline(models.Model):
    _name = 'student.discipline'
    _description = 'Persistent Model'

    title = fields.Char("Title", track_visibility=True)
    details = fields.Char("Details", track_visibility=True)

    res_part = fields.Many2one("res.partner",string="Partner")   

    attachment = fields.Many2many("ir.attachment",  string="Attachment")


    @api.model
    def create(self, vals):
        print("vals@@@@@@@@@@@@@@@@",vals)
        result = super(StudentDecipline, self).create(vals)

        print("result@@@@@@@@@@@@@@@@",result.res_part)

        result.res_part.message_post(subject=_(result.title), body=("Student Discipline") + result.title + "\n" +result.details, attachment_ids=result.attachment.mapped("id"))

        return result

        



    