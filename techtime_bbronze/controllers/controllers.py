# -*- coding: utf-8 -*-
# from odoo import http


# class TechtimeBbronze(http.Controller):
#     @http.route('/techtime_bbronze/techtime_bbronze/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/techtime_bbronze/techtime_bbronze/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('techtime_bbronze.listing', {
#             'root': '/techtime_bbronze/techtime_bbronze',
#             'objects': http.request.env['techtime_bbronze.techtime_bbronze'].search([]),
#         })

#     @http.route('/techtime_bbronze/techtime_bbronze/objects/<model("techtime_bbronze.techtime_bbronze"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('techtime_bbronze.object', {
#             'object': obj
#         })
