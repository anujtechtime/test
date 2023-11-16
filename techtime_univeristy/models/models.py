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

    # faculty = fields.Char("Faculty")
    # level = fields.Char("Level")
    # installment_no = fields.Integer("Installment No")
    # Discount = fields.Float("Discount %")
    partner_id = fields.Many2one(
        'res.partner', string='Student Name', readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True, change_default=True, index=True, tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    college_number = fields.Char("College Number", related="partner_id.college_number")
    student_no = fields.Char("Exam No.", related="partner_id.number_exam")
    Subject = fields.Selection([('morning','صباحي'),('afternoon','مسائي')], string="Shift")
    level = fields.Selection([('leve1','المرحلة الاولى'),('level2','المرحلة الثانية'),('level3','المرحلة الثالثة'),('level4','المرحلة الرابعة'),('level5','المرحلة الخامسة')], string="Level")
    college = fields.Many2one("faculty.faculty", string="College")
    department = fields.Many2one("department.department", string="Department")
    student = fields.Many2one("level.level", string="Student Type")
    year = fields.Many2one("year.year", string="Year")
    amount = fields.Char("مبلغ الدفع")
    # installment_no = fields.Float("Installment" ,related="level.installment") 

    # @api.model
    # def create(self, vals):
    #     result = super(SaleOrderField_user, self).create(vals)
    #     print("result##############",result)    
    #     print("result.college###########",result.college,result.department,result.student, result.year)
    #     installmet_dat = result.env["installment.details"].search([('college' , '=', result.college.id),("level","=",result.level),("Subject","=",result.Subject),('department','=',result.department.id),('Student','=',result.student.id),('year','=', result.year.id)],limit=1)
    #     print("result.id#$$$$$$$$$$$$$$$",installmet_dat)
    #     if installmet_dat:
    #         print("sale_installment_line_ids########",installmet_dat.sale_installment_line_ids.ids)
    #         # for datts in installmet_dat.sale_installment_line_ids:
    #         # result.sale_installment_line_ids = [(6, 0, installmet_dat.sale_installment_line_ids.ids)]
    #         result.installment_amount = installmet_dat.installment
    #         # result.payable_amount = installmet_dat.installment / installmet_dat.installment_number
    #         result.tenure_month = installmet_dat.installment_number
    #         result.second_payment_date = datetime.today().date()
    #         order_line = result.env['sale.order.line'].create({
    #             'product_id': 1,
    #             'price_unit': result.installment_amount,
    #             'product_uom': result.env.ref('uom.product_uom_unit').id,
    #             'product_uom_qty': 1,
    #             'order_id': result._origin.id,
    #             'name': 'sales order line',
    #         })
    #         # journal = result.env['account.move'].with_context(default_type='out_invoice')._get_default_journal()
    #         count = 0
    #         for i in installmet_dat.sale_installment_line_ids:
    #             # invoice_id = result.env['account.move'].create(invoice_vals)
    #             sale_installment = result.sale_installment_line_ids.create({
    #                 'number' : i.number,
    #                 'payment_date' : i.payment_date,
    #                 'amount_installment' : i.amount_installment,
    #                 'description': 'Installment Payment',
    #                 'sale_installment_id' : result.id,
    #                 # "invoice_id" : invoice_id.id
    #                 })
    #             count = count + 1

    #             # i.invoice_id = invoice_id.id
    #             # print("invoice_id##################",invoice_id)

    #             # account_invoice_line  = result.env['account.move.line'].with_context(
    #             #     check_move_validity=False).create({
    #             #     'name': self.order_line.product_id.name,
    #             #     'price_unit': self.payable_amount,
    #             #     'quantity': 1.0,
    #             #     'discount': 0.0,
    #             #     'journal_id': journal.id,
    #             #     'product_id': self.order_line.product_id.id,
    #             #     'analytic_account_id': self.analytic_account_id.id,
    #             #     'account_id': self.partner_invoice_id.property_account_receivable_id.id,
    #             #     'move_id': invoice_id.id,
    #             #     })
    #             # for order in self:
    #             #     order.order_line.update({
    #             #         'invoice_lines' : [(4, account_invoice_line.id)]
    #             #         })

    #     return result


    @api.onchange('year',"college","Subject","department","student","level")
    def _compute_level(self):
        print("self.college###########",self.college,self.department,self.student, self.year, self._origin)
        installmet_dat = self.env["installment.details"].search([('college' , '=', self.college.id),("level","=",self.level),("Subject","=",self.Subject),('department','=',self.department.id),('Student','=',self.student.id),('year','=', self.year.id)])
        print("self.id#$$$$$$$$$$$$$$$",installmet_dat)
        self.sale_installment_line_ids.unlink()
        invoice_past = self.env["account.move"].search([('invoice_origin', '=', self.name)])
        invoice_past.unlink()
        if installmet_dat and self._origin:
            for order in self.order_line:
                if order:
                    order.price_unit = self.installment_amount
            print("sale_installment_line_ids########",installmet_dat.sale_installment_line_ids.ids)
            # for datts in installmet_dat.sale_installment_line_ids:
            # self.sale_installment_line_ids = [(6, 0, installmet_dat.sale_installment_line_ids.ids)]
            self.installment_amount = installmet_dat.installment
            # self.payable_amount = installmet_dat.installment / installmet_dat.installment_number
            self.tenure_month = installmet_dat.installment_number
            self.second_payment_date = datetime.today().date()
            if not self.order_line:
                order_line = self.env['sale.order.line'].create({
                    'product_id': 1,
                    'price_unit': self.installment_amount,
                    'product_uom': self.env.ref('uom.product_uom_unit').id,
                    'product_uom_qty': 1,
                    'order_id': self._origin.id,
                    'name': 'sales order line',
                })
            # journal = self.env['account.move'].with_context(default_type='out_invoice')._get_default_journal()
            count = 0
            for i in installmet_dat.sale_installment_line_ids:
                # invoice_vals = {
                #     'ref': self.client_order_ref or '',
                #     'type': 'out_invoice',
                #     'narration': self.note,
                #     'invoice_date': self.second_payment_date,
                #     'invoice_date_due' : self.second_payment_date,
                #     'currency_id': self.pricelist_id.currency_id.id,
                #     'campaign_id': self.campaign_id.id,
                #     'medium_id': self.medium_id.id,
                #     'source_id': self.source_id.id,
                #     'invoice_user_id': self.user_id and self.user_id.id,
                #     'team_id': self.team_id.id,
                #     'partner_id': self.partner_invoice_id.id,
                #     'partner_shipping_id': self.partner_shipping_id.id,
                #     'invoice_partner_bank_id': self.company_id.partner_id.bank_ids[:1].id,
                #     'fiscal_position_id': self.fiscal_position_id.id or self.partner_invoice_id.property_account_position_id.id,
                #     'journal_id': journal.id,  # company comes from the journal
                #     'invoice_origin': self.name,
                #     'invoice_payment_term_id': self.payment_term_id.id,
                #     'invoice_payment_ref': self.reference,
                #     'transaction_ids': [(6, 0, self.transaction_ids.ids)],
                #     'invoice_line_ids': [(0, 0, {
                #         'name': self.order_line.product_id.name,
                #         'price_unit': i.amount_installment,
                #         'quantity': 1.0,
                #         'product_id': self.order_line.product_id.id,
                #         'product_uom_id': self.order_line.product_uom.id,
                #         # 'tax_ids': [(6, 0, self.order_line.tax_id.ids)],
                #         'sale_line_ids': [(6, 0, [order_line.id])],
                #         'analytic_tag_ids': [(6, 0, self.order_line.analytic_tag_ids.ids)],
                #         'analytic_account_id': self.analytic_account_id.id or False,
                #     })],
                #     'company_id': self.company_id.id,
                #     'sponsor' : self.sponsor.id,
                # } 

                sale_installment = self.sale_installment_line_ids.create({
                    'number' : count,
                    'payment_date' : i.payment_date,
                    'amount_installment' : i.amount_installment,
                    'description': 'Installment Payment',
                    'sale_installment_id' : self.id,
                    })
                count = count + 1

                # invoice_id = self.env['account.move'].create(invoice_vals)
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


class Payment_Data(models.Model):
    _inherit = 'account.payment'


    level = fields.Selection([('leve1','المرحلة الاولى'),('level2','المرحلة الثانية'),('level3','المرحلة الثالثة'),('level4','المرحلة الرابعة'),('level5','المرحلة الخامسة')], string="Level")
    college = fields.Many2one("faculty.faculty", string="College")
    student = fields.Many2one("level.level", string="Student Type")
    year = fields.Many2one("year.year", string="Year", related="partner_id.year")
    Subject = fields.Selection([('morning','صباحي'),('afternoon','مسائي')], string="Shift")
    department = fields.Many2one("department.department", string="Department")


    def post(self):
        """ Create the journal items for the payment and update the payment's state to 'posted'.
            A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
            and another in the destination reconcilable account (see _compute_destination_account_id).
            If invoice_ids is not empty, there will be one reconcilable move line per invoice to reconcile with.
            If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
        """
        AccountMove = self.env['account.move'].with_context(default_type='entry')
        for rec in self:

            if rec.state != 'draft':
                raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'posted' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].next_by_code(sequence_code, sequence_date=rec.payment_date)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            moves = AccountMove.create(rec._prepare_payment_moves())
            moves.filtered(lambda move: move.journal_id.post_at != 'bank_rec').post()

            # Update the state / move before performing any reconciliation.
            move_name = self._get_move_name_transfer_separator().join(moves.mapped('name'))
            rec.write({'state': 'posted', 'move_name': move_name})

            if rec.payment_type in ('inbound', 'outbound'):
                # ==== 'inbound' / 'outbound' ====
                if rec.invoice_ids:
                    (moves[0] + rec.invoice_ids).line_ids \
                        .filtered(lambda line: not line.reconciled and line.account_id == rec.destination_account_id and not (line.account_id == line.payment_id.writeoff_account_id and line.name == line.payment_id.writeoff_label))\
                        .reconcile()
            elif rec.payment_type == 'transfer':
                # ==== 'transfer' ====
                moves.mapped('line_ids')\
                    .filtered(lambda line: line.account_id == rec.company_id.transfer_account_id)\
                    .reconcile()
        print("AccountMove####################",rec.invoice_ids)
        # rec.invoice_ids.payment_id = self.id

        if self.invoice_ids.invoice_payment_state == 'paid':
            self.invoice_ids.action_view_payments()
        # print("selfhhhhhhhhhhhhhhhhhhhhhhhhhh",self)            

        # payment_data  = self.env["account.move"].search([("partner_id","=",self.partner_id.id),("state","=","posted"),("invoice_payment_state","=","not_paid"),("amount_total","=",self.amount)],limit=1, order='invoice_date asc')
        # payment_data.invoice_payment_ref = self.id
        # payment_data.payment_id = self.id
        # ddts = []
        # move_line = self.env["account.move.line"].search([("partner_id","=",self.partner_id.id),("parent_state","=","posted"),("full_reconcile_id","=",False),("debit","=",0)],order='id asc')
        # if move_line and payment_data:
        #     for ssnt in move_line:
        #         if "INV" not in ssnt.name:
        #             ddts.append(ssnt.id)
        #     payment_data.js_assign_outstanding_line(ssnt.id)
        return True



class AccountMove(models.Model):
    _inherit = 'account.move'


    level = fields.Selection([('leve1','المرحلة الاولى'),('level2','المرحلة الثانية'),('level3','المرحلة الثالثة'),('level4','المرحلة الرابعة'),('level5','المرحلة الخامسة')], string="Level")
    college = fields.Many2one("faculty.faculty", string="College")
    student = fields.Many2one("level.level", string="Student Type")
    Subject = fields.Selection([('morning','صباحي'),('afternoon','مسائي')], string="Shift")
    payment_id = fields.Many2one("account.payment", string="payment")
    year = fields.Many2one("year.year", string="Year",related="partner_id.year")

    def _check_reconcile_validity(self):
        # Empty self can happen if there is no line to check.
        if not self:
            return

        #Perform all checks on lines
        company_ids = set()
        all_accounts = []
        for line in self:
            company_ids.add(line.company_id.id)
            all_accounts.append(line.account_id)
            if line.reconciled:
                raise UserError(_('You are trying to reconcile some entries that are already reconciled.'))
        if len(company_ids) > 1:
            raise UserError(_('To reconcile the entries company should be the same for all entries.'))
        if len(set(all_accounts)) > 1:
            raise UserError(_('Entries are not from the same account.'))
        # if not (all_accounts[0].reconcile or all_accounts[0].internal_type == 'liquidity'):
        #     raise UserError(_('Account %s (%s) does not allow reconciliation. First change the configuration of this account to allow it.') % (all_accounts[0].name, all_accounts[0].code))



# class AccountMoveInstallment(models.Model):
#     _inherit = 'sale.installment'

#     invoice_status = fields.Selection([("draft","Draft"),("posted","Posted"),("cancel","Cancel")] , related="invoice_id.state") 

