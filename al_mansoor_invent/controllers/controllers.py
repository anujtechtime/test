# -*- coding: utf-8 -*-
# from odoo import http


# class AlMansoorInvent(http.Controller):
#     @http.route('/al_mansoor_invent/al_mansoor_invent/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/al_mansoor_invent/al_mansoor_invent/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('al_mansoor_invent.listing', {
#             'root': '/al_mansoor_invent/al_mansoor_invent',
#             'objects': http.request.env['al_mansoor_invent.al_mansoor_invent'].search([]),
#         })

#     @http.route('/al_mansoor_invent/al_mansoor_invent/objects/<model("al_mansoor_invent.al_mansoor_invent"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('al_mansoor_invent.object', {
#             'object': obj
#         })
