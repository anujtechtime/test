# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaaqalReportAccount(http.Controller):
#     @http.route('/almaaqal_report_account/almaaqal_report_account/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaaqal_report_account/almaaqal_report_account/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaaqal_report_account.listing', {
#             'root': '/almaaqal_report_account/almaaqal_report_account',
#             'objects': http.request.env['almaaqal_report_account.almaaqal_report_account'].search([]),
#         })

#     @http.route('/almaaqal_report_account/almaaqal_report_account/objects/<model("almaaqal_report_account.almaaqal_report_account"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaaqal_report_account.object', {
#             'object': obj
#         })
