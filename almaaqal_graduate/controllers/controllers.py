# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaaqalGraduate(http.Controller):
#     @http.route('/almaaqal_graduate/almaaqal_graduate/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaaqal_graduate/almaaqal_graduate/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaaqal_graduate.listing', {
#             'root': '/almaaqal_graduate/almaaqal_graduate',
#             'objects': http.request.env['almaaqal_graduate.almaaqal_graduate'].search([]),
#         })

#     @http.route('/almaaqal_graduate/almaaqal_graduate/objects/<model("almaaqal_graduate.almaaqal_graduate"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaaqal_graduate.object', {
#             'object': obj
#         })
