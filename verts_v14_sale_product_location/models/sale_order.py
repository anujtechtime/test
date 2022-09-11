# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
from odoo.tools.misc import formatLang, format_date, get_lang

from datetime import date, timedelta
from itertools import groupby
from itertools import zip_longest
from hashlib import sha256
from json import dumps

import json
import re

#forbidden fields
INTEGRITY_HASH_MOVE_FIELDS = ('date', 'journal_id', 'company_id')
INTEGRITY_HASH_LINE_FIELDS = ('debit', 'credit', 'account_id', 'partner_id')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_stock_location_id = fields.Many2one("stock.location", string="Stock Location",domain="[('usage', '=', 'internal')]")
    qty_on_hand = fields.Float('On Hand', readonly=True, compute='_compute_qty')
    net_price = fields.Integer("Net Price")
    margin = fields.Char("Margin.%")
    total_on_hand = fields.Float(related="product_id.qty_available", string="Total On Hand")
    

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        res = super(SaleOrderLine, self)._compute_amount()
        if self.discount:
            self.net_price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        return res

    @api.depends('product_stock_location_id')
    def _compute_qty(self):
        for rec in self:
            qunatity = 0
            if rec.product_stock_location_id and rec.product_id:
                stock_quants = self.env['stock.quant'].search([
                    ('location_id', '=', rec.product_stock_location_id.id),
                    ('product_id', '=', rec.product_id.id)
                ])

                for quant in stock_quants:
                    qunatity += quant.quantity
            rec.qty_on_hand = qunatity

    @api.onchange('net_price')
    def _inverse_net_price(self):
        if self.price_unit > 0:
            self.discount = (self.price_unit - self.net_price) / self.price_unit * 100
        if self.net_price > 0 and self.price_unit > 0:        
            self.margin = (self.net_price - self.product_id.standard_price) /  self.net_price * 100



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ], string="Payment", default="cash")
    project = fields.Many2one("stock.location", string="Project")

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for orde in self.order_line:
            if orde.product_stock_location_id:
                print("orde@@@@@@@@@@@@@@@@@@@@@@@",orde.move_ids.move_line_ids.location_id)
                orde.move_ids.move_line_ids.location_id =  orde.product_stock_location_id.id   
        return res




class ProductOldRecord(models.TransientModel):
    _name = 'product.pastorder'
    _description = 'Product Past Record'


    product_tmpl_id = fields.Many2one('product.product', string='Product Template', required=True)  
    sale_price = fields.Integer("Sale price")
    cost_price = fields.Integer("Cost price")
    purchase_price = fields.Integer("Last Purchase Price")
    last_sale_price = fields.Integer("Last Sale Price")
    location_quant = fields.Many2many("stock.quant" , string="On Hand")


    @api.model
    def default_get(self, fields):
        res = super(ProductOldRecord, self).default_get(fields)
        # Sale price, cost price last purchase price and last sales price
        sale_order_line = self.env['sale.order.line'].search([('id','=',self.env.context.get('active_id'))],limit=1)
        location_n = self.env['stock.quant'].search([('product_id','=',sale_order_line.product_id.id)]).filtered(lambda line: line.location_id.usage == 'internal')
        location_ids = location_n.mapped('id')
        lastsale = False
        sale_order = self.env['sale.order'].search([('partner_id','=',sale_order_line.order_id.partner_id.id),('state','=','sale')],order='date_order desc')
        for lines in sale_order:
            if lines.order_line.filtered(lambda l: l.product_id == sale_order_line.product_id):
                lastsale = lines.order_line.filtered(lambda l: l.product_id == sale_order_line.product_id)
            break
        
        if lastsale:
            if 'last_sale_price' in fields:
                res['last_sale_price'] = lastsale.price_unit    
            if 'purchase_price' in fields:
                res['purchase_price'] = lastsale.price_unit        
        if 'sale_price' in fields:
            res['sale_price'] = sale_order_line.product_id.lst_price
        if 'location_quant' in fields:
            res['location_quant'] = [[ 6, 0, location_ids ]] 
        if 'cost_price' in fields:
            res['cost_price'] = sale_order_line.product_id.standard_price



        # product_tmpl_id = self.env['product.template']
        # if 'product_id' in fields:
        #     if self.env.context.get('default_product_id'):
        #         product_id = self.env['product.product'].browse(self.env.context['default_product_id'])
        #         product_tmpl_id = product_id.product_tmpl_id
        #         res['product_tmpl_id'] = product_id.product_tmpl_id.id
        #         res['product_id'] = product_id.id
        #     elif self.env.context.get('default_product_tmpl_id'):
        #         product_tmpl_id = self.env['product.template'].browse(self.env.context['default_product_tmpl_id'])
        #         res['product_tmpl_id'] = product_tmpl_id.id
        #         res['product_id'] = product_tmpl_id.product_variant_id.id
        #         if len(product_tmpl_id.product_variant_ids) > 1:
        #             res['product_has_variants'] = True
        # company = product_tmpl_id.company_id or self.env.company
        
        # if 'warehouse_id' in fields and 'warehouse_id' not in res:
        #     warehouse = self.env['stock.warehouse'].search([('company_id', '=', company.id)], limit=1)
        #     res['warehouse_id'] = warehouse.id
        # if 'date_planned' in fields:
        #     res['date_planned'] = datetime.datetime.now()
        return res  

class AccountMoveAdd(models.Model):
    _inherit = "account.move"


    def post(self):
        # `user_has_group` won't be bypassed by `sudo()` since it doesn't change the user anymore.
    #     Invoicing/Billing
    # - Purchase/User 
        # group_id = self.env.ref('account.group_account_invoice')
        # group_id.users = [(4, self.env.user.id)]
        
        for move in self:
            if not move.line_ids.filtered(lambda line: not line.display_type):
                raise UserError(_('You need to add a line before posting.'))
            if move.auto_post and move.date > fields.Date.today():
                date_msg = move.date.strftime(get_lang(self.env).date_format)
                raise UserError(_("This move is configured to be auto-posted on %s" % date_msg))

            if not move.partner_id:
                if move.is_sale_document():
                    raise UserError(_("The field 'Customer' is required, please complete it to validate the Customer Invoice."))
                elif move.is_purchase_document():
                    raise UserError(_("The field 'Vendor' is required, please complete it to validate the Vendor Bill."))

            if move.is_invoice(include_receipts=True) and float_compare(move.amount_total, 0.0, precision_rounding=move.currency_id.rounding) < 0:
                raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead. Use the action menu to transform it into a credit note or refund."))

            # Handle case when the invoice_date is not set. In that case, the invoice_date is set at today and then,
            # lines are recomputed accordingly.
            # /!\ 'check_move_validity' must be there since the dynamic lines will be recomputed outside the 'onchange'
            # environment.
            if not move.invoice_date and move.is_invoice(include_receipts=True):
                move.invoice_date = fields.Date.context_today(self)
                move.with_context(check_move_validity=False)._onchange_invoice_date()

            # When the accounting date is prior to the tax lock date, move it automatically to the next available date.
            # /!\ 'check_move_validity' must be there since the dynamic lines will be recomputed outside the 'onchange'
            # environment.
            if (move.company_id.tax_lock_date and move.date <= move.company_id.tax_lock_date) and (move.line_ids.tax_ids or move.line_ids.tag_ids):
                move.date = move.company_id.tax_lock_date + timedelta(days=1)
                move.with_context(check_move_validity=False)._onchange_currency()

        # Create the analytic lines in batch is faster as it leads to less cache invalidation.
        self.mapped('line_ids').create_analytic_lines()
        for move in self:
            if move.auto_post and move.date > fields.Date.today():
                raise UserError(_("This move is configured to be auto-posted on {}".format(move.date.strftime(get_lang(self.env).date_format))))

            move.message_subscribe([p.id for p in [move.partner_id] if p not in move.sudo().message_partner_ids])

            to_write = {'state': 'posted'}

            if move.name == '/':
                # Get the journal's sequence.
                sequence = move._get_sequence()
                if not sequence:
                    raise UserError(_('Please define a sequence on your journal.'))

                # Consume a new number.
                to_write['name'] = sequence.with_context(ir_sequence_date=move.date).next_by_id()

            move.write(to_write)

            # Compute 'ref' for 'out_invoice'.
            if move.type == 'out_invoice' and not move.invoice_payment_ref:
                to_write = {
                    'invoice_payment_ref': move._get_invoice_computed_reference(),
                    'line_ids': []
                }
                for line in move.line_ids.filtered(lambda line: line.account_id.user_type_id.type in ('receivable', 'payable')):
                    to_write['line_ids'].append((1, line.id, {'name': to_write['invoice_payment_ref']}))
                move.write(to_write)

            if move == move.company_id.account_opening_move_id and not move.company_id.account_bank_reconciliation_start:
                # For opening moves, we set the reconciliation date threshold
                # to the move's date if it wasn't already set (we don't want
                # to have to reconcile all the older payments -made before
                # installing Accounting- with bank statements)
                move.company_id.account_bank_reconciliation_start = move.date

        for move in self:
            if not move.partner_id: continue
            if move.type.startswith('out_'):
                move.partner_id._increase_rank('customer_rank')
            elif move.type.startswith('in_'):
                move.partner_id._increase_rank('supplier_rank')
            else:
                continue

        # Trigger action for paid invoices in amount is zero
        self.filtered(
            lambda m: m.is_invoice(include_receipts=True) and m.currency_id.is_zero(m.amount_total)
        ).action_invoice_paid()

        # Force balance check since nothing prevents another module to create an incorrect entry.
        # This is performed at the very end to avoid flushing fields before the whole processing.
        self._check_balanced()
        return True