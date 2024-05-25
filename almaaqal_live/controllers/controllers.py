# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaaqalLive(http.Controller):
#     @http.route('/almaaqal_live/almaaqal_live/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaaqal_live/almaaqal_live/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaaqal_live.listing', {
#             'root': '/almaaqal_live/almaaqal_live',
#             'objects': http.request.env['almaaqal_live.almaaqal_live'].search([]),
#         })

#     @http.route('/almaaqal_live/almaaqal_live/objects/<model("almaaqal_live.almaaqal_live"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaaqal_live.object', {
#             'object': obj
#         })
