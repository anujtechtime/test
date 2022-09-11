# -*- coding: utf-8 -*-

from odoo import models, fields, api


class techtime_report(models.Model):
    _name = 'techtime_report.techtime_report'
    _description = 'techtime_report.techtime_report'

    name = fields.Char()
    menuitem = fields.Many2one("ir.ui.menu")
    menuitem_url = fields.Char()
    sales = fields.Boolean("sales")
    purchase = fields.Boolean("purchase")
    inventory = fields.Boolean("inventory")
    accounting = fields.Boolean("accounting")
    pos = fields.Boolean("pos")
    logo = fields.Binary("logo")


    @api.onchange('menuitem')
    def _onchange_menuitem(self):
        self.menuitem_url = '#menu_id=%s' % str(self.menuitem.id)

    def action_open_url(self):
        return {  'name'     : 'Go to website',
                  'res_model': 'ir.actions.act_url',
                  'type'     : 'ir.actions.act_url',
                  'target'   : 'self',
                  'url'      : self.menuitem_url
               }    


class SaleOrder(models.Model):
    _inherit = "sale.order"


    def _action_confirm(self):
        """ Implementation of additionnal mecanism of Sales Order confirmation.
            This method should be extended when the confirmation should generated
            other documents. In this method, the SO are in 'sale' state (not yet 'done').
        """
        # create an analytic account if at least an expense product
        val = super(SaleOrder, self)._action_confirm()
        for order in self:
            order._create_invoices()
            if any([expense_policy not in [False, 'no'] for expense_policy in order.order_line.mapped('product_id.expense_policy')]):
                if not order.analytic_account_id:
                    order._create_analytic_account()

        return val
