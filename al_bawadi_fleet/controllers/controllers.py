# -*- coding: utf-8 -*-
# from odoo import http


# class AlBawadiFleet(http.Controller):
#     @http.route('/al_bawadi_fleet/al_bawadi_fleet/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/al_bawadi_fleet/al_bawadi_fleet/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('al_bawadi_fleet.listing', {
#             'root': '/al_bawadi_fleet/al_bawadi_fleet',
#             'objects': http.request.env['al_bawadi_fleet.al_bawadi_fleet'].search([]),
#         })

#     @http.route('/al_bawadi_fleet/al_bawadi_fleet/objects/<model("al_bawadi_fleet.al_bawadi_fleet"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('al_bawadi_fleet.object', {
#             'object': obj
#         })
