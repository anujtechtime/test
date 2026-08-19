from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    payment_type_name = fields.Selection(
        [
            ('1', 'كاش'),
            ('2', 'دفع الكتروني'),
        ],
        string='نوع الدفع',
    )
