# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaaqalTemplate(http.Controller):
#     @http.route('/almaaqal_template/almaaqal_template/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaaqal_template/almaaqal_template/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaaqal_template.listing', {
#             'root': '/almaaqal_template/almaaqal_template',
#             'objects': http.request.env['almaaqal_template.almaaqal_template'].search([]),
#         })

#     @http.route('/almaaqal_template/almaaqal_template/objects/<model("almaaqal_template.almaaqal_template"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaaqal_template.object', {
#             'object': obj
#         })
