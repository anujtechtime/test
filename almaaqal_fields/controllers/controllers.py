# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaaqalFields(http.Controller):
#     @http.route('/almaaqal_fields/almaaqal_fields/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaaqal_fields/almaaqal_fields/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaaqal_fields.listing', {
#             'root': '/almaaqal_fields/almaaqal_fields',
#             'objects': http.request.env['almaaqal_fields.almaaqal_fields'].search([]),
#         })

#     @http.route('/almaaqal_fields/almaaqal_fields/objects/<model("almaaqal_fields.almaaqal_fields"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaaqal_fields.object', {
#             'object': obj
#         })
