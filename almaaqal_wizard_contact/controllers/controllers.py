# -*- coding: utf-8 -*-
# from odoo import http


# class AlmaaqalWizardContact(http.Controller):
#     @http.route('/almaaqal_wizard_contact/almaaqal_wizard_contact/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almaaqal_wizard_contact/almaaqal_wizard_contact/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('almaaqal_wizard_contact.listing', {
#             'root': '/almaaqal_wizard_contact/almaaqal_wizard_contact',
#             'objects': http.request.env['almaaqal_wizard_contact.almaaqal_wizard_contact'].search([]),
#         })

#     @http.route('/almaaqal_wizard_contact/almaaqal_wizard_contact/objects/<model("almaaqal_wizard_contact.almaaqal_wizard_contact"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almaaqal_wizard_contact.object', {
#             'object': obj
#         })
