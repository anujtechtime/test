# -*- coding: utf-8 -*-
# from odoo import http


# class NewFieldInstallment(http.Controller):
#     @http.route('/new_field_installment/new_field_installment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/new_field_installment/new_field_installment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('new_field_installment.listing', {
#             'root': '/new_field_installment/new_field_installment',
#             'objects': http.request.env['new_field_installment.new_field_installment'].search([]),
#         })

#     @http.route('/new_field_installment/new_field_installment/objects/<model("new_field_installment.new_field_installment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('new_field_installment.object', {
#             'object': obj
#         })
