# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class almaaqal_report_account(models.Model):
#     _name = 'almaaqal_report_account.almaaqal_report_account'
#     _description = 'almaaqal_report_account.almaaqal_report_account'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

from odoo import models, fields, _

# class SaleOrdermReportWizard(models.TransientModel):
#     _name = 'account.almaaqal.report.wizard'
#     _description = 'Sale Order Report Wizard'

#     date_from = fields.Date(string="Start Date", required=True)
#     date_to = fields.Date(string="End Date", required=True)

#     def action_print_report(self, ):
#         """Filters sale orders based on the selected date range and prints the report"""
#         data = self.pre_print_report(data)
#         records = self.env[data['model']].browse(data.get('ids', []))
#         return self.env.ref(
#             'almaaqal_template.action_report_trial_balance_2').report_action(
#             records, data=data)


class AccountBalanceReportpageblock(models.TransientModel):
    _inherit = "account.common.account.report"
    _name = 'account.balance.report.new.block'
    _description = 'Account Balance Report'

    journal_ids = fields.Many2many('account.journal',
                                   'account_balance_report_new_block_journal_rel',
                                   'account_id', 'journal_id',
                                   string='Journals', required=True,
                                   default=[])

    def _print_report(self, data):
        data = self.pre_print_report(data)
        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref(
            'almaaqal_report_account.action_report_account_balance').report_action(
            records, data=data)


class AccountBalanceReportpageblockNew(models.TransientModel):
    _inherit = "account.common.account.report"
    _name = 'account.balance.report.new.block.new'
    _description = 'Account Balance Report'

    journal_ids = fields.Many2many('account.journal',
                                   'account_balance_report_new_block_new_journal_rel',
                                   'account_id', 'journal_id',
                                   string='Journals', required=True,
                                   default=[])

    def _print_report(self, data):
        data = self.pre_print_report(data)
        records = self.env[data['model']].browse(data.get('ids', []))
        print("data@@@@@@@@@@@@@@",data)
        return self.env.ref(
            'almaaqal_report_account.action_report_account_balance_new').report_action(
            records, data=data)            

class AccountBalanceReportpageblockTwo(models.TransientModel):
    _inherit = "account.common.account.report"
    _name = 'account.balance.report.new.block.two'
    _description = 'Account Balance Report'

    journal_ids = fields.Many2many('account.journal',
                                   'account_balance_report_new_block_two_journal_rel',
                                   'account_id', 'journal_id',
                                   string='Journals', required=True,
                                   default=[])

    def _print_report(self, data):
        data = self.pre_print_report(data)
        records = self.env[data['model']].browse(data.get('ids', []))
        print("data@@@@@@@@@@@@@@",data)
        return self.env.ref(
            'almaaqal_report_account.action_report_account_balance_two').report_action(
            records, data=data)            

class AccountBalanceReportpageblockThree(models.TransientModel):
    _inherit = "account.common.account.report"
    _name = 'account.balance.report.new.block.three'
    _description = 'Account Balance Report'

    journal_ids = fields.Many2many('account.journal',
                                   'account_balance_report_new_block_three_journal_rel',
                                   'account_id', 'journal_id',
                                   string='Journals', required=True,
                                   default=[])

    def _print_report(self, data):
        data = self.pre_print_report(data)
        records = self.env[data['model']].browse(data.get('ids', []))
        print("data@@@@@@@@@@@@@@",data)
        return self.env.ref(
            'almaaqal_report_account.action_report_account_balance_three').report_action(
            records, data=data)            


class AccountBalanceReportpageblockFour(models.TransientModel):
    _inherit = "account.common.account.report"
    _name = 'account.balance.report.new.block.four'
    _description = 'Account Balance Report'

    journal_ids = fields.Many2many('account.journal',
                                   'account_balance_report_new_block_four_journal_rel',
                                   'account_id', 'journal_id',
                                   string='Journals', required=True,
                                   default=[])

    def _print_report(self, data):
        data = self.pre_print_report(data)
        records = self.env[data['model']].browse(data.get('ids', []))
        print("data@@@@@@@@@@@@@@",data)
        return self.env.ref(
            'almaaqal_report_account.action_report_account_balance_four').report_action(
            records, data=data)            
