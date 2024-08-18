# -*- coding: utf-8 -*-
# from odoo import http

# from odoo import http
# from odoo.http import request
# from docx import Document
# import zipfile
# import io
# from docx.shared import Pt
# from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

# class Binary(http.Controller):
#     @http.route('/web/binary/download_docx_report/<int:record_id>', type='http', auth="public")
#     def download_function_descriptions(self, record_id):
#         stream = io.BytesIO()
#         zip_archive = zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED)
#         document1 = Document()


#         record = request.env['almaaqal.grade'].sudo().browse(record_id)

#         print("record@@@@@@@@@@@@@@",record)

#         # document1.style = document1.styles['Body Text']
#         # document1.style.font.size = 12
#         # document1.style.font.name = 'Times New Roman'
#         # document1.add_run(boldText).bold = True
#         # document1.add_run(dataText)
#         print("self################3",self)

#         average_word = ""

#         if float(record.average) < 50:
#             average_word = 'راسب'
#         if float(record.average) < 60 and float(record.average) > 49.99:
#             average_word = 'مقبول'
        

#         if float(record.average) < 70 and float(record.average) > 59.99:
#             average_word = 'متوسط'
        

#         if float(record.average) < 80 and float(record.average) > 69.99:
#             average_word = 'جيد'
        
#         if float(record.average) < 90 and float(record.average) > 79.99:
#             average_word = 'جيد جدا'
        
#         if float(record.average) < 100 and float(record.average) > 89.99:
#             average_word = 'ممتاز'
        
#         para0 = document1.add_paragraph('قسم شؤون الطلبة والتسجیل')
#         para0.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

#         para1 = document1.add_paragraph('(وثيقة تخرج)')
#         para1.paragraph_format.space_before = Pt(130)
#         para1.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
#         # para1.paragraph_format.left_indent = Pt(172)

#         para2 = document1.add_paragraph(f'الى/ {record.subject_to_arabic}')
#         para2.paragraph_format.space_before = Pt(60)
#         para2.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
#         # para2.paragraph_format.left_indent = Pt(180)


        

#         para3 = document1.add_paragraph(f'نؤيد لكم بان السيد ( {record.student_name_in_arabic} ) الملصقة صورته اعلاه هو احد خريجي جامعة المعقل   / {record.college_in_arabic}  / {record.department_in_arabic}  /  الدراسة {record.study_type_arabic} للعام الدراسي {record.year_of_graduation}  ({record.attempt_ar}).   وقد منح شهادة  {record.certificate_name_department_AR}    بتقدير ({average_word})  وبمعدل  ({round(float(record.average),2)} %)  {record.study_year_name_ar} دراسية  بموجب الامر الجامعي ذي العدد  {record.University_order_number}  في   {record.University_order_date}')
#         para3.paragraph_format.space_before = Pt(80)


#         para4 = document1.add_paragraph('أ. د بدر  نعمة عكاش البدران')
#         para4.paragraph_format.space_before = Pt(80)
#         # para4.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

#         para5 = document1.add_paragraph('رئيس الجامعة')
#         para5.paragraph_format.space_before = Pt(20)
#         # para5.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

#         para6 = document1.add_paragraph('ملاحظة//-  الوثيقة خالية من الشطب والتعديل')
#         # para5.paragraph_format.space_before = Pt(20)
#         para6.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

#         # رئيس الجامعة
#         para5.paragraph_format.left_indent = Pt(10)


#         document1_file_name = "Arabic No Grade.docx"
#         document1.save(document1_file_name)
#         zip_archive.write(document1_file_name)
#         document2 = Document()
#         document2.add_paragraph('Test Paragraph for SECOND document')
#         document2_file_name = "test2.docx"
#         document2.save(document2_file_name)
#         zip_archive.write(document2_file_name)
#         zip_archive.close()
#         bytes_of_zipfile = stream.getvalue()
#         return request.make_response(bytes_of_zipfile,[('Content-Type', 'application/zip'),('Content-Disposition', 'attachment')])



# class AlmaaqalCertificate(http.Controller):
#     @http.route('/almaaqal_certificate/almaaqal_certificate/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaaqal_certificate/almaaqal_certificate/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaaqal_certificate.listing', {
#             'root': '/almaaqal_certificate/almaaqal_certificate',
#             'objects': http.request.env['almaaqal_certificate.almaaqal_certificate'].search([]),
#         })

#     @http.route('/almaaqal_certificate/almaaqal_certificate/objects/<model("almaaqal_certificate.almaaqal_certificate"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaaqal_certificate.object', {
#             'object': obj
#         })
