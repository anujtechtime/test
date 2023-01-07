# -*- coding: utf-8 -*-
# from odoo import http


# class MccTechtimePayment(http.Controller):
#     @http.route('/mcc_techtime_payment/mcc_techtime_payment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mcc_techtime_payment/mcc_techtime_payment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mcc_techtime_payment.listing', {
#             'root': '/mcc_techtime_payment/mcc_techtime_payment',
#             'objects': http.request.env['mcc_techtime_payment.mcc_techtime_payment'].search([]),
#         })

#     @http.route('/mcc_techtime_payment/mcc_techtime_payment/objects/<model("mcc_techtime_payment.mcc_techtime_payment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mcc_techtime_payment.object', {
#             'object': obj
#         })
