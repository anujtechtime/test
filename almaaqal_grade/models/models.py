# -*- coding: utf-8 -*-

from odoo import models, fields, api, _ 
from datetime import date
import base64
import logging

_logger = logging.getLogger(__name__)

class AlmaaqalGrade(models.Model):
    _name = 'almaaqal.grade'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Almaaqal Grade'


    Status = fields.Selection([('draft','Draft'),('posted','Posted'),('final_approved','Final Approved')], string="Status", default="draft",  tracking=True)
    

    exam_number_for_reference =  fields.Char("Exam Number",  tracking=True)

    college_in_english =  fields.Char("College in EN",  tracking=True)
    college_in_arabic =  fields.Char("College in AR",  tracking=True)

    study_type_arabic = fields.Char("Study Type AR",  tracking=True)
    study_type_english = fields.Char("Study Type EN",  tracking=True)

    serial = fields.Char("Serial",  tracking=True)

    gender = fields.Char("Gender",  tracking=True)

    subject_to_arabic = fields.Char("Subject to Arabic",  tracking=True)
    subject_to_english = fields.Char("Subject to English",  tracking=True)

    certificate_name_department_AR = fields.Char("Certificate Name/Department AR",  tracking=True)
    certificate_name_department_EN = fields.Char("Certificate Name/Department EN",  tracking=True)

    University_order_number = fields.Char("University order number",  tracking=True)
    University_order_date = fields.Date("University order date",  tracking=True)

    dean_collage_name_arabic = fields.Char("Dean Collage Name AR",  tracking=True)
    dean_collage_name_english = fields.Char("Dean Collage Name EN",  tracking=True)

    department_in_english =  fields.Char("Department in EN",  tracking=True)
    department_in_arabic =  fields.Char("Department in AR",  tracking=True)


    stage_year = fields.Char("Stage Year",  tracking=True)

    year_of_graduation =  fields.Char("Year of graduation",  tracking=True) 
    
    student_name_in_english =  fields.Char("Student Name in EN",  tracking=True)
    student_name_in_arabic =  fields.Char("Student Name in AR",  tracking=True)

    nationality_ar = fields.Char("Nationality AR",  tracking=True)
    nationality_en = fields.Char("Nationality EN",  tracking=True)

    average =  fields.Char("Average",  tracking=True) 

    average_in_words_en = fields.Char("Average in Words EN",  tracking=True)
    average_in_words_ar = fields.Char("Average in Words AR",  tracking=True)


    attempt_en = fields.Char("Attempt EN",  tracking=True)  
    attempt_ar = fields.Char("Attempt AR",  tracking=True)



    

    study_year_name_ar = fields.Char("Study Year Name AR",  tracking=True)  
    study_year_name_en = fields.Char("Study Year Name EN",  tracking=True)

    Graduate_Sequence = fields.Char("Graduate Sequence",  tracking=True)
    The_average_of_the_first_student_in_the_class = fields.Char("The average of the first student in the class",  tracking=True)
    Total_number_of_graduates  = fields.Char("Total number of graduates ",  tracking=True)

    subject = fields.One2many(comodel_name="subject.subject",inverse_name="grade_id", string="Subject",  tracking=True)  

    # subject = fields.Many2many("subject.subject")  
    average_word_word_en = fields.Char("Average English")

    old_average = fields.Char("Old average")

    posted_date = fields.Date("Posted Date",  tracking=True)
    average_word_word = fields.Char("average_word_word",  tracking=True)
    remark = fields.Many2many("grade.remark", string="Remark", tracking=True)

    def has_three_decimal_places(self, number):
        str_num = str(number)
        parts = str_num.split(".")
        return len(parts) == 2 and len(parts[1]) >= 4

    def truncate_to_three_decimals(self, number):
        str_num = str(number)
        if '.' in str_num:
            integer_part, decimal_part = str_num.split('.')
            truncated_decimal_part = decimal_part[:3]
            truncated_number = f"{integer_part}.{truncated_decimal_part}"
            return float(truncated_number)
        else:
            return float(str_num)
    @api.model
    def create(self, vals):
        if 'average' in vals:
            if float(vals['average']) < 50:
                vals['average_word_word'] = 'راسب'
                vals['average_word_word_en'] = 'Failed'

            if float(vals['average']) < 60 and float(vals['average']) > 49.99:
                vals['average_word_word'] = 'مقبول'
                vals['average_word_word_en'] = 'Acceptable'

            if float(vals['average']) < 70 and float(vals['average']) > 59.99:
                vals['average_word_word'] = 'متوسط'
                vals['average_word_word_en'] =  'Average'

            if float(vals['average']) < 80 and float(vals['average']) > 69.99:
                vals['average_word_word'] = 'جيد'
                vals['average_word_word_en'] = 'Good'
            
            if float(vals['average']) < 90 and float(vals['average']) > 79.99:
                vals['average_word_word'] = 'جيد جدا'
                vals['average_word_word_en'] = 'Very Good'
            
            if float(vals['average']) < 100 and float(vals['average']) > 89.99:
                vals['average_word_word'] = 'أمتياز'
                vals['average_word_word_en'] = 'Excellent'


                
        res =  super(AlmaaqalGrade, self).create(vals)
        threedecimal = res.has_three_decimal_places(float(res.average)) 
        if threedecimal:
            res.old_average = res.average
            res.average = res.truncate_to_three_decimals(res.average)
        return res        

    def write(self, vals):
        print("vals@@@@@@@@@@@@@@@@",vals)

        if 'average' in vals:
            if float(vals['average']) < 50:
                vals['average_word_word'] = 'راسب'
                vals['average_word_word_en'] = 'Failed'

            if float(vals['average']) < 60 and float(vals['average']) > 49.99:
                vals['average_word_word'] = 'مقبول'
                vals['average_word_word_en'] = 'Acceptable'

            if float(vals['average']) < 70 and float(vals['average']) > 59.99:
                vals['average_word_word'] = 'متوسط'
                vals['average_word_word_en'] =  'Average'

            if float(vals['average']) < 80 and float(vals['average']) > 69.99:
                vals['average_word_word'] = 'جيد'
                vals['average_word_word_en'] = 'Good'
            
            if float(vals['average']) < 90 and float(vals['average']) > 79.99:
                vals['average_word_word'] = 'جيد جدا'
                vals['average_word_word_en'] = 'Very Good'
            
            if float(vals['average']) < 100 and float(vals['average']) > 89.99:
                vals['average_word_word'] = 'أمتياز'
                vals['average_word_word_en'] = 'Excellent'
            res =  super(AlmaaqalGrade, self).write(vals)
            threedecimal = self.has_three_decimal_places(float(self.average)) 
            if threedecimal:
                self.old_average = self.average
                self.average = self.truncate_to_three_decimals(self.average)
            return res
        return super(AlmaaqalGrade, self).write(vals)



    # def rounding_float(self):
    #     threedecimal = self.has_three_decimal_places(self.average) 
    #     if threedecimal:
    #         self.average = self.truncate_to_three_decimals(self.average)

    @api.onchange('average')
    def _onchange_average_word(self):
        threedecimal = ""
        if float(self.average) < 50:
            self.average_word_word = 'راسب'
            self.average_word_word_en = 'Failed'
        

        if float(self.average) < 60 and float(self.average) > 49.99:
            self.average_word_word = 'مقبول'
            self.average_word_word_en = 'Acceptable'
        

        if float(self.average) < 70 and float(self.average) > 59.99:
            self.average_word_word = 'متوسط'
            self.average_word_word_en =  'Average'
        

        if float(self.average) < 80 and float(self.average) > 69.99:
            self.average_word_word = 'جيد'
            self.average_word_word_en = 'Good'

        
        if float(self.average) < 90 and float(self.average) > 79.99:
            self.average_word_word = 'جيد جدا'
            self.average_word_word_en = 'Very Good'
        
        if float(self.average) < 100 and float(self.average) > 89.99:
            self.average_word_word = 'أمتياز'
            self.average_word_word_en = 'Excellent'  

        threedecimal = self.has_three_decimal_places(float(self.average)) 
        if threedecimal:
            self.old_average = self.average
            self.average = self.truncate_to_three_decimals(self.average)

    def change_englishh_average(self):
        for dst in self:
            if float(dst.average) < 50:
                dst.average_word_word = 'راسب'
                dst.average_word_word_en = 'Failed'
            

            if float(dst.average) < 60 and float(dst.average) > 49.99:
                dst.average_word_word = 'مقبول'
                dst.average_word_word_en = 'Acceptable'
            

            if float(dst.average) < 70 and float(dst.average) > 59.99:
                dst.average_word_word = 'متوسط'
                dst.average_word_word_en =  'Average'
            

            if float(dst.average) < 80 and float(dst.average) > 69.99:
                dst.average_word_word = 'جيد'
                dst.average_word_word_en = 'Good'

            
            if float(dst.average) < 90 and float(dst.average) > 79.99:
                dst.average_word_word = 'جيد جدا'
                dst.average_word_word_en = 'Very Good'
            
            if float(dst.average) < 100 and float(dst.average) > 89.99:
                dst.average_word_word = 'أمتياز'
                dst.average_word_word_en = 'Excellent' 
            threedecimal = ""    
            threedecimal = dst.has_three_decimal_places(float(dst.average)) 
            if threedecimal:
                dst.old_average = dst.average
                dst.average = dst.truncate_to_three_decimals(dst.average)                                

    # @api.onchange('Status')
    def buuton_status_change(self):
        self.Status = 'posted'
        if not self.posted_date:
            self.posted_date = date.today()

    def buuton_status_change_draft(self):
        self.Status = 'draft'
        self.posted_date = False

    def buuton_status_change_final_approved(self):
        self.Status = 'final_approved'

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
        
    
    # def print_arabic_no_grade_pdf(self):
    #     # Generate PDF report
    #     report = self.env.ref('almaaqal_certificate.action_report_almaaqal_certificate')
    #     print("self@@@@@@@@@@@@@",self.ids)

        

    #     serial = self.env['ir.sequence'].next_by_code('arabic.nograde')
    #     tag = "Arabic No Grade"
            
    #     self.create_almaaqal_certificate(serial, tag)
        


    #     serial_main = self.env['ir.sequence'].next_by_code('arabic.nogradeserial')
    #     self.serial = serial_main

    #     remard_id = self.remark.create({
    #         "attachment_filename" : "Arabic No Grade.pdf",
    #         "user_id" : self.env.user.id,
    #         "serial" : serial,
    #         'subject_to_arabic' : self.subject_to_arabic,
    #         'subject_to_english' : self.subject_to_english,
    #         'serial_main' : serial_main,
    #         'posted_date' : self.posted_date
    #         })
    #     self.remark = [(4, remard_id.id)]


    #     pdf_content, _ = report.render_qweb_pdf(res_ids=self.ids)

    #     # Convert PDF to base64
    #     pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
    #     remard_id.update({
    #         "attachment_file" : pdf_base64,
    #         })

    #     # Create attachment
    #     attachment = self.env['ir.attachment'].create({
    #         'name': 'Report.pdf',
    #         'type': 'binary',
    #         'datas': pdf_base64,
    #         'res_model': self._name,
    #         'res_id': self.id,
    #         'mimetype': 'application/pdf'
    #     })

    #     self.message_post(
    #         body="Arabic No Grade (PDF),",
    #         attachment_ids=[attachment.id]
    #     )

    #     return self.env.ref('almaaqal_certificate.action_report_almaaqal_certificate').report_action(self)



    # def print_arabic_with_grade(self):
    #     # Generate PDF report
    #     report = self.env.ref('almaaqal_certificate.action_report_almaaqal_certificate_with_grade')
    #     print("self@@@@@@@@@@@@@",self.ids)

    #     pdf_content, _ = report.render_qweb_pdf(res_ids=self.ids)

    #     # Convert PDF to base64
    #     pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

    #     # Create attachment
    #     attachment = self.env['ir.attachment'].create({
    #         'name': 'Report.pdf',
    #         'type': 'binary',
    #         'datas': pdf_base64,
    #         'res_model': self._name,
    #         'res_id': self.id,
    #         'mimetype': 'application/pdf'
    #     })

    #     self.message_post(
    #         body="Arabic With Grade (PDF),",
    #         attachment_ids=[attachment.id]
    #     )

    #     serial = self.env['ir.sequence'].next_by_code('arabic.withgrade')
    #     tag = "Arabic With Grade"
            
    #     self.create_almaaqal_certificate(serial, tag)

    #     remard_id = self.remark.create({
    #         "attachment_filename" : "Arabic With Grade.pdf",
    #         "attachment_file" : pdf_base64,
    #         "user_id" : self.env.user.id,
    #         'serial' : serial,
    #         'subject_to_arabic' : self.subject_to_arabic,
    #         'subject_to_english' : self.subject_to_english,
    #         })
    #     self.remark = [(4, remard_id.id)]

    #     return self.env.ref('almaaqal_certificate.action_report_almaaqal_certificate_with_grade').report_action(self)    

    # def print_english_no_grade(self):
    #     # Generate PDF report
    #     report = self.env.ref('almaaqal_certificate.action_report_almaaqal_certificate_english')
    #     print("self@@@@@@@@@@@@@",self.ids)

    #     pdf_content, _ = report.render_qweb_pdf(res_ids=self.ids)

    #     # Convert PDF to base64
    #     pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

    #     # Create attachment
    #     attachment = self.env['ir.attachment'].create({
    #         'name': 'Report.pdf',
    #         'type': 'binary',
    #         'datas': pdf_base64,
    #         'res_model': self._name,
    #         'res_id': self.id,
    #         'mimetype': 'application/pdf'
    #     })

    #     serial = self.env['ir.sequence'].next_by_code('english.nograde')
    #     tag = "English No Grade"
            
    #     self.create_almaaqal_certificate(serial, tag)
        
    #     remard_id = self.remark.create({
    #         "attachment_filename" : "English No Grade.pdf",
    #         "attachment_file" : pdf_base64,
    #         "user_id" : self.env.user.id,
    #         "serial" : serial,
    #         'subject_to_arabic' : self.subject_to_arabic,
    #         'subject_to_english' : self.subject_to_english,
    #         })
    #     self.remark = [(4, remard_id.id)]
    #     self.message_post(
    #         body="English No Grade (PDF),",
    #         attachment_ids=[attachment.id]
    #     )

    #     return self.env.ref('almaaqal_certificate.action_report_almaaqal_certificate_english').report_action(self)
        



    # def print_english_with_grade(self):
    #     # Generate PDF report
    #     report = self.env.ref('almaaqal_certificate.action_report_almaaqal_certificate_with_grade_english')

    #     pdf_content, _ = report.render_qweb_pdf(res_ids=self.ids)

    #     # Convert PDF to base64
    #     pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

    #     # Create attachment
    #     attachment = self.env['ir.attachment'].create({
    #         'name': 'Report.pdf',
    #         'type': 'binary',
    #         'datas': pdf_base64,
    #         'res_model': self._name,
    #         'res_id': self.id,
    #         'mimetype': 'application/pdf'
    #     })

    #     self.message_post(
    #         body="English With Grade (PDF),",
    #         attachment_ids=[attachment.id]
    #     )

    #     serial = self.env['ir.sequence'].next_by_code('english.withgrade')
    #     tag = "English With Grade"
            
    #     self.create_almaaqal_certificate(serial, tag)

    #     remard_id = self.remark.create({
    #         "attachment_filename" : "English With Grade.pdf",
    #         "attachment_file" : pdf_base64,
    #         "user_id" : self.env.user.id,
    #         'serial' : serial,
    #         'subject_to_arabic' : self.subject_to_arabic,
    #         'subject_to_english' : self.subject_to_english,
    #         })
    #     self.remark = [(4, remard_id.id)]

    #     return self.env.ref('almaaqal_certificate.action_report_almaaqal_certificate_with_grade_english').report_action(self)   

    def create_almaaqal_certificate(self, serial, tag):
        certi = self.env["almaaqal.certificate"].create({
            'Status' : self.Status,
            'exam_number_for_reference' : self.exam_number_for_reference,
            'tags' : tag,
            'college_in_english' : self.college_in_english,
            'college_in_arabic' : self.college_in_arabic,
            'study_type_arabic' : self.study_type_arabic,
            'study_type_english' : self.study_type_english,
            'serial' : serial,
            'gender' : self.gender,
            'subject_to_arabic' : self.subject_to_arabic,
            'subject_to_english' : self.subject_to_english,
            'certificate_name_department_AR' : self.certificate_name_department_AR,
            'certificate_name_department_EN' : self.certificate_name_department_EN,
            'University_order_number' : self.University_order_number,
            'University_order_date' : self.University_order_date,
            'dean_collage_name_arabic' : self.dean_collage_name_arabic,
            'dean_collage_name_english' : self.dean_collage_name_english,
            'department_in_english' : self.department_in_english,
            'department_in_arabic' : self.department_in_arabic,
            'stage_year' : self.stage_year,
            'year_of_graduation' : self.year_of_graduation,
            'student_name_in_english' : self.student_name_in_english,
            'student_name_in_arabic' : self.student_name_in_arabic,
            'nationality_ar' : self.nationality_ar,
            'nationality_en' : self.nationality_en,
            'average' : self.average,
            'average_in_words_en' : self.average_in_words_en,
            'average_in_words_ar' : self.average_in_words_ar,
            'attempt_en' : self.attempt_en,
            'attempt_ar' : self.attempt_ar,
            'study_year_name_ar' : self.study_year_name_ar,
            'study_year_name_en' : self.study_year_name_en,
            'Graduate_Sequence' : self.Graduate_Sequence,
            'The_average_of_the_first_student_in_the_class' : self.The_average_of_the_first_student_in_the_class,
            'Total_number_of_graduates' : self.Total_number_of_graduates,
            })    
        subject_ids = []
        if self.subject:
            for sub in self.subject:
                subj = self.env['certificate.subject'].create({
                    'exam_number_link' : sub.exam_number_link,
                    'stage_year' : sub.stage_year,
                    'stage' : sub.stage,
                    'study_notes_in_arabic' : sub.study_notes_in_arabic, 
                    'study_notes_in_english' : sub.study_notes_in_english, 


                    'subject_1_arabic' : sub.subject_1_arabic,
                    'subject_1_english' : sub.subject_1_english,
                    'subject_1_units' : sub.subject_1_units,
                    'subject_1_grade' : sub.subject_1_grade, 
                    'Subject_1_Grade_Written_AR' : sub.Subject_1_Grade_Written_AR, 
                    'Subject_1_Grade_Written_EN' : sub.Subject_1_Grade_Written_EN,
                    'Subject_1_Semester' : sub.Subject_1_Semester,

                    'subject_2_arabic' : sub.subject_2_arabic,
                    'subject_2_english' : sub.subject_2_english,
                    'subject_2_units' : sub.subject_2_units,
                    'subject_2_grade' : sub.subject_2_grade, 
                    'Subject_2_Grade_Written_AR' : sub.Subject_2_Grade_Written_AR, 
                    'Subject_2_Grade_Written_EN' : sub.Subject_2_Grade_Written_EN,
                    'Subject_2_Semester' : sub.Subject_2_Semester,

                    'subject_3_arabic' : sub.subject_3_arabic,
                    'subject_3_english' : sub.subject_3_english,
                    'subject_3_units' : sub.subject_3_units,
                    'subject_3_grade' : sub.subject_3_grade, 
                    'Subject_3_Grade_Written_AR' : sub.Subject_3_Grade_Written_AR, 
                    'Subject_3_Grade_Written_EN' : sub.Subject_3_Grade_Written_EN,
                    'Subject_3_Semester' : sub.Subject_3_Semester,

                    'subject_4_arabic' : sub.subject_4_arabic,
                    'subject_4_english' : sub.subject_4_english,
                    'subject_4_units' : sub.subject_4_units,
                    'subject_4_grade' : sub.subject_4_grade, 
                    'Subject_4_Grade_Written_AR' : sub.Subject_4_Grade_Written_AR, 
                    'Subject_4_Grade_Written_EN' : sub.Subject_4_Grade_Written_EN,
                    'Subject_4_Semester' : sub.Subject_4_Semester,

                    'subject_5_arabic' : sub.subject_5_arabic,
                    'subject_5_english' : sub.subject_5_english,
                    'subject_5_units' : sub.subject_5_units,
                    'subject_5_grade' : sub.subject_5_grade, 
                    'Subject_5_Grade_Written_AR' : sub.Subject_5_Grade_Written_AR, 
                    'Subject_5_Grade_Written_EN' : sub.Subject_5_Grade_Written_EN,
                    'Subject_5_Semester' : sub.Subject_5_Semester,

                    'subject_6_arabic' : sub.subject_6_arabic,
                    'subject_6_english' : sub.subject_6_english,
                    'subject_6_units' : sub.subject_6_units,
                    'subject_6_grade' : sub.subject_6_grade, 
                    'Subject_6_Grade_Written_AR' : sub.Subject_6_Grade_Written_AR, 
                    'Subject_6_Grade_Written_EN' : sub.Subject_6_Grade_Written_EN,
                    'Subject_6_Semester' : sub.Subject_6_Semester,

                    'subject_7_arabic' : sub.subject_7_arabic,
                    'subject_7_english' : sub.subject_7_english,
                    'subject_7_units' : sub.subject_7_units,
                    'subject_7_grade' : sub.subject_7_grade, 
                    'Subject_7_Grade_Written_AR' : sub.Subject_7_Grade_Written_AR, 
                    'Subject_7_Grade_Written_EN' : sub.Subject_7_Grade_Written_EN,
                    'Subject_7_Semester' : sub.Subject_7_Semester,

                    'subject_8_arabic' : sub.subject_8_arabic,
                    'subject_8_english' : sub.subject_8_english,
                    'subject_8_units' : sub.subject_8_units,
                    'subject_8_grade' : sub.subject_8_grade, 
                    'Subject_8_Grade_Written_AR' : sub.Subject_8_Grade_Written_AR, 
                    'Subject_8_Grade_Written_EN' : sub.Subject_8_Grade_Written_EN,
                    'Subject_8_Semester' : sub.Subject_8_Semester,

                    'subject_9_arabic' : sub.subject_9_arabic,
                    'subject_9_english' : sub.subject_9_english,
                    'subject_9_units' : sub.subject_9_units,
                    'subject_9_grade' : sub.subject_9_grade, 
                    'Subject_9_Grade_Written_AR' : sub.Subject_9_Grade_Written_AR,
                    'Subject_9_Grade_Written_EN' : sub.Subject_9_Grade_Written_EN,
                    'Subject_9_Semester' : sub.Subject_9_Semester,

                    'subject_10_arabic' : sub.subject_10_arabic,
                    'subject_10_english' : sub.subject_10_english,
                    'subject_10_units' : sub.subject_10_units,
                    'subject_10_grade' : sub.subject_10_grade,
                    'Subject_10_Grade_Written_AR' : sub.Subject_10_Grade_Written_AR,
                    'Subject_10_Grade_Written_EN' : sub.Subject_10_Grade_Written_EN,
                    'Subject_10_Semester' : sub.Subject_10_Semester,

                    'subject_11_arabic' : sub.subject_11_arabic,
                    'subject_11_english' : sub.subject_11_english,
                    'subject_11_units' : sub.subject_11_units,
                    'subject_11_grade' : sub.subject_11_grade,
                    'Subject_11_Grade_Written_AR' : sub.Subject_11_Grade_Written_AR,
                    'Subject_11_Grade_Written_EN' : sub.Subject_11_Grade_Written_EN,
                    'Subject_11_Semester' : sub.Subject_11_Semester,

                    'subject_12_arabic' : sub.subject_12_arabic,
                    'subject_12_english' : sub.subject_12_english,
                    'subject_12_units' : sub.subject_12_units,
                    'subject_12_grade' : sub.subject_12_grade,
                    'Subject_12_Grade_Written_AR' : sub.Subject_12_Grade_Written_AR,
                    'Subject_12_Grade_Written_EN' : sub.Subject_12_Grade_Written_EN,
                    'Subject_12_Semester' : sub.Subject_12_Semester,

                    'subject_13_arabic' : sub.subject_13_arabic,
                    'subject_13_english' : sub.subject_13_english,
                    'subject_13_units' : sub.subject_13_units,
                    'subject_13_grade' : sub.subject_13_grade,
                    'Subject_13_Grade_Written_AR' : sub.Subject_13_Grade_Written_AR,
                    'Subject_13_Grade_Written_EN' : sub.Subject_13_Grade_Written_EN,
                    'Subject_13_Semester' : sub.Subject_13_Semester,

                    'subject_14_arabic' : sub.subject_14_arabic,
                    'subject_14_english' : sub.subject_14_english,
                    'subject_14_units' : sub.subject_14_units,
                    'subject_14_grade' : sub.subject_14_grade,
                    'Subject_14_Grade_Written_AR' : sub.Subject_14_Grade_Written_AR,
                    'Subject_14_Grade_Written_EN' : sub.Subject_14_Grade_Written_EN,
                    'Subject_14_Semester' : sub.Subject_14_Semester,

                    'subject_15_arabic' : sub.subject_15_arabic,
                    'subject_15_english' : sub.subject_15_english,
                    'subject_15_units' : sub.subject_15_units,
                    'subject_15_grade' : sub.subject_15_grade,
                    'Subject_15_Grade_Written_AR' : sub.Subject_15_Grade_Written_AR,
                    'Subject_15_Grade_Written_EN' : sub.Subject_15_Grade_Written_EN,
                    'Subject_15_Semester' : sub.Subject_15_Semester,

                    'subject_16_arabic' : sub.subject_16_arabic,
                    'subject_16_english' : sub.subject_16_english,
                    'subject_16_units' : sub.subject_16_units,
                    'subject_16_grade' : sub.subject_16_grade,
                    'Subject_16_Grade_Written_AR' : sub.Subject_16_Grade_Written_AR,
                    'Subject_16_Grade_Written_EN' : sub.Subject_16_Grade_Written_EN,
                    'Subject_16_Semester' : sub.Subject_16_Semester,

                    'subject_17_arabic' : sub.subject_17_arabic,
                    'subject_17_english' : sub.subject_17_english,
                    'subject_17_units' : sub.subject_17_units,
                    'subject_17_grade' : sub.subject_17_grade,
                    'Subject_17_Grade_Written_AR' : sub.Subject_17_Grade_Written_AR,
                    'Subject_17_Grade_Written_EN' : sub.Subject_17_Grade_Written_EN,
                    'Subject_17_Semester' : sub.Subject_17_Semester,

                    'subject_18_arabic' : sub.subject_18_arabic,
                    'subject_18_english' : sub.subject_18_english,
                    'subject_18_units' : sub.subject_18_units,
                    'subject_18_grade' : sub.subject_18_grade,
                    'Subject_18_Grade_Written_AR' : sub.Subject_18_Grade_Written_AR,
                    'Subject_18_Grade_Written_EN' : sub.Subject_18_Grade_Written_EN,
                    'Subject_18_Semester' : sub.Subject_18_Semester,

                    'subject_19_arabic' : sub.subject_19_arabic,
                    'subject_19_english' : sub.subject_19_english,
                    'subject_19_units' : sub.subject_19_units,
                    'subject_19_grade' : sub.subject_19_grade,
                    'Subject_19_Grade_Written_AR' : sub.Subject_19_Grade_Written_AR,
                    'Subject_19_Grade_Written_EN' : sub.Subject_19_Grade_Written_EN,
                    'Subject_19_Semester' : sub.Subject_19_Semester,

                    'subject_20_arabic' : sub.subject_20_arabic,
                    'subject_20_english' : sub.subject_20_english,
                    'subject_20_units' : sub.subject_20_units,
                    'subject_20_grade' : sub.subject_20_grade,
                    'Subject_20_Grade_Written_AR' : sub.Subject_20_Grade_Written_AR,
                    'Subject_20_Grade_Written_EN' : sub.Subject_20_Grade_Written_EN,
                    'Subject_20_Semester' : sub.Subject_20_Semester,

                    'subject_21_arabic' : sub.subject_21_arabic,
                    'subject_21_english' : sub.subject_21_english,
                    'subject_21_units' : sub.subject_21_units,
                    'subject_21_grade' : sub.subject_21_grade,
                    'Subject_21_Grade_Written_AR' : sub.Subject_21_Grade_Written_AR,
                    'Subject_21_Grade_Written_EN' : sub.Subject_21_Grade_Written_EN,
                    'Subject_21_Semester' : sub.Subject_21_Semester,

                    'subject_22_arabic' : sub.subject_22_arabic,
                    'subject_22_english' : sub.subject_22_english,
                    'subject_22_units' : sub.subject_22_units,
                    'subject_22_grade' : sub.subject_22_grade,
                    'Subject_22_Grade_Written_AR' : sub.Subject_22_Grade_Written_AR,
                    'Subject_22_Grade_Written_EN' : sub.Subject_22_Grade_Written_EN,
                    'Subject_22_Semester' : sub.Subject_22_Semester,

                    'subject_23_arabic' : sub.subject_23_arabic,
                    'subject_23_english' : sub.subject_23_english,
                    'subject_23_units' : sub.subject_23_units,
                    'subject_23_grade' : sub.subject_23_grade,
                    'Subject_23_Grade_Written_AR' : sub.Subject_23_Grade_Written_AR,
                    'Subject_23_Grade_Written_EN' : sub.Subject_23_Grade_Written_EN,
                    'Subject_23_Semester' : sub.Subject_23_Semester,

                    'subject_24_arabic' : sub.subject_24_arabic,
                    'subject_24_english' : sub.subject_24_english,
                    'subject_24_units' : sub.subject_24_units,
                    'subject_24_grade' : sub.subject_24_grade,
                    'Subject_24_Grade_Written_AR' : sub.Subject_24_Grade_Written_AR,
                    'Subject_24_Grade_Written_EN' : sub.Subject_24_Grade_Written_EN,
                    'Subject_24_Semester' : sub.Subject_24_Semester,


                    'subject_25_arabic' : sub.subject_25_arabic,
                    'subject_25_english' : sub.subject_25_english,
                    'subject_25_units' : sub.subject_25_units,
                    'subject_25_grade' : sub.subject_25_grade,
                    'Subject_25_Grade_Written_AR' : sub.Subject_25_Grade_Written_AR,
                    'Subject_25_Grade_Written_EN' : sub.Subject_25_Grade_Written_EN,
                    'Subject_25_Semester' : sub.Subject_25_Semester,
                    })
                subject_ids.append(subj.id)
                _logger.info("subject_ids************111111111111117777777777777777#####**%s" %subject_ids)
                certi.subject = [(4, subj.id)]

        # for order in self.sale_ids:
        # self.sale_orders = [(4, [order.id])]



class RemarkGrade(models.Model):
    _name = "grade.remark"
    _description = "Remark"

    # attachment_ids = fields.Binary("Attachment")
    # attachment_ids = fields.Many2one('ir.attachment', string='Attachments')

    attachment_file = fields.Binary(string="Attachment File")
    attachment_filename = fields.Char(string="Filename")

    user_id = fields.Many2one("res.users", string="User")
    serial = fields.Char("Serial")
    subject_to_arabic = fields.Char("Subject to arabic")
    subject_to_english = fields.Char("Subject to english")
    serial_main = fields.Char("Serial Main")
    posted_date = fields.Date("Posted Date")





class SubjectAlm(models.Model):
    _name = "subject.subject"
    _description = "Subject"

    exam_number_link =  fields.Char("Exam Number",  tracking=True)
    stage_year = fields.Char("Year",  tracking=True)
    grade_id = fields.Many2one('almaaqal.grade', string='Grade Id',  tracking=True)
    stage = fields.Integer("Stage")


    study_notes_in_arabic =  fields.Char("notes in arabic-stage",  tracking=True)     
    study_notes_in_english =  fields.Char("Notes in english-stage",  tracking=True) 


    subject_1_arabic = fields.Char("Subject 1 Arabic",  tracking=True)
    subject_1_english = fields.Char("Subject 1 English",  tracking=True)
    subject_1_units = fields.Char("Subject 1 Units",  tracking=True)
    subject_1_grade = fields.Char("Subject 1 Grade",  tracking=True) 
    Subject_1_Grade_Written_AR = fields.Char("Subject 1 Grade Written AR",  tracking=True) 
    Subject_1_Grade_Written_EN = fields.Char("Subject 1 Grade Written EN",  tracking=True)
    Subject_1_Semester  = fields.Char("Subject 1 Semester",  tracking=True)

    subject_2_arabic = fields.Char("Subject 2 Arabic",  tracking=True)
    subject_2_english = fields.Char("Subject 2 English",  tracking=True)
    subject_2_units = fields.Char("Subject 2 Units",  tracking=True)
    subject_2_grade = fields.Char("Subject 2 Grade",  tracking=True) 
    Subject_2_Grade_Written_AR = fields.Char("Subject 2 Grade Written AR",  tracking=True) 
    Subject_2_Grade_Written_EN = fields.Char("Subject 2 Grade Written EN",  tracking=True)
    Subject_2_Semester  = fields.Char("Subject 2 Semester",  tracking=True)

    subject_3_arabic = fields.Char("Subject 3 Arabic",  tracking=True)
    subject_3_english = fields.Char("Subject 3 English",  tracking=True)
    subject_3_units = fields.Char("Subject 3 Units",  tracking=True)
    subject_3_grade = fields.Char("Subject 3 Grade",  tracking=True) 
    Subject_3_Grade_Written_AR = fields.Char("Subject 3 Grade Written AR",  tracking=True) 
    Subject_3_Grade_Written_EN = fields.Char("Subject 3 Grade Written EN",  tracking=True)
    Subject_3_Semester  = fields.Char("Subject 3 Semester",  tracking=True)

    subject_4_arabic = fields.Char("Subject 4 Arabic",  tracking=True)
    subject_4_english = fields.Char("Subject 4 English",  tracking=True)
    subject_4_units = fields.Char("Subject 4 Units",  tracking=True)
    subject_4_grade = fields.Char("Subject 4 Grade",  tracking=True) 
    Subject_4_Grade_Written_AR = fields.Char("Subject 4 Grade Written AR",  tracking=True) 
    Subject_4_Grade_Written_EN = fields.Char("Subject 4 Grade Written EN",  tracking=True)
    Subject_4_Semester  = fields.Char("Subject 4 Semester",  tracking=True)

    subject_5_arabic = fields.Char("Subject 5 Arabic",  tracking=True)
    subject_5_english = fields.Char("Subject 5 English",  tracking=True)
    subject_5_units = fields.Char("Subject 5 Units",  tracking=True)
    subject_5_grade = fields.Char("Subject 5 Grade",  tracking=True) 
    Subject_5_Grade_Written_AR = fields.Char("Subject 5 Grade Written AR",  tracking=True) 
    Subject_5_Grade_Written_EN = fields.Char("Subject 5 Grade Written EN",  tracking=True)
    Subject_5_Semester  = fields.Char("Subject 5 Semester",  tracking=True)

    subject_6_arabic = fields.Char("Subject 6 Arabic",  tracking=True)
    subject_6_english = fields.Char("Subject 6 English",  tracking=True)
    subject_6_units = fields.Char("Subject 6 Units",  tracking=True)
    subject_6_grade = fields.Char("Subject 6 Grade",  tracking=True) 
    Subject_6_Grade_Written_AR = fields.Char("Subject 6 Grade Written AR",  tracking=True) 
    Subject_6_Grade_Written_EN = fields.Char("Subject 6 Grade Written EN",  tracking=True)
    Subject_6_Semester  = fields.Char("Subject 6 Semester",  tracking=True)

    subject_7_arabic = fields.Char("Subject 7 Arabic",  tracking=True)
    subject_7_english = fields.Char("Subject 7 English",  tracking=True)
    subject_7_units = fields.Char("Subject 7 Units",  tracking=True)
    subject_7_grade = fields.Char("Subject 7 Grade",  tracking=True) 
    Subject_7_Grade_Written_AR = fields.Char("Subject 7 Grade Written AR",  tracking=True) 
    Subject_7_Grade_Written_EN = fields.Char("Subject 7 Grade Written EN",  tracking=True)
    Subject_7_Semester  = fields.Char("Subject 7 Semester",  tracking=True)

    subject_8_arabic = fields.Char("Subject 8 Arabic",  tracking=True)
    subject_8_english = fields.Char("Subject 8 English",  tracking=True)
    subject_8_units = fields.Char("Subject 8 Units",  tracking=True)
    subject_8_grade = fields.Char("Subject 8 Grade",  tracking=True) 
    Subject_8_Grade_Written_AR = fields.Char("Subject 8 Grade Written AR",  tracking=True) 
    Subject_8_Grade_Written_EN = fields.Char("Subject 8 Grade Written EN",  tracking=True)
    Subject_8_Semester  = fields.Char("Subject 8 Semester",  tracking=True)

    subject_9_arabic = fields.Char("Subject 9 Arabic",  tracking=True)
    subject_9_english = fields.Char("Subject 9 English",  tracking=True)
    subject_9_units = fields.Char("Subject 9 Units",  tracking=True)
    subject_9_grade = fields.Char("Subject 9 Grade",  tracking=True) 
    Subject_9_Grade_Written_AR = fields.Char("Subject 9 Grade Written AR",  tracking=True)
    Subject_9_Grade_Written_EN = fields.Char("Subject 9 Grade Written EN",  tracking=True)
    Subject_9_Semester  = fields.Char("Subject 9 Semester",  tracking=True)

    subject_10_arabic = fields.Char("Subject 10 Arabic",  tracking=True)
    subject_10_english = fields.Char("Subject 10 English",  tracking=True)
    subject_10_units = fields.Char("Subject 10 Units",  tracking=True)
    subject_10_grade = fields.Char("Subject 10 Grade",  tracking=True)
    Subject_10_Grade_Written_AR = fields.Char("Subject 10 Grade Written AR",  tracking=True)
    Subject_10_Grade_Written_EN = fields.Char("Subject 10 Grade Written EN",  tracking=True)
    Subject_10_Semester  = fields.Char("Subject 10 Semester",  tracking=True)

    subject_11_arabic = fields.Char("Subject 11 Arabic",  tracking=True)
    subject_11_english = fields.Char("Subject 11 English",  tracking=True)
    subject_11_units = fields.Char("Subject 11 Units",  tracking=True)
    subject_11_grade = fields.Char("Subject 11 Grade",  tracking=True)
    Subject_11_Grade_Written_AR = fields.Char("Subject 11 Grade Written AR",  tracking=True)
    Subject_11_Grade_Written_EN = fields.Char("Subject 11 Grade Written EN",  tracking=True)
    Subject_11_Semester  = fields.Char("Subject 11 Semester",  tracking=True)

    subject_12_arabic = fields.Char("Subject 12 Arabic",  tracking=True)
    subject_12_english = fields.Char("Subject 12 English",  tracking=True)
    subject_12_units = fields.Char("Subject 12 Units",  tracking=True)
    subject_12_grade = fields.Char("Subject 12 Grade",  tracking=True)
    Subject_12_Grade_Written_AR = fields.Char("Subject 12 Grade Written AR",  tracking=True)
    Subject_12_Grade_Written_EN = fields.Char("Subject 12 Grade Written EN",  tracking=True)
    Subject_12_Semester  = fields.Char("Subject 12 Semester",  tracking=True)

    subject_13_arabic = fields.Char("Subject 13 Arabic",  tracking=True)
    subject_13_english = fields.Char("Subject 13 English",  tracking=True)
    subject_13_units = fields.Char("Subject 13 Units",  tracking=True)
    subject_13_grade = fields.Char("Subject 13 Grade",  tracking=True)
    Subject_13_Grade_Written_AR = fields.Char("Subject 13 Grade Written AR",  tracking=True)
    Subject_13_Grade_Written_EN = fields.Char("Subject 13 Grade Written EN",  tracking=True)
    Subject_13_Semester  = fields.Char("Subject 13 Semester",  tracking=True)

    subject_14_arabic = fields.Char("Subject 14 Arabic",  tracking=True)
    subject_14_english = fields.Char("Subject 14 English",  tracking=True)
    subject_14_units = fields.Char("Subject 14 Units",  tracking=True)
    subject_14_grade = fields.Char("Subject 14 Grade",  tracking=True)
    Subject_14_Grade_Written_AR = fields.Char("Subject 14 Grade Written AR",  tracking=True)
    Subject_14_Grade_Written_EN = fields.Char("Subject 14 Grade Written EN",  tracking=True)
    Subject_14_Semester  = fields.Char("Subject 14 Semester",  tracking=True)

    subject_15_arabic = fields.Char("Subject 15 Arabic",  tracking=True)
    subject_15_english = fields.Char("Subject 15 English",  tracking=True)
    subject_15_units = fields.Char("Subject 15 Units",  tracking=True)
    subject_15_grade = fields.Char("Subject 15 Grade",  tracking=True)
    Subject_15_Grade_Written_AR = fields.Char("Subject 15 Grade Written AR",  tracking=True)
    Subject_15_Grade_Written_EN = fields.Char("Subject 15 Grade Written EN",  tracking=True)
    Subject_15_Semester  = fields.Char("Subject 15 Semester",  tracking=True)

    subject_16_arabic = fields.Char("Subject 16 Arabic",  tracking=True)
    subject_16_english = fields.Char("Subject 16 English",  tracking=True)
    subject_16_units = fields.Char("Subject 16 Units",  tracking=True)
    subject_16_grade = fields.Char("Subject 16 Grade",  tracking=True)
    Subject_16_Grade_Written_AR = fields.Char("Subject 16 Grade Written AR",  tracking=True)
    Subject_16_Grade_Written_EN = fields.Char("Subject 16 Grade Written EN",  tracking=True)
    Subject_16_Semester  = fields.Char("Subject 16 Semester",  tracking=True)

    subject_17_arabic = fields.Char("Subject 17 Arabic",  tracking=True)
    subject_17_english = fields.Char("Subject 17 English",  tracking=True)
    subject_17_units = fields.Char("Subject 17 Units",  tracking=True)
    subject_17_grade = fields.Char("Subject 17 Grade",  tracking=True)
    Subject_17_Grade_Written_AR = fields.Char("Subject 17 Grade Written AR",  tracking=True)
    Subject_17_Grade_Written_EN = fields.Char("Subject 17 Grade Written EN",  tracking=True)
    Subject_17_Semester  = fields.Char("Subject 17 Semester",  tracking=True)

    subject_18_arabic = fields.Char("Subject 18 Arabic",  tracking=True)
    subject_18_english = fields.Char("Subject 18 English",  tracking=True)
    subject_18_units = fields.Char("Subject 18 Units",  tracking=True)
    subject_18_grade = fields.Char("Subject 18 Grade",  tracking=True)
    Subject_18_Grade_Written_AR = fields.Char("Subject 18 Grade Written AR",  tracking=True)
    Subject_18_Grade_Written_EN = fields.Char("Subject 18 Grade Written EN",  tracking=True)
    Subject_18_Semester  = fields.Char("Subject 18 Semester",  tracking=True)

    subject_19_arabic = fields.Char("Subject 19 Arabic",  tracking=True)
    subject_19_english = fields.Char("Subject 19 English",  tracking=True)
    subject_19_units = fields.Char("Subject 19 Units",  tracking=True)
    subject_19_grade = fields.Char("Subject 19 Grade",  tracking=True)
    Subject_19_Grade_Written_AR = fields.Char("Subject 19 Grade Written AR",  tracking=True)
    Subject_19_Grade_Written_EN = fields.Char("Subject 19 Grade Written EN",  tracking=True)
    Subject_19_Semester  = fields.Char("Subject 19 Semester",  tracking=True)

    subject_20_arabic = fields.Char("Subject 20 Arabic",  tracking=True)
    subject_20_english = fields.Char("Subject 20 English",  tracking=True)
    subject_20_units = fields.Char("Subject 20 Units",  tracking=True)
    subject_20_grade = fields.Char("Subject 20 Grade",  tracking=True)
    Subject_20_Grade_Written_AR = fields.Char("Subject 20 Grade Written AR",  tracking=True)
    Subject_20_Grade_Written_EN = fields.Char("Subject 20 Grade Written EN",  tracking=True)
    Subject_20_Semester  = fields.Char("Subject 20 Semester",  tracking=True)

    subject_21_arabic = fields.Char("Subject 21 Arabic",  tracking=True)
    subject_21_english = fields.Char("Subject 21 English",  tracking=True)
    subject_21_units = fields.Char("Subject 21 Units",  tracking=True)
    subject_21_grade = fields.Char("Subject 21 Grade",  tracking=True)
    Subject_21_Grade_Written_AR = fields.Char("Subject 21 Grade Written AR",  tracking=True)
    Subject_21_Grade_Written_EN = fields.Char("Subject 21 Grade Written EN",  tracking=True)
    Subject_21_Semester  = fields.Char("Subject 21 Semester",  tracking=True)

    subject_22_arabic = fields.Char("Subject 22 Arabic",  tracking=True)
    subject_22_english = fields.Char("Subject 22 English",  tracking=True)
    subject_22_units = fields.Char("Subject 22 Units",  tracking=True)
    subject_22_grade = fields.Char("Subject 22 Grade",  tracking=True)
    Subject_22_Grade_Written_AR = fields.Char("Subject 22 Grade Written AR",  tracking=True)
    Subject_22_Grade_Written_EN = fields.Char("Subject 22 Grade Written EN",  tracking=True)
    Subject_22_Semester  = fields.Char("Subject 22 Semester",  tracking=True)

    subject_23_arabic = fields.Char("Subject 23 Arabic",  tracking=True)
    subject_23_english = fields.Char("Subject 23 English",  tracking=True)
    subject_23_units = fields.Char("Subject 23 Units",  tracking=True)
    subject_23_grade = fields.Char("Subject 23 Grade",  tracking=True)
    Subject_23_Grade_Written_AR = fields.Char("Subject 23 Grade Written AR",  tracking=True)
    Subject_23_Grade_Written_EN = fields.Char("Subject 23 Grade Written EN",  tracking=True)
    Subject_23_Semester  = fields.Char("Subject 23 Semester",  tracking=True)

    subject_24_arabic = fields.Char("Subject 24 Arabic",  tracking=True)
    subject_24_english = fields.Char("Subject 24 English",  tracking=True)
    subject_24_units = fields.Char("Subject 24 Units",  tracking=True)
    subject_24_grade = fields.Char("Subject 24 Grade",  tracking=True)
    Subject_24_Grade_Written_AR = fields.Char("Subject 24 Grade Written AR",  tracking=True)
    Subject_24_Grade_Written_EN = fields.Char("Subject 24 Grade Written EN",  tracking=True)
    Subject_24_Semester  = fields.Char("Subject 24 Semester",  tracking=True)


    subject_25_arabic = fields.Char("Subject 25 Arabic",  tracking=True)
    subject_25_english = fields.Char("Subject 25 English",  tracking=True)
    subject_25_units = fields.Char("Subject 25 Units",  tracking=True)
    subject_25_grade = fields.Char("Subject 25 Grade",  tracking=True)
    Subject_25_Grade_Written_AR = fields.Char("Subject 25 Grade Written AR",  tracking=True)
    Subject_25_Grade_Written_EN = fields.Char("Subject 25 Grade Written EN",  tracking=True)
    Subject_25_Semester  = fields.Char("Subject 25 Semester",  tracking=True)
 

    @api.model
    def create(self, vals):
        if 'exam_number_link' in vals and vals["exam_number_link"]:
            vals['grade_id'] = self.env['almaaqal.grade'].search([("exam_number_for_reference",'=',vals["exam_number_link"])], limit=1).id
        return super(SubjectAlm, self).create(vals)    

    def write(self, vals):
        if 'exam_number_link' in vals and vals["exam_number_link"]:
            vals['grade_id'] = self.env['almaaqal.grade'].search([("exam_number_for_reference",'=',vals["exam_number_link"])], limit=1).id
        return super(SubjectAlm, self).write(vals)        




#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100



class SubjectcertificateAlm(models.Model):
    _name = "certificate.subject"
    _description = "Subject"

    exam_number_link =  fields.Char("Exam Number",  tracking=True)
    stage_year = fields.Char("Year",  tracking=True)
    stage = fields.Integer("Stage")


    study_notes_in_arabic =  fields.Char("notes in arabic-stage",  tracking=True)     
    study_notes_in_english =  fields.Char("Notes in english-stage",  tracking=True) 


    subject_1_arabic = fields.Char("Subject 1 Arabic",  tracking=True)
    subject_1_english = fields.Char("Subject 1 English",  tracking=True)
    subject_1_units = fields.Char("Subject 1 Units",  tracking=True)
    subject_1_grade = fields.Char("Subject 1 Grade",  tracking=True) 
    Subject_1_Grade_Written_AR = fields.Char("Subject 1 Grade Written AR",  tracking=True) 
    Subject_1_Grade_Written_EN = fields.Char("Subject 1 Grade Written EN",  tracking=True)
    Subject_1_Semester  = fields.Char("Subject 1 Semester",  tracking=True)

    subject_2_arabic = fields.Char("Subject 2 Arabic",  tracking=True)
    subject_2_english = fields.Char("Subject 2 English",  tracking=True)
    subject_2_units = fields.Char("Subject 2 Units",  tracking=True)
    subject_2_grade = fields.Char("Subject 2 Grade",  tracking=True) 
    Subject_2_Grade_Written_AR = fields.Char("Subject 2 Grade Written AR",  tracking=True) 
    Subject_2_Grade_Written_EN = fields.Char("Subject 2 Grade Written EN",  tracking=True)
    Subject_2_Semester  = fields.Char("Subject 2 Semester",  tracking=True)

    subject_3_arabic = fields.Char("Subject 3 Arabic",  tracking=True)
    subject_3_english = fields.Char("Subject 3 English",  tracking=True)
    subject_3_units = fields.Char("Subject 3 Units",  tracking=True)
    subject_3_grade = fields.Char("Subject 3 Grade",  tracking=True) 
    Subject_3_Grade_Written_AR = fields.Char("Subject 3 Grade Written AR",  tracking=True) 
    Subject_3_Grade_Written_EN = fields.Char("Subject 3 Grade Written EN",  tracking=True)
    Subject_3_Semester  = fields.Char("Subject 3 Semester",  tracking=True)

    subject_4_arabic = fields.Char("Subject 4 Arabic",  tracking=True)
    subject_4_english = fields.Char("Subject 4 English",  tracking=True)
    subject_4_units = fields.Char("Subject 4 Units",  tracking=True)
    subject_4_grade = fields.Char("Subject 4 Grade",  tracking=True) 
    Subject_4_Grade_Written_AR = fields.Char("Subject 4 Grade Written AR",  tracking=True) 
    Subject_4_Grade_Written_EN = fields.Char("Subject 4 Grade Written EN",  tracking=True)
    Subject_4_Semester  = fields.Char("Subject 4 Semester",  tracking=True)

    subject_5_arabic = fields.Char("Subject 5 Arabic",  tracking=True)
    subject_5_english = fields.Char("Subject 5 English",  tracking=True)
    subject_5_units = fields.Char("Subject 5 Units",  tracking=True)
    subject_5_grade = fields.Char("Subject 5 Grade",  tracking=True) 
    Subject_5_Grade_Written_AR = fields.Char("Subject 5 Grade Written AR",  tracking=True) 
    Subject_5_Grade_Written_EN = fields.Char("Subject 5 Grade Written EN",  tracking=True)
    Subject_5_Semester  = fields.Char("Subject 5 Semester",  tracking=True)

    subject_6_arabic = fields.Char("Subject 6 Arabic",  tracking=True)
    subject_6_english = fields.Char("Subject 6 English",  tracking=True)
    subject_6_units = fields.Char("Subject 6 Units",  tracking=True)
    subject_6_grade = fields.Char("Subject 6 Grade",  tracking=True) 
    Subject_6_Grade_Written_AR = fields.Char("Subject 6 Grade Written AR",  tracking=True) 
    Subject_6_Grade_Written_EN = fields.Char("Subject 6 Grade Written EN",  tracking=True)
    Subject_6_Semester  = fields.Char("Subject 6 Semester",  tracking=True)

    subject_7_arabic = fields.Char("Subject 7 Arabic",  tracking=True)
    subject_7_english = fields.Char("Subject 7 English",  tracking=True)
    subject_7_units = fields.Char("Subject 7 Units",  tracking=True)
    subject_7_grade = fields.Char("Subject 7 Grade",  tracking=True) 
    Subject_7_Grade_Written_AR = fields.Char("Subject 7 Grade Written AR",  tracking=True) 
    Subject_7_Grade_Written_EN = fields.Char("Subject 7 Grade Written EN",  tracking=True)
    Subject_7_Semester  = fields.Char("Subject 7 Semester",  tracking=True)

    subject_8_arabic = fields.Char("Subject 8 Arabic",  tracking=True)
    subject_8_english = fields.Char("Subject 8 English",  tracking=True)
    subject_8_units = fields.Char("Subject 8 Units",  tracking=True)
    subject_8_grade = fields.Char("Subject 8 Grade",  tracking=True) 
    Subject_8_Grade_Written_AR = fields.Char("Subject 8 Grade Written AR",  tracking=True) 
    Subject_8_Grade_Written_EN = fields.Char("Subject 8 Grade Written EN",  tracking=True)
    Subject_8_Semester  = fields.Char("Subject 8 Semester",  tracking=True)

    subject_9_arabic = fields.Char("Subject 9 Arabic",  tracking=True)
    subject_9_english = fields.Char("Subject 9 English",  tracking=True)
    subject_9_units = fields.Char("Subject 9 Units",  tracking=True)
    subject_9_grade = fields.Char("Subject 9 Grade",  tracking=True) 
    Subject_9_Grade_Written_AR = fields.Char("Subject 9 Grade Written AR",  tracking=True)
    Subject_9_Grade_Written_EN = fields.Char("Subject 9 Grade Written EN",  tracking=True)
    Subject_9_Semester  = fields.Char("Subject 9 Semester",  tracking=True)

    subject_10_arabic = fields.Char("Subject 10 Arabic",  tracking=True)
    subject_10_english = fields.Char("Subject 10 English",  tracking=True)
    subject_10_units = fields.Char("Subject 10 Units",  tracking=True)
    subject_10_grade = fields.Char("Subject 10 Grade",  tracking=True)
    Subject_10_Grade_Written_AR = fields.Char("Subject 10 Grade Written AR",  tracking=True)
    Subject_10_Grade_Written_EN = fields.Char("Subject 10 Grade Written EN",  tracking=True)
    Subject_10_Semester  = fields.Char("Subject 10 Semester",  tracking=True)

    subject_11_arabic = fields.Char("Subject 11 Arabic",  tracking=True)
    subject_11_english = fields.Char("Subject 11 English",  tracking=True)
    subject_11_units = fields.Char("Subject 11 Units",  tracking=True)
    subject_11_grade = fields.Char("Subject 11 Grade",  tracking=True)
    Subject_11_Grade_Written_AR = fields.Char("Subject 11 Grade Written AR",  tracking=True)
    Subject_11_Grade_Written_EN = fields.Char("Subject 11 Grade Written EN",  tracking=True)
    Subject_11_Semester  = fields.Char("Subject 11 Semester",  tracking=True)

    subject_12_arabic = fields.Char("Subject 12 Arabic",  tracking=True)
    subject_12_english = fields.Char("Subject 12 English",  tracking=True)
    subject_12_units = fields.Char("Subject 12 Units",  tracking=True)
    subject_12_grade = fields.Char("Subject 12 Grade",  tracking=True)
    Subject_12_Grade_Written_AR = fields.Char("Subject 12 Grade Written AR",  tracking=True)
    Subject_12_Grade_Written_EN = fields.Char("Subject 12 Grade Written EN",  tracking=True)
    Subject_12_Semester  = fields.Char("Subject 12 Semester",  tracking=True)

    subject_13_arabic = fields.Char("Subject 13 Arabic",  tracking=True)
    subject_13_english = fields.Char("Subject 13 English",  tracking=True)
    subject_13_units = fields.Char("Subject 13 Units",  tracking=True)
    subject_13_grade = fields.Char("Subject 13 Grade",  tracking=True)
    Subject_13_Grade_Written_AR = fields.Char("Subject 13 Grade Written AR",  tracking=True)
    Subject_13_Grade_Written_EN = fields.Char("Subject 13 Grade Written EN",  tracking=True)
    Subject_13_Semester  = fields.Char("Subject 13 Semester",  tracking=True)

    subject_14_arabic = fields.Char("Subject 14 Arabic",  tracking=True)
    subject_14_english = fields.Char("Subject 14 English",  tracking=True)
    subject_14_units = fields.Char("Subject 14 Units",  tracking=True)
    subject_14_grade = fields.Char("Subject 14 Grade",  tracking=True)
    Subject_14_Grade_Written_AR = fields.Char("Subject 14 Grade Written AR",  tracking=True)
    Subject_14_Grade_Written_EN = fields.Char("Subject 14 Grade Written EN",  tracking=True)
    Subject_14_Semester  = fields.Char("Subject 14 Semester",  tracking=True)

    subject_15_arabic = fields.Char("Subject 15 Arabic",  tracking=True)
    subject_15_english = fields.Char("Subject 15 English",  tracking=True)
    subject_15_units = fields.Char("Subject 15 Units",  tracking=True)
    subject_15_grade = fields.Char("Subject 15 Grade",  tracking=True)
    Subject_15_Grade_Written_AR = fields.Char("Subject 15 Grade Written AR",  tracking=True)
    Subject_15_Grade_Written_EN = fields.Char("Subject 15 Grade Written EN",  tracking=True)
    Subject_15_Semester  = fields.Char("Subject 15 Semester",  tracking=True)

    subject_16_arabic = fields.Char("Subject 16 Arabic",  tracking=True)
    subject_16_english = fields.Char("Subject 16 English",  tracking=True)
    subject_16_units = fields.Char("Subject 16 Units",  tracking=True)
    subject_16_grade = fields.Char("Subject 16 Grade",  tracking=True)
    Subject_16_Grade_Written_AR = fields.Char("Subject 16 Grade Written AR",  tracking=True)
    Subject_16_Grade_Written_EN = fields.Char("Subject 16 Grade Written EN",  tracking=True)
    Subject_16_Semester  = fields.Char("Subject 16 Semester",  tracking=True)

    subject_17_arabic = fields.Char("Subject 17 Arabic",  tracking=True)
    subject_17_english = fields.Char("Subject 17 English",  tracking=True)
    subject_17_units = fields.Char("Subject 17 Units",  tracking=True)
    subject_17_grade = fields.Char("Subject 17 Grade",  tracking=True)
    Subject_17_Grade_Written_AR = fields.Char("Subject 17 Grade Written AR",  tracking=True)
    Subject_17_Grade_Written_EN = fields.Char("Subject 17 Grade Written EN",  tracking=True)
    Subject_17_Semester  = fields.Char("Subject 17 Semester",  tracking=True)

    subject_18_arabic = fields.Char("Subject 18 Arabic",  tracking=True)
    subject_18_english = fields.Char("Subject 18 English",  tracking=True)
    subject_18_units = fields.Char("Subject 18 Units",  tracking=True)
    subject_18_grade = fields.Char("Subject 18 Grade",  tracking=True)
    Subject_18_Grade_Written_AR = fields.Char("Subject 18 Grade Written AR",  tracking=True)
    Subject_18_Grade_Written_EN = fields.Char("Subject 18 Grade Written EN",  tracking=True)
    Subject_18_Semester  = fields.Char("Subject 18 Semester",  tracking=True)

    subject_19_arabic = fields.Char("Subject 19 Arabic",  tracking=True)
    subject_19_english = fields.Char("Subject 19 English",  tracking=True)
    subject_19_units = fields.Char("Subject 19 Units",  tracking=True)
    subject_19_grade = fields.Char("Subject 19 Grade",  tracking=True)
    Subject_19_Grade_Written_AR = fields.Char("Subject 19 Grade Written AR",  tracking=True)
    Subject_19_Grade_Written_EN = fields.Char("Subject 19 Grade Written EN",  tracking=True)
    Subject_19_Semester  = fields.Char("Subject 19 Semester",  tracking=True)

    subject_20_arabic = fields.Char("Subject 20 Arabic",  tracking=True)
    subject_20_english = fields.Char("Subject 20 English",  tracking=True)
    subject_20_units = fields.Char("Subject 20 Units",  tracking=True)
    subject_20_grade = fields.Char("Subject 20 Grade",  tracking=True)
    Subject_20_Grade_Written_AR = fields.Char("Subject 20 Grade Written AR",  tracking=True)
    Subject_20_Grade_Written_EN = fields.Char("Subject 20 Grade Written EN",  tracking=True)
    Subject_20_Semester  = fields.Char("Subject 20 Semester",  tracking=True)

    subject_21_arabic = fields.Char("Subject 21 Arabic",  tracking=True)
    subject_21_english = fields.Char("Subject 21 English",  tracking=True)
    subject_21_units = fields.Char("Subject 21 Units",  tracking=True)
    subject_21_grade = fields.Char("Subject 21 Grade",  tracking=True)
    Subject_21_Grade_Written_AR = fields.Char("Subject 21 Grade Written AR",  tracking=True)
    Subject_21_Grade_Written_EN = fields.Char("Subject 21 Grade Written EN",  tracking=True)
    Subject_21_Semester  = fields.Char("Subject 21 Semester",  tracking=True)

    subject_22_arabic = fields.Char("Subject 22 Arabic",  tracking=True)
    subject_22_english = fields.Char("Subject 22 English",  tracking=True)
    subject_22_units = fields.Char("Subject 22 Units",  tracking=True)
    subject_22_grade = fields.Char("Subject 22 Grade",  tracking=True)
    Subject_22_Grade_Written_AR = fields.Char("Subject 22 Grade Written AR",  tracking=True)
    Subject_22_Grade_Written_EN = fields.Char("Subject 22 Grade Written EN",  tracking=True)
    Subject_22_Semester  = fields.Char("Subject 22 Semester",  tracking=True)

    subject_23_arabic = fields.Char("Subject 23 Arabic",  tracking=True)
    subject_23_english = fields.Char("Subject 23 English",  tracking=True)
    subject_23_units = fields.Char("Subject 23 Units",  tracking=True)
    subject_23_grade = fields.Char("Subject 23 Grade",  tracking=True)
    Subject_23_Grade_Written_AR = fields.Char("Subject 23 Grade Written AR",  tracking=True)
    Subject_23_Grade_Written_EN = fields.Char("Subject 23 Grade Written EN",  tracking=True)
    Subject_23_Semester  = fields.Char("Subject 23 Semester",  tracking=True)

    subject_24_arabic = fields.Char("Subject 24 Arabic",  tracking=True)
    subject_24_english = fields.Char("Subject 24 English",  tracking=True)
    subject_24_units = fields.Char("Subject 24 Units",  tracking=True)
    subject_24_grade = fields.Char("Subject 24 Grade",  tracking=True)
    Subject_24_Grade_Written_AR = fields.Char("Subject 24 Grade Written AR",  tracking=True)
    Subject_24_Grade_Written_EN = fields.Char("Subject 24 Grade Written EN",  tracking=True)
    Subject_24_Semester  = fields.Char("Subject 24 Semester",  tracking=True)


    subject_25_arabic = fields.Char("Subject 25 Arabic",  tracking=True)
    subject_25_english = fields.Char("Subject 25 English",  tracking=True)
    subject_25_units = fields.Char("Subject 25 Units",  tracking=True)
    subject_25_grade = fields.Char("Subject 25 Grade",  tracking=True)
    Subject_25_Grade_Written_AR = fields.Char("Subject 25 Grade Written AR",  tracking=True)
    Subject_25_Grade_Written_EN = fields.Char("Subject 25 Grade Written EN",  tracking=True)
    Subject_25_Semester  = fields.Char("Subject 25 Semester",  tracking=True)
 


# class AlmaaqalGradeAll(models.Model):
#     _inherit = "res.partner"

#     Status = fields.Selection(
#         selection_add=[("hosting_university", " استضافة من الجامعة")],
#     )