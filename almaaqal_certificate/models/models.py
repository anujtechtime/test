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

    Status = fields.Selection([('draft','Draft'),('posted','Posted'),('final_approved','Final Approved')], string="Status", default="draft")
    
    tags = fields.Char("Tags")

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




    study_year_name_ar = fields.Char("Study Year Name AR")  
    study_year_name_en = fields.Char("Study Year Name EN")

    Graduate_Sequence = fields.Char("Graduate Sequence")
    The_average_of_the_first_student_in_the_class = fields.Char("The average of the first student in the class")
    Total_number_of_graduates  = fields.Char("Total number of graduates ")

    subject = fields.Many2many("certificate.subject", string="Subject")  


    # subject = fields.Many2many("subject.subject")  


    

    posted_date = fields.Date("Posted Date")
    average_word_word = fields.Char("average_word_word")
