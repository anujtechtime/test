# -*- coding: utf-8 -*-
# from odoo import http


# class AlnasmiProductFields(http.Controller):
#     @http.route('/alnasmi_product_fields/alnasmi_product_fields/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/alnasmi_product_fields/alnasmi_product_fields/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('alnasmi_product_fields.listing', {
#             'root': '/alnasmi_product_fields/alnasmi_product_fields',
#             'objects': http.request.env['alnasmi_product_fields.alnasmi_product_fields'].search([]),
#         })

#     @http.route('/alnasmi_product_fields/alnasmi_product_fields/objects/<model("alnasmi_product_fields.alnasmi_product_fields"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('alnasmi_product_fields.object', {
#             'object': obj
#         })
