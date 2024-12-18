# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaaqalStudentUnpaid(http.Controller):
#     @http.route('/almaaqal_student_unpaid/almaaqal_student_unpaid/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaaqal_student_unpaid/almaaqal_student_unpaid/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaaqal_student_unpaid.listing', {
#             'root': '/almaaqal_student_unpaid/almaaqal_student_unpaid',
#             'objects': http.request.env['almaaqal_student_unpaid.almaaqal_student_unpaid'].search([]),
#         })

#     @http.route('/almaaqal_student_unpaid/almaaqal_student_unpaid/objects/<model("almaaqal_student_unpaid.almaaqal_student_unpaid"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaaqal_student_unpaid.object', {
#             'object': obj
#         })
