# -*- coding: utf-8 -*-

from odoo import models, fields, api , _
from odoo.exceptions import UserError

class BaseResPartner(models.Model):
    _inherit = "res.partner"

    class_name = fields.Many2one("student.class", string="Class")

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
    note = fields.Char("Notes")
    students_collage  = fields.Many2one("faculty.faculty", string="Location College")
    student_department = fields.Many2one("department.department", string="Location Department")
    student_class  = fields.Many2one("student.class", string="Location Class")
    student_entity  = fields.Many2many("student.label", string="Student entity")

    @api.model
    def create(self, vals):
        print("vals@@@@@@@@@@@@@@@@@@@@",vals)

        lst = []
        student = ""

        print("self#############",self)

        if 'students_collage' in vals and "student_department" in vals and "student_class" in vals:
            student = self.env["res.partner"].search([("college","=",vals['students_collage']),("department","=",vals["student_department"]),("class_name","=",vals["student_class"])])
        
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
