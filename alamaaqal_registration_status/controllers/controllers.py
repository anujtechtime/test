# -*- coding: utf-8 -*-
# from odoo import http


# class AlamaaqalRegistrationStatus(http.Controller):
#     @http.route('/alamaaqal_registration_status/alamaaqal_registration_status/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/alamaaqal_registration_status/alamaaqal_registration_status/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('alamaaqal_registration_status.listing', {
#             'root': '/alamaaqal_registration_status/alamaaqal_registration_status',
#             'objects': http.request.env['alamaaqal_registration_status.alamaaqal_registration_status'].search([]),
#         })

#     @http.route('/alamaaqal_registration_status/alamaaqal_registration_status/objects/<model("alamaaqal_registration_status.alamaaqal_registration_status"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('alamaaqal_registration_status.object', {
#             'object': obj
#         })
