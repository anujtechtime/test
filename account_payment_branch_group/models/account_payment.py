from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"

    x_branch_code = fields.Integer(string="Branch Code")


class AccountPayment(models.Model):
    _inherit = "account.payment"

    user_branch_code = fields.Integer(
        string="User Branch Code",
        related="create_uid.x_branch_code",
        store=True
    )
