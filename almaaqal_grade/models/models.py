# -*- coding: utf-8 -*-

from odoo import models, fields, api, _ 
from datetime import date


class AlmaaqalGrade(models.Model):
    _name = 'almaaqal.grade'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Almaaqal Grade'


    Status = fields.Selection([('draft','Draft'),('posted','Posted'),('final_approved','Final Approved')], string="Status", default="draft")
    

    exam_number_for_reference =  fields.Char("Exam Number")

    college_in_english =  fields.Char("College in EN")
    college_in_arabic =  fields.Char("College in AR")

    study_type_arabic = fields.Char("Study Type AR")
    study_type_english = fields.Char("Study Type EN")

    serial = fields.Char("Serial")

    gender = fields.Char("Gender")

    subject_to_arabic = fields.Char("Subject to Arabic")
    subject_to_english = fields.Char("Subject to English")

    certificate_name_department_AR = fields.Char("Certificate Name/Department AR")
    certificate_name_department_EN = fields.Char("Certificate Name/Department EN")

    University_order_number = fields.Char("University order number")
    University_order_date = fields.Date("University order date")

    dean_collage_name_arabic = fields.Char("Dean Collage Name AR")
    dean_collage_name_english = fields.Char("Dean Collage Name EN")

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

    Graduate_Sequence = fields.Char("Graduate Sequence")
    The_average_of_the_first_student_in_the_class = fields.Char("The average of the first student in the class")
    Total_number_of_graduates  = fields.Char("Total number of graduates ")


    # subject = fields.Many2many("subject.subject")  


    subject_1_arabic = fields.Char("Subject 1 Arabic")
    subject_1_english = fields.Char("Subject 1 English")
    subject_1_units = fields.Char("Subject 1 Units")
    subject_1_grade = fields.Char("Subject 1 Grade") 
    Subject_1_Grade_Written_AR = fields.Char("Subject 1 Grade Written AR") 
    Subject_1_Grade_Written_EN = fields.Char("Subject 1 Grade Written EN")
    Subject_1_Semester  = fields.Char("Subject 1 Semester")

    subject_2_arabic = fields.Char("Subject 2 Arabic")
    subject_2_english = fields.Char("Subject 2 English")
    subject_2_units = fields.Char("Subject 2 Units")
    subject_2_grade = fields.Char("Subject 2 Grade") 
    Subject_2_Grade_Written_AR = fields.Char("Subject 2 Grade Written AR") 
    Subject_2_Grade_Written_EN = fields.Char("Subject 2 Grade Written EN")
    Subject_2_Semester  = fields.Char("Subject 2 Semester")

    subject_3_arabic = fields.Char("Subject 3 Arabic")
    subject_3_english = fields.Char("Subject 3 English")
    subject_3_units = fields.Char("Subject 3 Units")
    subject_3_grade = fields.Char("Subject 3 Grade") 
    Subject_3_Grade_Written_AR = fields.Char("Subject 3 Grade Written AR") 
    Subject_3_Grade_Written_EN = fields.Char("Subject 3 Grade Written EN")
    Subject_3_Semester  = fields.Char("Subject 3 Semester")

    subject_4_arabic = fields.Char("Subject 4 Arabic")
    subject_4_english = fields.Char("Subject 4 English")
    subject_4_units = fields.Char("Subject 4 Units")
    subject_4_grade = fields.Char("Subject 4 Grade") 
    Subject_4_Grade_Written_AR = fields.Char("Subject 4 Grade Written AR") 
    Subject_4_Grade_Written_EN = fields.Char("Subject 4 Grade Written EN")
    Subject_4_Semester  = fields.Char("Subject 4 Semester")

    subject_5_arabic = fields.Char("Subject 5 Arabic")
    subject_5_english = fields.Char("Subject 5 English")
    subject_5_units = fields.Char("Subject 5 Units")
    subject_5_grade = fields.Char("Subject 5 Grade") 
    Subject_5_Grade_Written_AR = fields.Char("Subject 5 Grade Written AR") 
    Subject_5_Grade_Written_EN = fields.Char("Subject 5 Grade Written EN")
    Subject_5_Semester  = fields.Char("Subject 5 Semester")

    subject_6_arabic = fields.Char("Subject 6 Arabic")
    subject_6_english = fields.Char("Subject 6 English")
    subject_6_units = fields.Char("Subject 6 Units")
    subject_6_grade = fields.Char("Subject 6 Grade") 
    Subject_6_Grade_Written_AR = fields.Char("Subject 6 Grade Written AR") 
    Subject_6_Grade_Written_EN = fields.Char("Subject 6 Grade Written EN")
    Subject_6_Semester  = fields.Char("Subject 6 Semester")

    subject_7_arabic = fields.Char("Subject 7 Arabic")
    subject_7_english = fields.Char("Subject 7 English")
    subject_7_units = fields.Char("Subject 7 Units")
    subject_7_grade = fields.Char("Subject 7 Grade") 
    Subject_7_Grade_Written_AR = fields.Char("Subject 7 Grade Written AR") 
    Subject_7_Grade_Written_EN = fields.Char("Subject 7 Grade Written EN")
    Subject_7_Semester  = fields.Char("Subject 7 Semester")

    subject_8_arabic = fields.Char("Subject 8 Arabic")
    subject_8_english = fields.Char("Subject 8 English")
    subject_8_units = fields.Char("Subject 8 Units")
    subject_8_grade = fields.Char("Subject 8 Grade") 
    Subject_8_Grade_Written_AR = fields.Char("Subject 8 Grade Written AR") 
    Subject_8_Grade_Written_EN = fields.Char("Subject 8 Grade Written EN")
    Subject_8_Semester  = fields.Char("Subject 8 Semester")

    subject_9_arabic = fields.Char("Subject 9 Arabic")
    subject_9_english = fields.Char("Subject 9 English")
    subject_9_units = fields.Char("Subject 9 Units")
    subject_9_grade = fields.Char("Subject 9 Grade") 
    Subject_9_Grade_Written_AR = fields.Char("Subject 9 Grade Written AR") 
    Subject_9_Grade_Written_EN = fields.Char("Subject 9 Grade Written EN")
    Subject_9_Semester  = fields.Char("Subject 9 Semester")

    subject_10_arabic = fields.Char("Subject 10 Arabic")
    subject_10_english = fields.Char("Subject 10 English")
    subject_10_units = fields.Char("Subject 10 Units")
    subject_10_grade = fields.Char("Subject 10 Grade")
    Subject_10_Grade_Written_AR = fields.Char("Subject 10 Grade Written AR") 
    Subject_10_Grade_Written_EN = fields.Char("Subject 10 Grade Written EN")
    Subject_10_Semester  = fields.Char("Subject 10 Semester") 

    subject_11_arabic = fields.Char("Subject 11 Arabic")
    subject_11_english = fields.Char("Subject 11 English")
    subject_11_units = fields.Char("Subject 11 Units")
    subject_11_grade = fields.Char("Subject 11 Grade") 
    Subject_11_Grade_Written_AR = fields.Char("Subject 11 Grade Written AR") 
    Subject_11_Grade_Written_EN = fields.Char("Subject 11 Grade Written EN")
    Subject_11_Semester  = fields.Char("Subject 11 Semester")

    subject_12_arabic = fields.Char("Subject 12 Arabic")
    subject_12_english = fields.Char("Subject 12 English")
    subject_12_units = fields.Char("Subject 12 Units")
    subject_12_grade = fields.Char("Subject 12 Grade") 
    Subject_12_Grade_Written_AR = fields.Char("Subject 12 Grade Written AR") 
    Subject_12_Grade_Written_EN = fields.Char("Subject 12 Grade Written EN")
    Subject_12_Semester  = fields.Char("Subject 12 Semester")

    subject_13_arabic = fields.Char("Subject 13 Arabic")
    subject_13_english = fields.Char("Subject 13 English")
    subject_13_units = fields.Char("Subject 13 Units")
    subject_13_grade = fields.Char("Subject 13 Grade") 
    Subject_13_Grade_Written_AR = fields.Char("Subject 13 Grade Written AR") 
    Subject_13_Grade_Written_EN = fields.Char("Subject 13 Grade Written EN")
    Subject_13_Semester  = fields.Char("Subject 13 Semester")

    subject_14_arabic = fields.Char("Subject 14 Arabic")
    subject_14_english = fields.Char("Subject 14 English")
    subject_14_units = fields.Char("Subject 14 Units")
    subject_14_grade = fields.Char("Subject 14 Grade") 
    Subject_14_Grade_Written_AR = fields.Char("Subject 14 Grade Written AR") 
    Subject_14_Grade_Written_EN = fields.Char("Subject 14 Grade Written EN")
    Subject_14_Semester  = fields.Char("Subject 14 Semester")

    subject_15_arabic = fields.Char("Subject 15 Arabic")
    subject_15_english = fields.Char("Subject 15 English")
    subject_15_units = fields.Char("Subject 15 Units")
    subject_15_grade = fields.Char("Subject 15 Grade") 
    Subject_15_Grade_Written_AR = fields.Char("Subject 15 Grade Written AR") 
    Subject_15_Grade_Written_EN = fields.Char("Subject 15 Grade Written EN")
    Subject_15_Semester  = fields.Char("Subject 15 Semester")

    posted_date = fields.Date("Posted Date")
    average_word_word = fields.Char("average_word_word")


    @api.model
    def create(self, vals):
        if 'average' in vals:
            if float(vals['average']) < 50:
                vals['average_word_word'] = 'راسب'
            

            if float(vals['average']) < 60 and float(vals['average']) > 49.99:
                vals['average_word_word'] = 'مقبول'
            

            if float(vals['average']) < 70 and float(vals['average']) > 59.99:
                vals['average_word_word'] = 'متوسط'
            

            if float(vals['average']) < 80 and float(vals['average']) > 69.99:
                vals['average_word_word'] = 'جيد'
            
            if float(vals['average']) < 90 and float(vals['average']) > 79.99:
                vals['average_word_word'] = 'جيد جدا'
            
            if float(vals['average']) < 100 and float(vals['average']) > 89.99:
                vals['average_word_word'] = 'ممتاز'
        return super(AlmaaqalGrade, self).create(vals)    

    def write(self, vals):
        print("vals@@@@@@@@@@@@@@@@",vals)
        if 'average' in vals:
            if float(vals['average']) < 50:
                vals['average_word_word'] = 'راسب'
            

            if float(vals['average']) < 60 and float(vals['average']) > 49.99:
                vals['average_word_word'] = 'مقبول'
            

            if float(vals['average']) < 70 and float(vals['average']) > 59.99:
                vals['average_word_word'] = 'متوسط'
            

            if float(vals['average']) < 80 and float(vals['average']) > 69.99:
                vals['average_word_word'] = 'جيد'
            
            if float(vals['average']) < 90 and float(vals['average']) > 79.99:
                vals['average_word_word'] = 'جيد جدا'
            
            if float(vals['average']) < 100 and float(vals['average']) > 89.99:
                vals['average_word_word'] = 'ممتاز'
        return super(AlmaaqalGrade, self).write(vals)

    @api.onchange('average')
    def _onchange_average_word(self):
        if float(self.average) < 50:
            self.average_word_word = 'راسب'
        

        if float(self.average) < 60 and float(self.average) > 49.99:
            self.average_word_word = 'مقبول'
        

        if float(self.average) < 70 and float(self.average) > 59.99:
            self.average_word_word = 'متوسط'
        

        if float(self.average) < 80 and float(self.average) > 69.99:
            self.average_word_word = 'جيد'
        
        if float(self.average) < 90 and float(self.average) > 79.99:
            self.average_word_word = 'جيد جدا'
        
        if float(self.average) < 100 and float(self.average) > 89.99:
            self.average_word_word = 'ممتاز'
                    

    # @api.onchange('Status')
    def buuton_status_change(self):
        self.Status = 'posted'
        self.posted_date = date.today()

    def buuton_status_change_draft(self):
        self.Status = 'draft'
        self.posted_date = False

    def remove_underscores(self, text):
        """Remove underscores from the given text."""
        return text.replace('_', '')    

    def print_pdf(self):
        for ddt in self:
            return {'type': 'ir.actions.act_url',
                'url': '/web/binary/download_docx_report/%s' % ddt.id,
                'target': 'self',
                'res_id': ddt.id,
                }    
        
    
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
