# -*- coding: utf-8 -*-
# from odoo import http


# class TechtimeDepartment(http.Controller):
#     @http.route('/techtime_department/techtime_department/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/techtime_department/techtime_department/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('techtime_department.listing', {
#             'root': '/techtime_department/techtime_department',
#             'objects': http.request.env['techtime_department.techtime_department'].search([]),
#         })

#     @http.route('/techtime_department/techtime_department/objects/<model("techtime_department.techtime_department"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('techtime_department.object', {
#             'object': obj
#         })
