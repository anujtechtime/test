# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaaqalGrade(http.Controller):
#     @http.route('/almaaqal_grade/almaaqal_grade/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaaqal_grade/almaaqal_grade/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaaqal_grade.listing', {
#             'root': '/almaaqal_grade/almaaqal_grade',
#             'objects': http.request.env['almaaqal_grade.almaaqal_grade'].search([]),
#         })

#     @http.route('/almaaqal_grade/almaaqal_grade/objects/<model("almaaqal_grade.almaaqal_grade"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaaqal_grade.object', {
#             'object': obj
#         })
