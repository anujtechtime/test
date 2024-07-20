# -*- coding: utf-8 -*-

from odoo import models, fields, api, _ 


class AlmaaqalGrade(models.Model):
    _name = 'almaaqal.grade'
    _description = 'Almaaqal Grade'

    college_in_english =  fields.Char("College in English")
    college_in_arabic =  fields.Char("College in Arabic")
    department_in_english =  fields.Char("Department in English")
    department_in_arabic =  fields.Char("Department in Arabic")
    year_of_graduation =  fields.Char("Year of graduation") 
    exam_number_for_reference =  fields.Char("Exam Number for Reference")
    student_name_in_english =  fields.Char("Student Name in English")
    student_name_in_arabic =  fields.Char("Student Name in Arabic")
    average =  fields.Char("Average") 
    notes_in_arabic =  fields.Char("notes in arabic")     
    notes_in_english =  fields.Char("Notes in english") 
    subject = fields.Many2many("subject.subject")   

    
class Subject(models.Model):
    _name = "subject.subject"
    _description = "Subject"


    subject_arabic = fields.Char("Subject Arabic")    
    subject_english = fields.Char("Subject English")   
    subject_units = fields.Char("Subject Units") 
    subject_grade = fields.Char("Subject Grade") 


#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
