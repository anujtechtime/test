# -*- coding: utf-8 -*-
from odoo import http

# class TechtimeSale(http.Controller):
#     @http.route('/techtime_sale/techtime_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/techtime_sale/techtime_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('techtime_sale.listing', {
#             'root': '/techtime_sale/techtime_sale',
#             'objects': http.request.env['techtime_sale.techtime_sale'].search([]),
#         })

#     @http.route('/techtime_sale/techtime_sale/objects/<model("techtime_sale.techtime_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('techtime_sale.object', {
#             'object': obj
#         })