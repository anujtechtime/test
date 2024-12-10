# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaaqalRecordAccess(http.Controller):
#     @http.route('/almaaqal_record_access/almaaqal_record_access/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaaqal_record_access/almaaqal_record_access/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaaqal_record_access.listing', {
#             'root': '/almaaqal_record_access/almaaqal_record_access',
#             'objects': http.request.env['almaaqal_record_access.almaaqal_record_access'].search([]),
#         })

#     @http.route('/almaaqal_record_access/almaaqal_record_access/objects/<model("almaaqal_record_access.almaaqal_record_access"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaaqal_record_access.object', {
#             'object': obj
#         })
