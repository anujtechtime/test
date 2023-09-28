# -*- coding: utf-8 -*-

from odoo import models, fields, api , _ 
from odoo.exceptions import UserError, ValidationError
from googletrans import Translator
import googletrans



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
    batch_number = fields.Char("Batch Number")
    date_of_expiration = fields.Char("Date Of  Expiration")

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
