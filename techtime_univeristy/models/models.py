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
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    student_no = fields.Char("Student No.", related="partner_id.number_exam")
    Subject = fields.Selection([('morning','Morning'),('afternoon','AfterNoon')], string="Shift")

    college = fields.Many2one("faculty.faculty", string="College")
    department = fields.Many2one("department.department", string="Department")
    student = fields.Many2one("level.level", string="Student Type")
    year = fields.Many2one("year.year", string="Year")
    # installment_no = fields.Float("Installment" ,related="level.installment") 

    @api.model
    def create(self, vals):
        result = super(SaleOrderField_user, self).create(vals)
        print("result##############",result)    
        print("result.college###########",result.college,result.department,result.student, result.year)
        installmet_dat = result.env["installment.details"].search([('college' , '=', result.college.id),("Subject","=",result.Subject),('department','=',result.department.id),('Student','=',result.student.id),('year','=', result.year.id)])
        print("result.id#$$$$$$$$$$$$$$$",installmet_dat)
        if installmet_dat:
            print("sale_installment_line_ids########",installmet_dat.sale_installment_line_ids.ids)
            # for datts in installmet_dat.sale_installment_line_ids:
            # result.sale_installment_line_ids = [(6, 0, installmet_dat.sale_installment_line_ids.ids)]
            result.installment_amount = installmet_dat.installment
            # result.payable_amount = installmet_dat.installment / installmet_dat.installment_number
            result.tenure_month = installmet_dat.installment_number
            result.second_payment_date = datetime.today().date()
            order_line = result.env['sale.order.line'].create({
                'product_id': 1,
                'price_unit': result.installment_amount,
                'product_uom': result.env.ref('uom.product_uom_unit').id,
                'product_uom_qty': 1,
                'order_id': result._origin.id,
                'name': 'sales order line',
            })
            # journal = result.env['account.move'].with_context(default_type='out_invoice')._get_default_journal()
            count = 0
            for i in installmet_dat.sale_installment_line_ids:
                # invoice_id = result.env['account.move'].create(invoice_vals)
                sale_installment = result.sale_installment_line_ids.create({
                    'number' : i.number,
                    'payment_date' : result.second_payment_date,
                    'amount_installment' : i.amount_installment,
                    'description': 'Installment Payment',
                    'sale_installment_id' : result.id,
                    # "invoice_id" : invoice_id.id
                    })
                count = count + 1

                # i.invoice_id = invoice_id.id
                # print("invoice_id##################",invoice_id)

                # account_invoice_line  = result.env['account.move.line'].with_context(
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

        return result


    @api.onchange('year',"college","Subject","department","student","year")
    def _compute_level(self):
        print("self.college###########",self.college,self.department,self.student, self.year, self._origin)
        installmet_dat = self.env["installment.details"].search([('college' , '=', self.college.id),("Subject","=",self.Subject),('department','=',self.department.id),('Student','=',self.student.id),('year','=', self.year.id)])
        print("self.id#$$$$$$$$$$$$$$$",installmet_dat)
        self.sale_installment_line_ids.unlink()
        invoice_past = self.env["account.move"].search([('invoice_origin', '=', self.name)])
        invoice_past.unlink()
        if installmet_dat and self._origin:
            for order in self.order_line:
                if order:
                    order.unlink()
            print("sale_installment_line_ids########",installmet_dat.sale_installment_line_ids.ids)
            # for datts in installmet_dat.sale_installment_line_ids:
            # self.sale_installment_line_ids = [(6, 0, installmet_dat.sale_installment_line_ids.ids)]
            self.installment_amount = installmet_dat.installment
            # self.payable_amount = installmet_dat.installment / installmet_dat.installment_number
            self.tenure_month = installmet_dat.installment_number
            self.second_payment_date = datetime.today().date()
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
                    'payment_date' : self.second_payment_date,
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

