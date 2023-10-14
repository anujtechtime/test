# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaqalStudentDiscount(http.Controller):
#     @http.route('/almaqal_student_discount/almaqal_student_discount/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaqal_student_discount/almaqal_student_discount/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaqal_student_discount.listing', {
#             'root': '/almaqal_student_discount/almaqal_student_discount',
#             'objects': http.request.env['almaqal_student_discount.almaqal_student_discount'].search([]),
#         })

#     @http.route('/almaqal_student_discount/almaqal_student_discount/objects/<model("almaqal_student_discount.almaqal_student_discount"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaqal_student_discount.object', {
#             'object': obj
#         })
