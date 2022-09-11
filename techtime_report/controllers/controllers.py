# -*- coding: utf-8 -*-
# from odoo import http


# class TechtimeReport(http.Controller):
#     @http.route('/techtime_report/techtime_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/techtime_report/techtime_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('techtime_report.listing', {
#             'root': '/techtime_report/techtime_report',
#             'objects': http.request.env['techtime_report.techtime_report'].search([]),
#         })

#     @http.route('/techtime_report/techtime_report/objects/<model("techtime_report.techtime_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('techtime_report.object', {
#             'object': obj
#         })
