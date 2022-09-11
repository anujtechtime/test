# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class curr_inv_report(models.TransientModel):
    _name = 'sale.order.curr_inv_report'
    _description = 'Current Inventory Valuation Report'

    is_stock_move = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Show Stock Move", default="no")
    product = fields.Many2one('product.product', string='Product')
    company_id = fields.Many2one(comodel_name='res.company', string='Company')

    def print_xls_report(self):
        product = 0
        if self.product:
            product = int(self.product[0])
        data = {}
        data = {'is_stock_move': self.is_stock_move, 'product': product}
        context = self._context.copy()
        context['report_data'] = data
        self = self.with_context(context)
        return self.env['report'].get_action(
            [], 'cur_inv.sale.order.xlsx', data=data)

    def print_pdf_report(self):
        product = 0
        if self.product:
            product = int(self.product[0])
        data = {}
        data = {'is_stock_move': self.is_stock_move, 'product': product}
        return self.env.ref('curr_inv_report_10.record_id_sale_order_curr_inv_report').report_action([],data=data)
