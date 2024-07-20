# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaaqalCertificate(http.Controller):
#     @http.route('/almaaqal_certificate/almaaqal_certificate/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaaqal_certificate/almaaqal_certificate/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaaqal_certificate.listing', {
#             'root': '/almaaqal_certificate/almaaqal_certificate',
#             'objects': http.request.env['almaaqal_certificate.almaaqal_certificate'].search([]),
#         })

#     @http.route('/almaaqal_certificate/almaaqal_certificate/objects/<model("almaaqal_certificate.almaaqal_certificate"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaaqal_certificate.object', {
#             'object': obj
#         })
