# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaaqalHall(http.Controller):
#     @http.route('/almaaqal_hall/almaaqal_hall/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaaqal_hall/almaaqal_hall/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaaqal_hall.listing', {
#             'root': '/almaaqal_hall/almaaqal_hall',
#             'objects': http.request.env['almaaqal_hall.almaaqal_hall'].search([]),
#         })

#     @http.route('/almaaqal_hall/almaaqal_hall/objects/<model("almaaqal_hall.almaaqal_hall"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaaqal_hall.object', {
#             'object': obj
#         })
