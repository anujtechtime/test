# -*- coding: utf-8 -*-
# from odoo import http


# class TechtimeTechtimeModule(http.Controller):
#     @http.route('/techtime_techtime_module/techtime_techtime_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/techtime_techtime_module/techtime_techtime_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('techtime_techtime_module.listing', {
#             'root': '/techtime_techtime_module/techtime_techtime_module',
#             'objects': http.request.env['techtime_techtime_module.techtime_techtime_module'].search([]),
#         })

#     @http.route('/techtime_techtime_module/techtime_techtime_module/objects/<model("techtime_techtime_module.techtime_techtime_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('techtime_techtime_module.object', {
#             'object': obj
#         })
