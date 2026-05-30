
from odoo import http
from odoo.http import request

class PartnerAutocomplete(http.Controller):

    @http.route('/contact_autocomplete/search', type='json', auth='user')
    def partner_autocomplete(self, term):
        partners = request.env['res.partner'].sudo().search([
            ('name', 'ilike', term)
        ], limit=10)

        return [{'id': p.id, 'name': p.name} for p in partners]
