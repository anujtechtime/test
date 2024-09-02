# -*- coding: utf-8 -*-

from odoo import models, fields, api, _ 
from datetime import date
import base64

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


    

    posted_date = fields.Date("Posted Date",  tracking=True)
    average_word_word = fields.Char("average_word_word",  tracking=True)
    remark = fields.Many2many("grade.remark", string="Remark", tracking=True)


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
        
    
    def print_arabic_no_grade_pdf(self):
        # Generate PDF report
        report = self.env.ref('almaaqal_certificate.action_report_almaaqal_certificate')
        print("self@@@@@@@@@@@@@",self.ids)

        pdf_content, _ = report.render_qweb_pdf(res_ids=self.ids)

        # Convert PDF to base64
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

        # Create attachment
        attachment = self.env['ir.attachment'].create({
            'name': 'Report.pdf',
            'type': 'binary',
            'datas': pdf_base64,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf'
        })


        self.env["almaaqal.certificate"].create({
            'Status' : self.Status,
            'exam_number_for_reference' : self.exam_number_for_reference,
            'college_in_english' : self.college_in_english,
            'college_in_arabic' : self.college_in_arabic,
            'study_type_arabic' : self.study_type_arabic,
            'study_type_english' : self.study_type_english,
            'serial' : self.serial,
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
            # 'subject' : (6, 0, [docs.subject.ids if docs.subject else False]) ,
            })

        print("CCCCCCCCCCCCCCCC",self.env.user)

        remard_id = self.remark.create({
            "attachment_filename" : "Arabic No Grade.pdf",
            "attachment_file" : pdf_base64,
            "user_id" : self.env.user.id
            })
        self.remark = [(4, remard_id.id)]
        # report._get_report_values(self.ids)
        # Post attachment to Chatter
        self.message_post(
            body="Arabic No Grade (PDF),",
            attachment_ids=[attachment.id]
        )

        return self.env.ref('almaaqal_certificate.action_report_almaaqal_certificate').report_action(self)


    def print_arabic_with_grade(self):
        # Generate PDF report
        report = self.env.ref('almaaqal_certificate.action_report_almaaqal_certificate_with_grade')
        print("self@@@@@@@@@@@@@",self.ids)

        pdf_content, _ = report.render_qweb_pdf(res_ids=self.ids)

        # Convert PDF to base64
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

        # Create attachment
        attachment = self.env['ir.attachment'].create({
            'name': 'Report.pdf',
            'type': 'binary',
            'datas': pdf_base64,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf'
        })

        print("CCCCCCCCCCCCCCCC",self.env.user)

        remard_id = self.remark.create({
            "attachment_filename" : "Arabic With Grade.pdf",
            "attachment_file" : pdf_base64,
            "user_id" : self.env.user.id
            })
        self.remark = [(4, remard_id.id)]
        # report._get_report_values(self.ids)
        # Post attachment to Chatter
        self.message_post(
            body="Arabic With Grade (PDF),",
            attachment_ids=[attachment.id]
        )

        self.env["almaaqal.certificate"].create({
            'Status' : self.Status,
            'exam_number_for_reference' : self.exam_number_for_reference,
            'college_in_english' : self.college_in_english,
            'college_in_arabic' : self.college_in_arabic,
            'study_type_arabic' : self.study_type_arabic,
            'study_type_english' : self.study_type_english,
            'serial' : self.serial,
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
            # 'subject' : (6, 0, [docs.subject.ids if docs.subject else False]) ,
            })

        return self.env.ref('almaaqal_certificate.action_report_almaaqal_certificate_with_grade').report_action(self)    


class RemarkGrade(models.Model):
    _name = "grade.remark"
    _description = "Remark"

    # attachment_ids = fields.Binary("Attachment")
    # attachment_ids = fields.Many2one('ir.attachment', string='Attachments')

    attachment_file = fields.Binary(string="Attachment File")
    attachment_filename = fields.Char(string="Filename")

    user_id = fields.Many2one("res.users", string="User")
    serial = fields.Char("Serial")



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

    @api.model
    def create(self, vals):
        if 'exam_number_link' in vals and vals["exam_number_link"]:
            vals['grade_id'] = self.env['almaaqal.grade'].search([("exam_number_for_reference",'=',vals["exam_number_link"])], limit=1).id
        return super(SubjectAlm, self).create(vals)    

    def write(self, vals):
        if 'exam_number_link' in vals and vals["exam_number_link"]:
            vals['grade_id'] = self.env['almaaqal.grade'].search([("exam_number_for_reference",'=',vals["exam_number_link"])], limit=1).id
        return super(SubjectAlm, self).write(vals)        



class ArabicSummaryReport(models.AbstractModel):
    _name = 'report.almaaqal_certificate.report_almaaqal_certificate'
    _description = 'Holidays Summary Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("self##############222222222222222",docids)
        docs = self.env['almaaqal.grade'].browse(docids) 
        # holidays = self.env['hr.leave'].browse(self.ids)

        self.env["almaaqal.certificate"].create({
            'Status' : docs.Status,
            'exam_number_for_reference' : docs.exam_number_for_reference,
            'college_in_english' : docs.college_in_english,
            'college_in_arabic' : docs.college_in_arabic,
            'study_type_arabic' : docs.study_type_arabic,
            'study_type_english' : docs.study_type_english,
            'serial' : docs.serial,
            'gender' : docs.gender,
            'subject_to_arabic' : docs.subject_to_arabic,
            'subject_to_english' : docs.subject_to_english,
            'certificate_name_department_AR' : docs.certificate_name_department_AR,
            'certificate_name_department_EN' : docs.certificate_name_department_EN,
            'University_order_number' : docs.University_order_number,
            'University_order_date' : docs.University_order_date,
            'dean_collage_name_arabic' : docs.dean_collage_name_arabic,
            'dean_collage_name_english' : docs.dean_collage_name_english,
            'department_in_english' : docs.department_in_english,
            'department_in_arabic' : docs.department_in_arabic,
            'stage_year' : docs.stage_year,
            'year_of_graduation' : docs.year_of_graduation,
            'student_name_in_english' : docs.student_name_in_english,
            'student_name_in_arabic' : docs.student_name_in_arabic,
            'nationality_ar' : docs.nationality_ar,
            'nationality_en' : docs.nationality_en,
            'average' : docs.average,
            'average_in_words_en' : docs.average_in_words_en,
            'average_in_words_ar' : docs.average_in_words_ar,
            'attempt_en' : docs.attempt_en,
            'attempt_ar' : docs.attempt_ar,
            'study_year_name_ar' : docs.study_year_name_ar,
            'study_year_name_en' : docs.study_year_name_en,
            'Graduate_Sequence' : docs.Graduate_Sequence,
            'The_average_of_the_first_student_in_the_class' : docs.The_average_of_the_first_student_in_the_class,
            'Total_number_of_graduates' : docs.Total_number_of_graduates,
            # 'subject' : (6, 0, [docs.subject.ids if docs.subject else False]) ,
            })
        
        return {
            'doc_ids': docids,
            'doc_model': "almaaqal.grade",
            'docs': docs,
        } 


#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
