# -*- coding: utf-8 -*-
# from odoo import http


# class TechtimeUniveristy(http.Controller):
#     @http.route('/techtime_univeristy/techtime_univeristy/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/techtime_univeristy/techtime_univeristy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('techtime_univeristy.listing', {
#             'root': '/techtime_univeristy/techtime_univeristy',
#             'objects': http.request.env['techtime_univeristy.techtime_univeristy'].search([]),
#         })

#     @http.route('/techtime_univeristy/techtime_univeristy/objects/<model("techtime_univeristy.techtime_univeristy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('techtime_univeristy.object', {
#             'object': obj
#         })
