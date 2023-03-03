# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#        (https://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, api, _
import logging

_logger = logging.getLogger(__name__)


class AccountMoveDS(models.Model):
    _inherit = "account.move"


    def js_assign_outstanding_line(self, line_id):
        rslt = super(AccountMoveDS, self).js_assign_outstanding_line(line_id)
        _logger.info("invoice_payment_state************333333333333333333#####**%s" %self.invoice_payment_state) 
        if self.invoice_payment_state == 'paid':
            self.action_view_payments()
        return rslt    




    def action_view_payments(self):
        """
        This function returns an action that display existing payments of given
        account moves.
        When only one found, show the payment immediately.
        """
        if self.type in ("in_invoice", "in_refund"):
            action = self.env.ref("account.action_account_payments_payable")
        else:
            action = self.env.ref("account.action_account_payments")
        result = action.read()[0]
        reconciles = self._get_reconciled_info_JSON_values()
        payment = []
        for rec in reconciles:
            payment.append(rec["account_payment_id"])

            
        _logger.info("payment************333333333333333333#####**%s" %payment) 

        self.payment_number_temp = ""
        payment_number_temp = ""
        for dtfs in payment:
            data_payment = self.env["account.payment"].search([("id",'=',dtfs)])
            if data_payment.name:
                self.payment_number_temp = self.payment_number_temp + data_payment.name.split('/')[1] + "/" +data_payment.name.split('/')[2] + ","

        # choose the view_mode accordingly
        if len(reconciles) != 1:
            result["domain"] = "[('id', 'in', " + str(payment) + ")]"
        else:
            res = self.env.ref("account.view_account_payment_form", False)
            result["views"] = [(res and res.id or False, "form")]
            result["res_id"] = payment and payment[0] or False
        _logger.info("resultresult************333333333333333333#####**%s" %result)

        return result
