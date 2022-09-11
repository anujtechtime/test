# -*- coding: utf-8 -*-
# from odoo import http


# class TechtimePayrollExcel(http.Controller):
#     @http.route('/techtime_payroll_excel/techtime_payroll_excel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/techtime_payroll_excel/techtime_payroll_excel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('techtime_payroll_excel.listing', {
#             'root': '/techtime_payroll_excel/techtime_payroll_excel',
#             'objects': http.request.env['techtime_payroll_excel.techtime_payroll_excel'].search([]),
#         })

#     @http.route('/techtime_payroll_excel/techtime_payroll_excel/objects/<model("techtime_payroll_excel.techtime_payroll_excel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('techtime_payroll_excel.object', {
#             'object': obj
#         })
