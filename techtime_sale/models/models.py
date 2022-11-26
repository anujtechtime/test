# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.osv import expression
from dateutil.relativedelta import relativedelta
from odoo.tools import float_is_zero, float_compare



from werkzeug.urls import url_encode


class SaleOrderField_user(models.Model):
    _inherit = 'sale.order'

    sponsor = fields.Many2one('res.partner' , string="Sponsor")
    downpayment = fields.Float('Down Payment', copy=True)
    installment_amount = fields.Float('Installment Amount', copy=True)
    second_payment_date = fields.Date('Second Payment Date')
    payable_amount = fields.Float('Payable Amount', copy=True)
    tenure_month = fields.Integer('Tenure (months)', default=1)
    sale_installment_line_ids = fields.One2many('sale.installment', 'sale_installment_id', string='Membership Lines', copy=True)


    def action_installment_invoice(self):
        if self.sale_installment_line_ids:
            for ddtss in self.sale_installment_line_ids:
                journal = self.env['account.move'].with_context(default_type='out_invoice')._get_default_journal()
                count = 0
                invoice_vals = {
                    'ref': self.client_order_ref or '',
                    'type': 'out_invoice',
                    'narration': self.note,
                    'invoice_date': self.second_payment_date,
                    'invoice_date_due' : ddtss.payment_date,
                    'currency_id': self.pricelist_id.currency_id.id,
                    'campaign_id': self.campaign_id.id,
                    'medium_id': self.medium_id.id,
                    'source_id': self.source_id.id,
                    'invoice_user_id': self.user_id and self.user_id.id,
                    'team_id': self.team_id.id,
                    'partner_id': self.partner_invoice_id.id,
                    'partner_shipping_id': self.partner_shipping_id.id,
                    'invoice_partner_bank_id': self.company_id.partner_id.bank_ids[:1].id,
                    'fiscal_position_id': self.fiscal_position_id.id or self.partner_invoice_id.property_account_position_id.id,
                    'journal_id': journal.id,  # company comes from the journal
                    'invoice_origin': self.name,
                    'invoice_payment_term_id': self.payment_term_id.id,
                    'invoice_payment_ref': self.reference,
                    'transaction_ids': [(6, 0, self.transaction_ids.ids)],
                    'invoice_line_ids': [(0, 0, {
                        'name': self.order_line.product_id.name,
                        'price_unit': ddtss.amount_installment,
                        'quantity': 1.0,
                        'product_id': self.order_line.product_id.id,
                        'product_uom_id': self.order_line.product_uom.id,
                        # 'tax_ids': [(6, 0, self.order_line.tax_id.ids)],
                        'sale_line_ids': [(6, 0, [self.order_line.id])],
                        'analytic_tag_ids': [(6, 0, self.order_line.analytic_tag_ids.ids)],
                        'analytic_account_id': self.analytic_account_id.id or False,
                    })],
                    'company_id': self.company_id.id,
                    'sponsor' : self.sponsor.id,
                } 
                count = count + 1

                invoice_id = self.env['account.move'].create(invoice_vals)
                invoice_id.action_post()
                # i.invoice_id = invoice_id.id
                # print("invoice_id##############",invoice_id)

                # account_invoice_line  = self.env['account.move.line'].with_context(
                #     check_move_validity=False).create({
                #     'name': self.order_line.product_id.name,
                #     'price_unit': self.payable_amount,
                #     'quantity': 1.0,
                #     'discount': 0.0,
                #     'journal_id': journal.id,
                #     'product_id': self.order_line.product_id.id,
                #     'analytic_account_id': self.analytic_account_id.id,
                #     'account_id': self.partner_invoice_id.property_account_receivable_id.id,
                #     'move_id': invoice_id.id,
                #     })
                # for order in self:
                #     order.order_line.update({
                #         'invoice_lines' : [(4, account_invoice_line.id)]
                #         })

                account_install_line = self.env['account.installment'].create({
                    'number' : ddtss.number,
                    'payment_date' : ddtss.payment_date,
                    'amount_installment' : ddtss.amount_installment,
                    'description': 'Down Payment',
                    'sale_order_id' : ddtss.id,
                    'account_installment_id' : invoice_id.id
                    })

                invoice_id.update({
                    'account_installment_line_ids' : [(6, 0, account_install_line.ids)],
                    })
                ddtss.write({
                    "invoice_id" : invoice_id.id,
                })
        return True

    @api.onchange('downpayment')
    def _compute_downpayment(self):
        self.installment_amount = self.amount_total - self.downpayment
        if self.tenure_month > 0:
            self.payable_amount = self.installment_amount / self.tenure_month
        else:
            self.payable_amount = 0  

    @api.onchange('tenure_month')
    def _compute_tenure_month(self):
        if self.tenure_month > 0:
            self.payable_amount = self.installment_amount / self.tenure_month
        else:
            self.payable_amount = 0
                  

class ResPartnerFielduser(models.Model):
    _inherit = 'res.partner'

    employee_number = fields.Char('Employee number')
                  

class AccountInvoiceField_user(models.Model):
    _inherit = 'account.move'

    sponsor = fields.Many2one('res.partner' , string="Sponsor") 
    account_installment_line_ids = fields.One2many('account.installment', 'account_installment_id', string='Membership Lines', copy=True)   


    def action_post(self):
        if self.filtered(lambda x: x.journal_id.post_at == 'bank_rec').mapped('line_ids.payment_id').filtered(lambda x: x.state != 'reconciled'):
            raise UserError(_("A payment journal entry generated in a journal configured to post entries only when payments are reconciled with a bank statement cannot be manually posted. Those will be posted automatically after performing the bank reconciliation."))
        if self.env.context.get('default_type'):
            context = dict(self.env.context)
            del context['default_type']
            self = self.with_context(check_move_validity=False)
        self.account_installment_line_ids.sale_order_id.update({
            'status' : 'posted',
            })
        self.account_installment_line_ids.update({
            'status' : 'paid',
            })
        return self.post()
        
    @api.depends(
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state')
    def _compute_amount(self):
        invoice_ids = [move.id for move in self if move.id and move.is_invoice(include_receipts=True)]
        self.env['account.payment'].flush(['state'])
        if invoice_ids:
            self._cr.execute(
                '''
                    SELECT move.id
                    FROM account_move move
                    JOIN account_move_line line ON line.move_id = move.id
                    JOIN account_partial_reconcile part ON part.debit_move_id = line.id OR part.credit_move_id = line.id
                    JOIN account_move_line rec_line ON
                        (rec_line.id = part.debit_move_id AND line.id = part.credit_move_id)
                    JOIN account_payment payment ON payment.id = rec_line.payment_id
                    JOIN account_journal journal ON journal.id = rec_line.journal_id
                    WHERE payment.state IN ('posted', 'sent')
                    AND journal.post_at = 'bank_rec'
                    AND move.id IN %s
                UNION
                    SELECT move.id
                    FROM account_move move
                    JOIN account_move_line line ON line.move_id = move.id
                    JOIN account_partial_reconcile part ON part.debit_move_id = line.id OR part.credit_move_id = line.id
                    JOIN account_move_line rec_line ON
                        (rec_line.id = part.credit_move_id AND line.id = part.debit_move_id)
                    JOIN account_payment payment ON payment.id = rec_line.payment_id
                    JOIN account_journal journal ON journal.id = rec_line.journal_id
                    WHERE payment.state IN ('posted', 'sent')
                    AND journal.post_at = 'bank_rec'
                    AND move.id IN %s
                ''', [tuple(invoice_ids), tuple(invoice_ids)]
            )
            in_payment_set = set(res[0] for res in self._cr.fetchall())
        else:
            in_payment_set = {}

        for move in self:
            total_untaxed = 0.0
            total_untaxed_currency = 0.0
            total_tax = 0.0
            total_tax_currency = 0.0
            total_residual = 0.0
            total_residual_currency = 0.0
            total = 0.0
            total_currency = 0.0
            currencies = set()

            for line in move.line_ids:
                if line.currency_id:
                    currencies.add(line.currency_id)

                if move.is_invoice(include_receipts=True):
                    # === Invoices ===

                    if not line.exclude_from_invoice_tab:
                        # Untaxed amount.
                        total_untaxed += line.balance
                        total_untaxed_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.tax_line_id:
                        # Tax amount.
                        total_tax += line.balance
                        total_tax_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.account_id.user_type_id.type in ('receivable', 'payable'):
                        # Residual amount.
                        total_residual += line.amount_residual
                        total_residual_currency += line.amount_residual_currency
                else:
                    # === Miscellaneous journal entry ===
                    if line.debit:
                        total += line.balance
                        total_currency += line.amount_currency

            if move.type == 'entry' or move.is_outbound():
                sign = 1
            else:
                sign = -1
            move.amount_untaxed = sign * (total_untaxed_currency if len(currencies) == 1 else total_untaxed)
            move.amount_tax = sign * (total_tax_currency if len(currencies) == 1 else total_tax)
            move.amount_total = sign * (total_currency if len(currencies) == 1 else total)
            move.amount_residual = -sign * (total_residual_currency if len(currencies) == 1 else total_residual)
            move.amount_untaxed_signed = -total_untaxed
            move.amount_tax_signed = -total_tax
            move.amount_total_signed = abs(total) if move.type == 'entry' else -total
            move.amount_residual_signed = total_residual

            currency = len(currencies) == 1 and currencies.pop() or move.company_id.currency_id
            is_paid = currency and currency.is_zero(move.amount_residual) or not move.amount_residual

            # Compute 'invoice_payment_state'.
            if move.type == 'entry':
                move.invoice_payment_state = False
            elif move.state == 'posted' and is_paid:
                if move.id in in_payment_set:
                    move.invoice_payment_state = 'in_payment'
                else:
                    move.invoice_payment_state = 'paid'
                    self.account_installment_line_ids.sale_order_id.update({
                        'status' : 'paid',
                        })
                    self.account_installment_line_ids.update({
                        'status' : 'paid',
                        })
            else:
                move.invoice_payment_state = 'not_paid'


class SaleMembership(models.Model):
    _name = 'sale.installment'
    _description = "Sale Installment"

    sale_installment_id = fields.Many2one("sale.order", string="Installment")
    college_installment_id = fields.Many2one("installment.details", string="Installment")
    invoice_id = fields.Many2one('account.move',string="Invoice")
    payment_status = fields.Selection([
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid'),
        ],related="invoice_id.invoice_payment_state", string="Payment Status")
    number = fields.Integer("#No")
    payment_date = fields.Date("Payment Date")
    amount_installment = fields.Float("Amount")
    description = fields.Char("Description")
    status = fields.Selection([
        ('draft', 'DRAFT'),
        ('posted', 'Posted'),
        ('paid', 'Paid'),
        ('cancel', 'Cancel'),
        ], string='Status', readonly=True, copy=False, default='draft')


class SaleMembershipAccount(models.Model):
    _name = 'account.installment'
    _description = "Account Installment"

    account_installment_id = fields.Many2one("account.move", string="Installment")
    sale_order_id = fields.Many2one("sale.installment", string="Sale Order")
    number = fields.Integer("#No")
    payment_date = fields.Date("Payment Date")
    amount_installment = fields.Float("Amount")
    description = fields.Char("Description")
    Pay = fields.Boolean("Pay")
    status = fields.Selection([
        ('draft', 'DRAFT'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancel', 'Cancel'),
        ], string='Status', readonly=True, copy=False, default='draft')    