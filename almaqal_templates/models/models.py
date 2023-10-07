# -*- coding: utf-8 -*-

from odoo import models, fields, api , _ 
from odoo.exceptions import UserError, ValidationError
from googletrans import Translator
import googletrans
import base64
from pdf2image import convert_from_path
from PIL import Image 



class almaqal_templates(models.Model):
    _inherit = "sale.order"

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            year_active  = self.env["year.year"].search([("active", "=", True)])
            self.year = self.year.id
            self.partner_id = self.partner_id.id
            print("year_active@@@@@@@@@@@@@@@",year_active)
            print("selfddddddddddddddddddddd",self.year)

            if self.partner_id.year.id not in year_active.mapped("id"):
                return {'warning': { 
                    'title': "Warning", 
                    'message': 'الطالب لم يرحل. هل تريد اكمال عملية التسجيل؟', 
                    } 
                }
            failed_student = self.env["sale.order"].search([("partner_id","=",self.partner_id.id),("college","=",self.partner_id.college.id),("year","!=",self.partner_id.year.id),("level","=",self.partner_id.level)], limit=1)
            print("failed_student@@@@@@@@@@@@@@@",failed_student)
            print("self.partner_id@@@@@@@@@@@@@@",self.partner_id)
            print("self.college@@@@@@@@@@@@@@@",self.college)
            print("self.year@@@@@@@@@@@@@@@@@@@",self.year)
            print("level@@@@@@@@@@@@@@@",self.level)
            if failed_student:
                self.installment_amount = failed_student.installment_amount
                return {'warning': { 
                    'title': "Warning", 
                    'message': 'This Student is failed.', 
                    } 
                }      

class almaqalPayment(models.Model):
    _inherit = "account.payment"

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            year_active  = self.env["year.year"].search([("active", "=", True)])
            self.year = self.year.id
            self.partner_id = self.partner_id.id

            if self.partner_id.year.id not in year_active.mapped("id"):
                return {'warning': { 
                    'title': "Warning", 
                    'message': 'الطالب لم يرحل. هل تريد اكمال عملية التسجيل؟', 
                    } 
                }       


class Techtest(models.Model):
    _inherit = 'res.partner'

    name_english = fields.Char("English Name")
    batch_number = fields.Char("Batch Number")
    date_of_expiration = fields.Date("Date Of  Expiration")
    image_stuent = fields.Binary("Image Student badge")

    def _onchange_year_born(self):
        print_report = self.env.ref('almaqal_templates.report_payment_receipt_student_batch_data').sudo().render_qweb_pdf(self.ids)
        print("print_report#############",print_report)

        pdf_credit_score = base64.b64encode(print_report[0]) 

        print("pdf_credit_score@@@@@@@@@@@@@@@@@@@@@",pdf_credit_score)

        f = open('/opt/odoo13/odoo/sample.pdf', 'wb')


        f.write(print_report[0])

        images = convert_from_path('/opt/odoo13/odoo/sample.pdf')


        for i in range(len(images)):
            images[i].save('page'+ str(i) +'.jpg') 
 
  
        # Store path of the output image in the variable output_path 
        output_path = '/opt/odoo13/odoo/sample.pdf' 
          
        # Processing the image 
        inputs = Image.open('page0.jpg') 
          
        # # Removing the background from the given Image 
        # output = remove(inputs) 
          
        # #Saving the image in the given path 
        # output.save(output_path)  

        # img = Image.open("./image.png")
        img = inputs.convert("RGBA")
     
        datas = img.getdata()
     
        newData = []
     
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
     
        img.putdata(newData)

        print("img@@@@@@@@@@@@@@@@@@@@@@@@@@@",img)
        img.save("./New.png", "PNG")
        print("Successful")

        print("img@@@@@@@@@@@@@@ccccccccccc",img)


        def open_target_file(target_path):
            with open(target_path,"rb") as excel_file:
                return excel_file.read()

        def encode_file(excel_file):
            return base64.b64encode(excel_file)

        def decode_file():
            return base64.b64decode(excel_file)

        destiny_path = ""

        excel_file = open_target_file('New.png')
        encoded_excel = encode_file(excel_file)

        self.image_stuent = encoded_excel

    @api.onchange('name')
    def _onchange_name(self):
        for sstd in self:
            if sstd.name:
                text = sstd.name
                print("text###############",text)
                translator = Translator()
                translated_text = translator.translate(text, src='ar', dest='en')
                sstd.name_english = translated_text.text
            
            # print("translation@@@@@@@@",translated_text.text)
            # print(googletrans.LANGUAGES)
