# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaaqalRequestTransfering(http.Controller):
#     @http.route('/almaaqal_request_transfering/almaaqal_request_transfering/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaaqal_request_transfering/almaaqal_request_transfering/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaaqal_request_transfering.listing', {
#             'root': '/almaaqal_request_transfering/almaaqal_request_transfering',
#             'objects': http.request.env['almaaqal_request_transfering.almaaqal_request_transfering'].search([]),
#         })

#     @http.route('/almaaqal_request_transfering/almaaqal_request_transfering/objects/<model("almaaqal_request_transfering.almaaqal_request_transfering"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaaqal_request_transfering.object', {
#             'object': obj
#         })
