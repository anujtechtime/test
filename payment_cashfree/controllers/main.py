# -*- coding: utf-8 -*-
# Copyright 2018, 2020 Heliconia Solutions Pvt Ltd (https://heliconia.io)

import logging
import pprint
import werkzeug
import requests
import json

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class CashfreeController(http.Controller):

    @http.route(['/payment/cashfree/return', '/payment/cashfree/cancel', '/payment/cashfree/error',
                 '/payment/cashfree/notify'], type='http', auth='public', csrf=False)
    def cashfree_return(self, **post):
        """ Cashfree."""
        acquirer_id = request.env.ref('payment_cashfree.payment_acquirer_cashfree').sudo()
        if acquirer_id and post.get('order_id'):
            header = acquirer_id.get_api_header()
            url = acquirer_id.cashfree_get_form_action_url()
            order_url = url + '/orders/' + post.get('order_id')
            response = requests.post(order_url, headers=header)
            if response.status_code == 200:
                response_val = json.loads(response.text)
                _logger.info(
                    'Cashfree: entering form_feedback with post data %s', pprint.pformat(response_val))
                if post:
                    request.env['payment.transaction'].sudo().form_feedback(response_val, 'cashfree')
        return werkzeug.utils.redirect('/payment/process')


# import logging
# import pprint
# import werkzeug
# import requests
# import json
#
# from odoo import http
# from odoo.http import request
#
# _logger = logging.getLogger(__name__)
#
# class CashfreeController(http.Controller):
#
#     @http.route(['/payment/cashfree/return', '/payment/cashfree/cancel', '/payment/cashfree/error',
#                  '/payment/cashfree/notify'], type='http', auth='public', csrf=False)
#     def cashfree_return(self, **post):
#         """Handle Cashfree return."""
#         acquirer_id = request.env.ref('payment_cashfree.payment_acquirer_cashfree').sudo()
#         if acquirer_id and post.get('order_id'):
#             try:
#                 header = acquirer_id.get_api_header()
#                 url = acquirer_id.cashfree_get_form_action_url()
#                 order_url = url + '/orders/' + post.get('order_id')
#                 response = requests.post(order_url, headers=header)
#                 response.raise_for_status()  # Raise error for non-200 responses
#                 response_val = response.json()
#                 _logger.info(
#                     'Cashfree: entering form_feedback with post data %s', pprint.pformat(response_val))
#                 if post:
#                     request.env['payment.transaction'].sudo().form_feedback(response_val, 'cashfree')
#             except requests.RequestException as e:
#                 _logger.error('Error making request to Cashfree API: %s', e)
#                 # Handle error response or redirect to an error page
#         return werkzeug.utils.redirect('/payment/process')
