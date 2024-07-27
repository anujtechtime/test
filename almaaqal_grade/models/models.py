# -*- coding: utf-8 -*-

from odoo import models, fields, api, _ 


class AlmaaqalGrade(models.Model):
    _name = 'almaaqal.grade'
    _description = 'Almaaqal Grade'

    exam_number_for_reference =  fields.Char("Exam Number")

    college_in_english =  fields.Char("College in EN")
    college_in_arabic =  fields.Char("College in AR")

    study_type_arabic = fields.Char("Study Type AR")
    study_type_english = fields.Char("Study Type EN")

    gender = fields.Char("Gender")


    certificate_name_department_AR = fields.Char("Certificate Name/Department AR")
    certificate_name_department_EN = fields.Char("Certificate Name/Department EN")

    University_order_number = fields.Char("University order number")
    University_order_date = fields.Date("University order date")



    department_in_english =  fields.Char("Department in EN")
    department_in_arabic =  fields.Char("Department in AR")


    stage_year = fields.Char("Stage Year")

    year_of_graduation =  fields.Char("Year of graduation") 
    
    student_name_in_english =  fields.Char("Student Name in EN")
    student_name_in_arabic =  fields.Char("Student Name in AR")

    nationality_ar = fields.Char("Nationality AR")
    nationality_en = fields.Char("Nationality EN")

    average =  fields.Char("Average") 

    average_in_words_en = fields.Char("Average in Words EN")
    average_in_words_ar = fields.Char("Average in Words AR")


    attempt_en = fields.Char("Attempt EN")  
    attempt_ar = fields.Char("Attempt AR")



    study_notes_in_arabic =  fields.Char("notes in arabic")     
    study_notes_in_english =  fields.Char("Notes in english") 

    study_year_name_ar = fields.Char("Study Year Name AR")  
    study_year_name_en = fields.Char("Study Year Name EN")

    # subject = fields.Many2many("subject.subject")  


    subject_1_arabic = fields.Char("Subject 1 Arabic")
    subject_1_english = fields.Char("Subject 1 English")
    subject_1_units = fields.Char("Subject 1 Units")
    subject_1_grade = fields.Char("Subject 1 Grade") 

    subject_2_arabic = fields.Char("Subject 2 Arabic")
    subject_2_english = fields.Char("Subject 2 English")
    subject_2_units = fields.Char("Subject 2 Units")
    subject_2_grade = fields.Char("Subject 2 Grade") 

    subject_3_arabic = fields.Char("Subject 3 Arabic")
    subject_3_english = fields.Char("Subject 3 English")
    subject_3_units = fields.Char("Subject 3 Units")
    subject_3_grade = fields.Char("Subject 3 Grade") 

    subject_4_arabic = fields.Char("Subject 4 Arabic")
    subject_4_english = fields.Char("Subject 4 English")
    subject_4_units = fields.Char("Subject 4 Units")
    subject_4_grade = fields.Char("Subject 4 Grade") 

    subject_5_arabic = fields.Char("Subject 5 Arabic")
    subject_5_english = fields.Char("Subject 5 English")
    subject_5_units = fields.Char("Subject 5 Units")
    subject_5_grade = fields.Char("Subject 5 Grade") 

    subject_6_arabic = fields.Char("Subject 6 Arabic")
    subject_6_english = fields.Char("Subject 6 English")
    subject_6_units = fields.Char("Subject 6 Units")
    subject_6_grade = fields.Char("Subject 6 Grade") 

    subject_7_arabic = fields.Char("Subject 7 Arabic")
    subject_7_english = fields.Char("Subject 7 English")
    subject_7_units = fields.Char("Subject 7 Units")
    subject_7_grade = fields.Char("Subject 7 Grade") 

    subject_8_arabic = fields.Char("Subject 8 Arabic")
    subject_8_english = fields.Char("Subject 8 English")
    subject_8_units = fields.Char("Subject 8 Units")
    subject_8_grade = fields.Char("Subject 8 Grade") 

    subject_9_arabic = fields.Char("Subject 9 Arabic")
    subject_9_english = fields.Char("Subject 9 English")
    subject_9_units = fields.Char("Subject 9 Units")
    subject_9_grade = fields.Char("Subject 9 Grade") 

    subject_10_arabic = fields.Char("Subject 10 Arabic")
    subject_10_english = fields.Char("Subject 10 English")
    subject_10_units = fields.Char("Subject 10 Units")
    subject_10_grade = fields.Char("Subject 10 Grade") 

    subject_11_arabic = fields.Char("Subject 11 Arabic")
    subject_11_english = fields.Char("Subject 11 English")
    subject_11_units = fields.Char("Subject 11 Units")
    subject_11_grade = fields.Char("Subject 11 Grade") 

    subject_12_arabic = fields.Char("Subject 12 Arabic")
    subject_12_english = fields.Char("Subject 12 English")
    subject_12_units = fields.Char("Subject 12 Units")
    subject_12_grade = fields.Char("Subject 12 Grade") 

    subject_13_arabic = fields.Char("Subject 13 Arabic")
    subject_13_english = fields.Char("Subject 13 English")
    subject_13_units = fields.Char("Subject 13 Units")
    subject_13_grade = fields.Char("Subject 13 Grade") 

    subject_14_arabic = fields.Char("Subject 14 Arabic")
    subject_14_english = fields.Char("Subject 14 English")
    subject_14_units = fields.Char("Subject 14 Units")
    subject_14_grade = fields.Char("Subject 14 Grade") 

    subject_15_arabic = fields.Char("Subject 15 Arabic")
    subject_15_english = fields.Char("Subject 15 English")
    subject_15_units = fields.Char("Subject 15 Units")
    subject_15_grade = fields.Char("Subject 15 Grade") 


    
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
