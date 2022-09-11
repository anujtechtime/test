# -*- coding: utf-8 -*-
# from odoo import http


# class Ifxs(http.Controller):
#     @http.route('/ifxs/ifxs/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ifxs/ifxs/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ifxs.listing', {
#             'root': '/ifxs/ifxs',
#             'objects': http.request.env['ifxs.ifxs'].search([]),
#         })

#     @http.route('/ifxs/ifxs/objects/<model("ifxs.ifxs"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ifxs.object', {
#             'object': obj
#         })
