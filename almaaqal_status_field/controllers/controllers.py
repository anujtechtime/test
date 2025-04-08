# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaaqalStatusField(http.Controller):
#     @http.route('/almaaqal_status_field/almaaqal_status_field/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaaqal_status_field/almaaqal_status_field/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaaqal_status_field.listing', {
#             'root': '/almaaqal_status_field/almaaqal_status_field',
#             'objects': http.request.env['almaaqal_status_field.almaaqal_status_field'].search([]),
#         })

#     @http.route('/almaaqal_status_field/almaaqal_status_field/objects/<model("almaaqal_status_field.almaaqal_status_field"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaaqal_status_field.object', {
#             'object': obj
#         })
