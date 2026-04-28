from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    year_of_acceptance_1 = fields.Many2one(
        comodel_name='techtime_mcc_data.techtime_mcc_data',
        string="Year of Acceptance",
        related='partner_id.year_of_acceptance_1',
        store=True,
        readonly=True
    )
