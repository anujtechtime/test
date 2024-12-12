# -*- coding: utf-8 -*-

from odoo import models, fields, api , _
from odoo.exceptions import UserError
import xlwt
from xlwt import Workbook, easyxf
import io
import base64


class BaseResPartner(models.Model):
    _inherit = "res.partner"

    class_name = fields.Many2one("student.class", string="الشعبة")

class AlmaaqalStudentClass(models.Model):
    _name = 'student.class'
    _description = 'Student Class'

    name = fields.Char("Class Name")

class AlmaaqalHall(models.Model):
    _name = 'exam.hall'
    _description = 'Exam Hall'

    name = fields.Char("Hall Name", required=True)
    location_collage = fields.Many2one("faculty.faculty",string="Location College")
    location_floor = fields.Integer("Location Floor")
    location_building = fields.Integer("Location Building")
    location_department = fields.Many2one("department.department",string="Location Department") 
    seats = fields.Integer("Seats", required=True) 
    rows = fields.Integer("Rows", required=True)
    columns = fields.Integer("Columns", required=True)
    booking_entity = fields.Many2many("booking.entry",string="Booking entity", required=True)

class AlmaaqalBooking(models.Model):
    _name = 'booking.entry'
    _description = 'Booking Entry'

    booking_date = fields.Date("Booking Date", required=True)
    hall_entry = fields.Many2one("exam.hall", string="Hall Entry")
    booking_time_from  = fields.Float("Booking Time From", required=True)
    booking_time_to = fields.Float("Booking Time To", required=True)
    note = fields.Char("Title")
    students_collage  = fields.Many2one("faculty.faculty", string="Student College")
    student_department = fields.Many2one("department.department", string="Student Department")
    student_class  = fields.Many2one("student.class", string="Student Class")
    student_level = fields.Selection([('leve1','المرحلة الاولى'),('level2','المرحلة الثانية'),('level3','المرحلة الثالثة'),('level4','المرحلة الرابعة'),('level5','المرحلة الخامسة')], string="Student Level")
    student_shift = fields.Selection([('morning','Morning'),('afternoon','AfterNoon')], string="Student Shift")
    student_entity  = fields.Many2many("student.label", string="Student entity")
    

    @api.model
    def create(self, vals):
        print("vals@@@@@@@@@@@@@@@@@@@@",vals)

        lst = []
        student = ""

        print("self#############",self)

        if 'students_collage' in vals and "student_department" in vals and "student_class" in vals and "student_shift" in vals:
            student = self.env["res.partner"].search([("college","=",vals['students_collage']),("department","=",vals["student_department"]),("class_name","=",vals["student_class"]),("level","=",vals["student_level"]),("shift","=",vals["student_shift"])])
        
        if "hall_entry" in vals:
            hall = self.env["exam.hall"].browse(int(vals['hall_entry']))

            if vals['hall_entry'] and student and  hall.seats < len(student.mapped("id")):
                raise UserError(_('This Hall have the capacity of "%s". and student is "%s') % (hall.seats, len(student.mapped("id"))))

        if student:
            for stud in student:
                label = self.env["student.label"].create({
                    "student_name" : stud.id,
                    "student_class" : vals["student_class"],
                    "student_exam_id" : stud.number_exam,
                    })
                print("label@@@@@@@@@@@@@@@@@",label)
                lst.append(label.id)
            vals["student_entity"] = lst

        res =  super(AlmaaqalBooking, self).create(vals)
        print("res@@@@@@@@@@@@@@@@@",res)
        res.hall_entry.booking_entity = [(4, res.id)]
        return res

    def report_for_student_label(self):
        filename = 'Student Label.xls'
        string = 'Student Label.xls'
        wb = xlwt.Workbook(encoding='utf-8')

        # Add a sheet
        ws = wb.add_sheet(string)

        # Define styles
        header_style = easyxf('font: bold 1, height 280; align: vert centre, horiz center')
        sub_header_style = easyxf('font: height 220; align: vert centre, horiz center')
        border_style = easyxf('font: height 280; align: wrap on, vert centre, horiz center; borders: left thin, right thin, top thin, bottom thin')
        arabic_text_style = easyxf('align: vert centre, horiz right')
        depp = ""
        if self.student_level == 'leve1':
            depp = 'المرحلة الاولى'
        if self.student_level == 'level2':
            depp = 'المرحلة الثانية'
        if self.student_level == 'level3':
            depp = 'المرحلة الثالثة'
        if self.student_level == 'level4':
            depp = 'المرحلة الرابعة'
        if self.student_level == 'level5':
            depp = 'المرحلة الخامسة'

        # Add header and sub-header information
        ws.write_merge(0, 0, 1, 7, self.students_collage.college + "-" + self.student_department.department, header_style)
        ws.write_merge(1, 1, 1, 7, 'Hall Name = %s  CAPACITY = %s  BUILDING = %s  FLOOR = %s CLASS = %s LEVEL= %s  SHIFT = %s' % (self.hall_entry.name ,self.hall_entry.seats, self.hall_entry.location_building ,self.hall_entry.location_floor, self.student_class.name, depp, self.student_shift), header_style)
        ws.write_merge(2, 2, 1, 7, "Students Number - %s" % len(self.student_entity.mapped("id")) , header_style)

        # Set column widths
        ws.col(1).width = 280 * 60

        ws.row(4).height_mismatch = True
        ws.row(4).height = 30 * 30

        # Define data

        # Populate the data into the worksheet
        row_start = 4

        rows = 1
        columns = 1
        col = 1
        for std in self.student_entity:
            ws.write(row_start, columns, std.student_name.name + " \n " + self.students_collage.college + " | "  + std.student_class.name + " | " + depp + "  R=" + str(rows) + "  Col=" + str(col) or '', border_style)  #status
            
            if col == self.hall_entry.columns:
                row_start = row_start + 2
                rows = rows + 1
                columns = 1
                col = 1



                ws.row(row_start).height_mismatch = True
                ws.row(row_start).height = 30 * 30

            else:
                columns = columns + 2
                col = col + 1

                ws.col(columns).width = 280 * 60

        print("row_start##################",row_start - 4)  
        print("col#333333333333333333",col)  

        # columns = columns + 2
        if col <= self.hall_entry.columns:
            for i in range(self.hall_entry.columns - col + 1):
                ws.write(row_start, columns, '', border_style)  #status
                columns = columns + 2
        
        print("row_start###############",rows)
        # row_left = row_start - 3

        # if row_left == 1:
        row_left = self.hall_entry.rows - rows
        columns = 1
        col = 1
        row_start = row_start + 2
        ws.row(row_start).height_mismatch = True
        ws.row(row_start).height = 30 * 30

        print("row_left@@@@@@@@@@@@@@@@",row_left)

        print("self.hall_entry.columns@@@@@@@@@@@@@@@@",self.hall_entry.columns)


        for i in range(row_left * self.hall_entry.columns):

            ws.write(row_start, columns, '', border_style)  #status

            if col == self.hall_entry.columns:
                row_start = row_start + 2
                rows = rows + 1
                columns = 1
                col = 1



                ws.row(row_start).height_mismatch = True
                ws.row(row_start).height = 30 * 30

            else:
                print("columns@@@@@@@@@@",columns)
                columns = columns + 2
                col = col + 1

                ws.col(columns).width = 280 * 60



                        
        fp = io.BytesIO()
        wb.save(fp)
        # print(wb)
        out = base64.encodebytes(fp.getvalue())
        attachment = {
                       'name': str(filename),
                       'display_name': str(filename),
                       'datas': out,
                       'type': 'binary'
                   }
        ir_id = self.env['ir.attachment'].create(attachment) 

        xlDecoded = base64.b64decode(out)

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        download_url = '/web/content/' + str(ir_id.id) + '?download=true'
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }          




class AlmaaqalStudent(models.Model):
    _name = 'student.label'
    _description = 'Student label'

    student_name  = fields.Many2one("res.partner", string="Student Name", required=True)
    student_class = fields.Many2one("student.class", string="Student Class")
    student_exam_id  = fields.Char("Exam ID")
    is_Paid = fields.Boolean("Is Paid")
    is_full_data = fields.Char("Is Full Data")

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
