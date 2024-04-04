# -*- coding: utf-8 -*-

from odoo import models, fields, api , _ 
from odoo.exceptions import UserError, ValidationError
from googletrans import Translator
import googletrans
import logging
import base64
from pdf2image import convert_from_path
from io import BytesIO
from PIL import Image, ImageFilter
from PIL import Image 
from datetime import date, datetime, timedelta

_logger = logging.getLogger(__name__)




class almaqal_templates(models.Model):
    _inherit = "sale.order"


    # @api.model
    # def create(self, vals):
    #     result = super(almaqal_templates, self).create(vals)
    #     print("result##############",result)    
    #     print("result.college###########",result.college,result.department,result.student, result.year)
    #     installmet_dat = result.env["installment.details"].search([('college' , '=', result.college.id),("level","=",result.level),("Subject","=",result.Subject),('department','=',result.department.id),('Student','=',result.student.id),('year','=', result.year.id)],limit=1)
    #     print("result.id#$$$$$$$$$$$$$$$",installmet_dat)
    #     print("installmet_dat@@@@@@@@@@@@@@@",installmet_dat)
    #     if installmet_dat:
    #         print("sale_installment_line_ids########",installmet_dat.sale_installment_line_ids.ids)
    #         # for datts in installmet_dat.sale_installment_line_ids:
    #         # result.sale_installment_line_ids = [(6, 0, installmet_dat.sale_installment_line_ids.ids)]
    #         result.installment_amount = installmet_dat.installment
    #         # result.payable_amount = installmet_dat.installment / installmet_dat.installment_number
    #         result.tenure_month = installmet_dat.installment_number
    #         result.second_payment_date = datetime.today().date()
    #         order_line = result.env['sale.order.line'].create({
    #             'product_id': 1,
    #             'price_unit': result.installment_amount,
    #             'product_uom': result.env.ref('uom.product_uom_unit').id,
    #             'product_uom_qty': 1,
    #             'order_id': result._origin.id,
    #             'name': 'sales order line',
    #         })
    #     failed_student = self.env["sale.order"].search([("partner_id","=",result.partner_id.id),("college","=",result.partner_id.college.id),("year","!=",result.partner_id.year.id),("level","=",result.partner_id.level)], limit=1)
    #     print("failed_student@@@@@@@@@@@@@@@@",failed_student)
    #     _logger.info("failed_student************11111111111111#####**%s" %failed_student)
    #     if failed_student:
    #         result.installment_amount = failed_student.installment_amount
    #         for i in failed_student.sale_installment_line_ids:
    #             installment = result.sale_installment_line_ids.create({
    #             'number' : i.number,
    #             'payment_date' : i.payment_date,
    #             'amount_installment' : i.amount_installment,
    #             'description': 'Installment Payment',
    #             'sale_installment_id' : result.id,
    #             # "invoice_id" : invoice_id.id
    #             })  
    #     if not failed_student and installmet_dat:
    #         count = 0
    #         for i in installmet_dat.sale_installment_line_ids:
    #             sale_installment = result.sale_installment_line_ids.create({
    #                 'number' : i.number,
    #                 'payment_date' : i.payment_date,
    #                 'amount_installment' : i.amount_installment,
    #                 'description': 'Installment Payment',
    #                 'sale_installment_id' : result.id,
    #                 # "invoice_id" : invoice_id.id
    #                 })
    #             count = count + 1          

    #     return result

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
            if failed_student:
                self.installment_amount = failed_student.installment_amount
                for i in failed_student.sale_installment_line_ids:
                    installment = self.sale_installment_line_ids.create({
                    'number' : i.number,
                    'payment_date' : i.payment_date,
                    'amount_installment' : i.amount_installment,
                    'description': 'Installment Payment',
                    'sale_installment_id' : self._origin.id,
                    # "invoice_id" : invoice_id.id
                    })
                return {'warning': { 
                    'title': "Warning", 
                    'message': 'هذا الطالب راسب, هل تريد اكمال عملية التسجيل؟', 
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
            #     raise UserError(_('الطالب لم يرحل. هل تريد اكمال عملية التسجيل؟'))
#     _name = 'almaqal_templates.almaqal_templates'
#     _description = 'almaqal_templates.almaqal_templates'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class Techtest(models.Model):
    _inherit = 'res.partner'


    name_english = fields.Char("English Name")
    batch_number = fields.Char(string='Badge', required=True,
                          readonly=True, default=lambda self: _('New'))
    date_of_expiration = fields.Date("Date Of  Expiration")
    image_stuent = fields.Binary("Image Student badge")

    @api.model
    def increase_image_sharpness(self, image):
        if image:
            # Convert base64 image to bytes
            image_bytes = base64.b64decode(image)
            
            # Open the image using PIL
            img = Image.open(BytesIO(image_bytes))

            # Apply sharpening filter
            sharpened_img = img.filter(ImageFilter.SHARPEN)

            # Convert back to base64
            buffer = BytesIO()
            sharpened_img.save(buffer, format="png")
            image_bytes_sharp = buffer.getvalue()

            return base64.b64encode(image_bytes_sharp)
        return False

    def write(self, vals):
        if 'image_1920' in vals:
            vals['image_1920'] = self.increase_image_sharpness(vals['image_1920'])
        return super(Techtest, self).write(vals)     

    @api.onchange('date_of_expiration','batch_number', 'name_english','name', 'college','level','year_born','batch_number')
    def _onchange_year_born(self):
        if self.date_of_expiration and self.batch_number and self.name_english and self.name and self.college and self.level and self.image_1920 and self.year_born and self.batch_number:
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

    def print_student_badge(self):
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

        # self.image_stuent = encoded_excel
        self.image_stuent = self.increase_image_sharpness(encoded_excel)
        return {
                     'type' : 'ir.actions.act_url',
                     'url': '/web/image?model=res.partner&field=image_stuent&id=%s&download=true'%(self.id),
                     'target': 'self',
         }

    def sequence_amiu(self):
        for batch in self:
            batch.batch_number = self.env['ir.sequence'].next_by_code('badge.sequence')

    @api.model
    def create(self, vals):
       if vals.get('batch_number', _('New')) == _('New'):
           vals['batch_number'] = self.env['ir.sequence'].next_by_code(
               'badge.sequence') or _('New')
           

       res = super(Techtest, self).create(vals)
       # text = res.name
       # translator = Translator()
       # translated_text = translator.translate(text, src='ar', dest='en')
       # res.name_english = translated_text.text
       return res  

    # @api.onchange('name')
    # def _onchange_name(self):
    #     for sstd in self:
    #         if sstd.name:
    #             text = sstd.name
    #             print("text###############",text)
    #             translator = Translator()
    #             translated_text = translator.translate(text, src='ar', dest='en')
    #             sstd.name_english = translated_text.text