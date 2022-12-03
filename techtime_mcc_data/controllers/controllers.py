# -*- coding: utf-8 -*-
# from odoo import http


# class TechtimeMccData(http.Controller):
#     @http.route('/techtime_mcc_data/techtime_mcc_data/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/techtime_mcc_data/techtime_mcc_data/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('techtime_mcc_data.listing', {
#             'root': '/techtime_mcc_data/techtime_mcc_data',
#             'objects': http.request.env['techtime_mcc_data.techtime_mcc_data'].search([]),
#         })

#     @http.route('/techtime_mcc_data/techtime_mcc_data/objects/<model("techtime_mcc_data.techtime_mcc_data"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('techtime_mcc_data.object', {
#             'object': obj
#         })
