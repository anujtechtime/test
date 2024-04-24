# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaaqalTrialBalance(http.Controller):
#     @http.route('/almaaqal_trial_balance/almaaqal_trial_balance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaaqal_trial_balance/almaaqal_trial_balance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaaqal_trial_balance.listing', {
#             'root': '/almaaqal_trial_balance/almaaqal_trial_balance',
#             'objects': http.request.env['almaaqal_trial_balance.almaaqal_trial_balance'].search([]),
#         })

#     @http.route('/almaaqal_trial_balance/almaaqal_trial_balance/objects/<model("almaaqal_trial_balance.almaaqal_trial_balance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaaqal_trial_balance.object', {
#             'object': obj
#         })
