# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaqalTemplates(http.Controller):
#     @http.route('/almaqal_templates/almaqal_templates/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaqal_templates/almaqal_templates/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaqal_templates.listing', {
#             'root': '/almaqal_templates/almaqal_templates',
#             'objects': http.request.env['almaqal_templates.almaqal_templates'].search([]),
#         })

#     @http.route('/almaqal_templates/almaqal_templates/objects/<model("almaqal_templates.almaqal_templates"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaqal_templates.object', {
#             'object': obj
#         })
