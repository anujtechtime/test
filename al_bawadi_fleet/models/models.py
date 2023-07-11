# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import qrcode
import base64
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO
from io import BytesIO
from datetime import date as date_n  
   



class SaleOrderField_user(models.Model):
    _inherit = 'account.move'

    receipt_number = fields.Integer("Receipt Number")
    car_number = fields.Char(string="Car Number")
    car_type = fields.Selection([('small','Small'),('large','Large')], string="Car Type")
    car_type_drop_down = fields.Selection([('container','container'),('refrigerator','refrigerator')], string="Large Car")
    in_date = fields.Datetime("In Date")
    out_date = fields.Datetime("Out Date")


    qr_code = fields.Binary("QR Code", attachment=True, store=True)

    amount_for_parking = fields.Monetary("Parking Amount", store=True, currency_field='currency_id')


    @api.onchange('out_date')
    def generate_out_date(self):  
        if self.in_date and self.out_date:
            self.amount_for_parking = 4000 * ((self.out_date - self.in_date).days + 1)
            print("self.amount_for_parking@@@@@@@@@@@@@@",self.amount_for_parking)



    @api.onchange('in_date')
    def generate_qr_code(self):
        if self.in_date:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data("In Time :" + str(self.in_date + relativedelta(hours=5.5)))
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            self.qr_code = qr_image