# -*- coding: utf-8 -*-
# from odoo import http


# class TechtimeStudentExcel(http.Controller):
#     @http.route('/techtime_student_excel/techtime_student_excel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/techtime_student_excel/techtime_student_excel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('techtime_student_excel.listing', {
#             'root': '/techtime_student_excel/techtime_student_excel',
#             'objects': http.request.env['techtime_student_excel.techtime_student_excel'].search([]),
#         })

#     @http.route('/techtime_student_excel/techtime_student_excel/objects/<model("techtime_student_excel.techtime_student_excel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('techtime_student_excel.object', {
#             'object': obj
#         })
