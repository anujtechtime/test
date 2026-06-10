# -*- coding: utf-8 -*-
# from odoo import http


# class NewFieldInvoice(http.Controller):
#     @http.route('/new_field_invoice/new_field_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/new_field_invoice/new_field_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('new_field_invoice.listing', {
#             'root': '/new_field_invoice/new_field_invoice',
#             'objects': http.request.env['new_field_invoice.new_field_invoice'].search([]),
#         })

#     @http.route('/new_field_invoice/new_field_invoice/objects/<model("new_field_invoice.new_field_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('new_field_invoice.object', {
#             'object': obj
#         })
