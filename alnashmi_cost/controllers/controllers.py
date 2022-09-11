# -*- coding: utf-8 -*-
# from odoo import http


# class AlnashmiCost(http.Controller):
#     @http.route('/alnashmi_cost/alnashmi_cost/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/alnashmi_cost/alnashmi_cost/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('alnashmi_cost.listing', {
#             'root': '/alnashmi_cost/alnashmi_cost',
#             'objects': http.request.env['alnashmi_cost.alnashmi_cost'].search([]),
#         })

#     @http.route('/alnashmi_cost/alnashmi_cost/objects/<model("alnashmi_cost.alnashmi_cost"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('alnashmi_cost.object', {
#             'object': obj
#         })
