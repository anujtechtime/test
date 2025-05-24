# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaaqalEdit(http.Controller):
#     @http.route('/almaaqal_edit/almaaqal_edit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaaqal_edit/almaaqal_edit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaaqal_edit.listing', {
#             'root': '/almaaqal_edit/almaaqal_edit',
#             'objects': http.request.env['almaaqal_edit.almaaqal_edit'].search([]),
#         })

#     @http.route('/almaaqal_edit/almaaqal_edit/objects/<model("almaaqal_edit.almaaqal_edit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaaqal_edit.object', {
#             'object': obj
#         })
