# -*- coding: utf-8 -*-
# from odoo import http


# class BurjModule(http.Controller):
#     @http.route('/burj_module/burj_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/burj_module/burj_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('burj_module.listing', {
#             'root': '/burj_module/burj_module',
#             'objects': http.request.env['burj_module.burj_module'].search([]),
#         })

#     @http.route('/burj_module/burj_module/objects/<model("burj_module.burj_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('burj_module.object', {
#             'object': obj
#         })
