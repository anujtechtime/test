# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CrmTeamDateAccount(models.Model):

    _inherit = "account.payment"

    payment_method = fields.Selection([('cash','نقد'),
        ('debit','دين'),
        ('cheque','صك')],string="Payment Method")

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')

