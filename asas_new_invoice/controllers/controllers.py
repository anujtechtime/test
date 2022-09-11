# -*- coding: utf-8 -*-
# from odoo import http


# class AsasNewInvoice(http.Controller):
#     @http.route('/asas_new_invoice/asas_new_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asas_new_invoice/asas_new_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asas_new_invoice.listing', {
#             'root': '/asas_new_invoice/asas_new_invoice',
#             'objects': http.request.env['asas_new_invoice.asas_new_invoice'].search([]),
#         })

#     @http.route('/asas_new_invoice/asas_new_invoice/objects/<model("asas_new_invoice.asas_new_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asas_new_invoice.object', {
#             'object': obj
#         })
