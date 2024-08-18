# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CertiPartner(models.Model):
    _inherit = "res.partner"

    grade = fields.Float("Grade")
    graduation_sequence = fields.Integer("Graduation Sequence")

    def name_get(self):
        result = []
        for record in self:
            if self.env.context.get('display_number_exam'):
                # Display email if the context key is set
                display_value = record.number_exam or record.name
            else:
                # Default display value
                display_value = record.name
            result.append((record.id, display_value))
        return result


class AlmaaqalCertificate(models.Model):
    _name = 'almaaqal.certificate'
    _description = 'Certificate'

    student = fields.Many2one("res.partner", string="Student", context={'display_number_exam': True})

    number = fields.Char("Number")
    date = fields.Date("Date")
    Status = fields.Selection([('draft','Draft'),('posted','Posted')], string="Status")

    type_d = fields.Selection([('arabic_no_grades','Arabic No Grades'),('english_no_grades','English No Grades'),('arabic_with_grades','Arabic with Grades'),('english_with_grades','English With Grades'),], string="Type") 

    # Student (Connected to student module: Partner)
    name_in_arabic =  fields.Char(string="Name in Arabic", readonly=True, store=True)
    name_in_english = fields.Char("Name in English", readonly=True , store=True)
    college = fields.Char(string="College", readonly=True, store=True)
    department = fields.Char(string="Department", readonly=True, store=True)
    grade = fields.Float("Grade", readonly=True, store=True)
    graduation_sequence = fields.Integer("Graduation Sequence", readonly=True, store=True)
    year_name_graduation_year = fields.Char( string="Year Name Graduation year", readonly=True, store=True)  
    notes = fields.Text("Notes", readonly=True, store=True)

    grade_year = fields.Many2many("almaaqal.grade", string="Grade")

    @api.onchange('student')
    def _on_change_student(self):
        self.name_in_arabic = self.student.name
        self.name_in_english = self.student.name_english
        self.college = self.student.college.college
        self.department = self.student.department.department
        self.grade = self.student.grade
        self.graduation_sequence = self.student.graduation_sequence
        self.year_name_graduation_year = self.student.year_of_collage_graduation.name
        self.notes = self.student.notes


        exam_no = self.env["almaaqal.grade"].search([("exam_number_for_reference","=",self.student.number_exam)])
        if exam_no:
            self.grade_year = [(4, exam_no.id)]

        print("grade_year@@@@@@@@@@@@@@@@@@",self.grade_year)

    @api.model
    def create(self, vals):
        if 'student' in vals:
            student_v  = self.env["res.partner"].search([("id",'=',vals['student'])])
            vals['name_in_arabic'] = student_v.name
            vals['name_in_english'] = student_v.name_english
            vals['college'] = student_v.college.college
            vals['department'] = student_v.department.department
            vals['grade'] = student_v.grade
            vals['graduation_sequence'] = student_v.graduation_sequence
            vals['year_name_graduation_year'] = student_v.year_of_collage_graduation.name
            vals['notes'] = student_v.notes
        return super(AlmaaqalCertificate, self).create(vals)    

    def write(self, vals):
        print("vals@@@@@@@@@@@@@@@@",vals)
        if 'student' in vals:
            student_v  = self.env["res.partner"].search([("id",'=',vals['student'])])
            vals['name_in_arabic'] = student_v.name
            vals['name_in_english'] = student_v.name_english
            vals['college'] = student_v.college.college
            vals['department'] = student_v.department.department
            vals['grade'] = student_v.grade
            vals['graduation_sequence'] = student_v.graduation_sequence
            vals['year_name_graduation_year'] = student_v.year_of_collage_graduation.name
            vals['notes'] = student_v.notes
        return super(AlmaaqalCertificate, self).write(vals)    



