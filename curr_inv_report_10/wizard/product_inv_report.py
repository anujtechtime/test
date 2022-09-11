# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError

class product_inv_report(models.TransientModel):
    _name = 'sale.order.product_inv_report'
    _description = 'Product Inventory Report'

    product = fields.Many2one('product.product', string='Product')

    def print_xls_report(self):
        product = 0
        if self.product:
            product = int(self.product[0])
        data = {}
        data = {'product': product}
        context = self._context.copy()
        context['report_data'] = data
        self = self.with_context(context)
        return self.env['report'].get_action(
            [], 'prod_inv.sale.order.xlsx', data=data)
