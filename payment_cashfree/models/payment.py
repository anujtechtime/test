# -*- coding: utf-8 -*-
# Copyright 2018, 2020 Heliconia Solutions Pvt Ltd (https://heliconia.io)

import hashlib
import hmac
import base64

from werkzeug import urls

from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError, _partner_split_name, _partner_format_address
from odoo.tools.float_utils import float_compare
from odoo.tools import consteq, float_round

import logging
import requests
import json

_logger = logging.getLogger(__name__)


class PaymentAcquirerCashfree(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('cashfree', 'Cashfree')])
    cashfree_app_id = fields.Char(string='App id', required_if_provider='cashfree', groups='base.group_user')
    cashfree_secret_key = fields.Char(string='Secret Key', required_if_provider='cashfree', groups='base.group_user')
    cashfree_version = fields.Char(string="API Version")

    def get_api_header(self):
        return {
              'x-client-id': self.cashfree_app_id,
              'x-client-secret': self.cashfree_secret_key,
              'x-api-version': self.cashfree_version,
              'Content-Type': 'application/json'
            }

    def _get_cashfree_urls(self, state):
        """ Cashfree URLs"""
        if state == 'prod':
            return {'cashfree_form_url': 'https://api.cashfree.com/pg'}
        else:
            return {'cashfree_form_url': 'https://sandbox.cashfree.com/pg'}

    def _cashfree_get_customer(self, mobile, email, name):
        url = self.cashfree_get_form_action_url() + "/customers"
        payload = json.dumps({
            "customer_phone": mobile,
            "customer_email": email,
            "customer_name": name
        })
        headers = self.get_api_header()
        response = requests.request("POST", url, headers=headers, data=payload)
        result = json.loads(response.text)
        result['customer_uid'] = result.pop("customer_uid", "")
        result['customer_email'] = email
        result['customer_name'] = name
        return result

    def _cashfree_generate_sign(self, inout, postData):
        if inout not in ('in', 'out'):
            raise Exception("Type must be 'in' or 'out'")
        message = False
        if inout == 'out':
            sortedKeys = sorted(postData)
            signatureData = ""
            for key in sortedKeys:
                signatureData += key + str(postData[key]);
            message = signatureData.encode('utf-8')

        elif inout == 'in':
            signatureData = postData["orderId"] + postData["orderAmount"] + postData["referenceId"] + \
                            postData["txStatus"] + postData["paymentMode"] + postData["txMsg"] + postData["txTime"]
            message = signatureData.encode('utf-8')
        secret = self.cashfree_secret_key.encode('utf-8')
        signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
        return signature


    def cashfree_form_generate_values(self, values):
        self.ensure_one()
        base_url = self.get_base_url()
        cashfree_values = dict(appId=self.cashfree_app_id,
                               # orderId=values['reference'],
                               # orderId=int(values['reference']),
                               orderId=values.get('reference'),
                               orderAmount=values['amount'],
                               orderCurrency=values['currency'].name,
                               customerName=values.get('partner_name'),
                               customerEmail=values.get('partner_email'),
                               customerPhone=values.get('partner_phone'),
                               returnUrl=urls.url_join(base_url, '/payment/cashfree/return'),
                               notifyUrl=urls.url_join(base_url, '/payment/cashfree/notify'),
                               )
        cashfree_values['signature'] = self._cashfree_generate_sign('out', cashfree_values)
        values.update(cashfree_values)
        response = self.get_cashfree_return_url(values)
        values.update({
            "paymentSessionId": response.get("payment_session_id"),
            "paymentMode": "production" if self.state == 'prod' else "sandbox",
            "returnUrl": response.get("order_meta", {}).get("return_url", ""),
            "notifyUrl": response.get("order_meta", {}).get("notify_url", ""),
        })
        return values




    def cashfree_get_form_action_url(self):
        self.ensure_one()
        return self._get_cashfree_urls(self.state)['cashfree_form_url']

    def get_cashfree_return_url(self, values):
        self.ensure_one()
        url = self.cashfree_get_form_action_url() + "/orders"
        order_name = values.get('reference').split('-')[0]
        order_id = self.env['sale.order'].sudo().search([('name', '=', order_name)], limit=1)
        customer_details = {
            "customer_id": 'CU' + str(order_id.partner_id.id),
            "customer_name": order_id.partner_id.name,
            "customer_email": order_id.partner_id.email,
            "customer_phone": order_id.partner_id.phone,
        }
        data = {
            "customer_details": customer_details,
            "order_meta": {
                "return_url": values.get("returnUrl") + "?order_id=" + values.get("orderId"),
                "notify_url": values.get("notifyUrl") + "?order_id=" + values.get("orderId"),
            },
            "order_amount": values.get("amount"),
            "order_currency": "INR",
            "order_id": values.get("reference")
        }
        payload = json.dumps(data)
        headers = self.get_api_header()

        response = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(response.text)


class PaymentTransactionCashfree(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _cashfree_form_get_tx_from_data(self, data):
        print(":data", data)
        reference = data.get('order_id')
        if reference:
            tx = self.search([('reference', '=', reference)], limit=1)
            tx.provider_reference = 'cashfree'

        if not tx:
            raise ValidationError(
                "Cashfree: " + _("No transaction found matching reference %s.", reference)
            )

        return tx


    def _cashfree_form_get_invalid_parameters(self, data):
        invalid_parameters = []
        if self.acquirer_reference and data.get('order_id') != self.acquirer_reference:
            invalid_parameters.append(
                ('Transaction Id', data.get('order_id'), self.acquirer_reference))
        if float_compare(float(data.get('order_amount', '0.0')), self.amount, 2) != 0:
            invalid_parameters.append(
                ('order_amount', data.get('order_amount'), '%.2f' % self.amount))
        return invalid_parameters


    def _cashfree_form_validate(self, data):
        status = data.get('order_status')
        result = self.write({
            'acquirer_reference': data.get('referenceId'),
            'date': fields.Datetime.now(),
        })
        if status == 'PAID':
            self._set_transaction_done()
        elif status in ['FAILED', 'CANCELLED', 'FLAGGED']:
            self._set_transaction_cancel()
        else:
            self._set_transaction_pending()
        return result
