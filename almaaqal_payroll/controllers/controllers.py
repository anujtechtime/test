# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaaqalPayroll(http.Controller):
#     @http.route('/almaaqal_payroll/almaaqal_payroll/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaaqal_payroll/almaaqal_payroll/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaaqal_payroll.listing', {
#             'root': '/almaaqal_payroll/almaaqal_payroll',
#             'objects': http.request.env['almaaqal_payroll.almaaqal_payroll'].search([]),
#         })

#     @http.route('/almaaqal_payroll/almaaqal_payroll/objects/<model("almaaqal_payroll.almaaqal_payroll"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaaqal_payroll.object', {
#             'object': obj
#         })
