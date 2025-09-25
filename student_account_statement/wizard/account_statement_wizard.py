from odoo import models, fields

class AccountStatementWizard(models.TransientModel):
    _name = 'account.statement.wizard'
    _description = 'Account Statement Wizard'

    partner_id = fields.Many2one('res.partner', string='Student', required=True)

    def action_print_report(self):
        return self.env.ref('student_account_statement.action_report_account_statement').report_action(self)
