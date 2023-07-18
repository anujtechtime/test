# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import qrcode
import base64
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO
from io import BytesIO
from datetime import date as date_n  
from odoo.exceptions import UserError, ValidationError
from barcode import EAN13
from barcode.writer import ImageWriter
import random

   



class SaleOrderField_user(models.Model):
    _inherit = 'account.move'

    # @api.depends('in_date')
    # def _compute_level(self):
    #     for expense in self:
    #         
            

    receipt_number = fields.Char("Receipt Number")
    car_number = fields.Char(string="Car Number")
    car_type = fields.Selection([('small','Small'),('large','Large')], string="Car Type")
    car_type_drop_down = fields.Selection([('container','container'),('refrigerator','refrigerator')], string="Large Car")
    in_date = fields.Datetime("In Date")
    out_date = fields.Datetime("Out Date")


    qr_code = fields.Binary("QR Code", attachment=True, store=True)

    amount_for_parking = fields.Monetary("Parking Amount", store=True, currency_field='currency_id')


    @api.model
    def create(self, vals):
        res =  super(SaleOrderField_user, self).create(vals)
        res.in_date = datetime.today()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data("In Time :" + str(res.in_date + relativedelta(hours=5.5)) + ", Receipt Number : " + str(res.receipt_number) + ", Car Number :" + res.car_number)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        res.qr_code = qr_image
        return res


    def button_check_out(self):
        for out in self:
            out.out_date = datetime.today()
            self.generate_out_date()

    @api.onchange('out_date')
    def generate_out_date(self):  
        if self.in_date and self.out_date:
            self.amount_for_parking = 4000 * ((self.out_date - self.in_date).days + 1)
            print("self.amount_for_parking@@@@@@@@@@@@@@",self.amount_for_parking)


    @api.onchange('in_date', 'receipt_number')
    def generate_qr_code(self):
        if self.in_date:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data("In Time :" + str(self.in_date + relativedelta(hours=5.5)) + ", Receipt Number : " + str(self.receipt_number) + ", Car Number :" + self.car_number)
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            self.qr_code = qr_image


    # @api.onchange('receipt_number')
    # def generate_qr_code(self):
    #     for ddts in self:
    #         # ddts.receipt_number = random.randint(100000000000,999999999999)
    #         if ddts.receipt_number:
    #             if len(ddts.receipt_number) != 12:
    #                 return ValidationError(_("The Receipt Number must be of 12 Digits!."))
    #             # qr = qrcode.QRCode(
    #             #     version=1,
    #             #     error_correction=qrcode.constants.ERROR_CORRECT_L,
    #             #     box_size=10,
    #             #     border=4,
    #             # )
    #             # qr.add_data("In Time :" + str(self.in_date + relativedelta(hours=5.5)))
    #             # qr.make(fit=True)
    #             # img = qr.make_image()
    #             temp = BytesIO()

    #             img = EAN13(str(ddts.receipt_number), writer=ImageWriter())

    #             print("img@@@@@@@@@@@@@@@",img)


    #             data = img.save("new_code")
    #             # my_code.save(“”)

    #             print("img#rrrrrrrrrrrrrrrrrrr",data)
    #             # qr_image = base64.b64encode(img.read())
    #             with open("new_code.png", "rb") as img_file:
    #                 my_string = base64.b64encode(img_file.read())
    #             print("ssssssssssssssss",my_string)


    #             ddts.qr_code = my_string