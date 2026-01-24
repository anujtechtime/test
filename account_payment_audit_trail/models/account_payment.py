from odoo import models, _

class AccountPayment(models.Model):
    _inherit = "account.payment"

    def _payment_tracking_fields(self):
        ignored = {
            'id', 'create_uid', 'create_date',
            'write_uid', 'write_date',
            '__last_update', 'message_ids',
            'message_follower_ids', 'activity_ids',
            'message_attachment_count'
        }
        for name, field in self._fields.items():
            if name in ignored:
                continue
            if field.type in ('binary', 'one2many', 'many2many'):
                continue
            yield name, field

    def write(self, vals):
        if self.env.context.get("skip_payment_audit"):
            return super().write(vals)

        for payment in self:
            changes = []
            for field_name, field in payment._payment_tracking_fields():
                if field_name not in vals:
                    continue

                old_value = payment[field_name]
                new_value = vals[field_name]

                if old_value == new_value:
                    continue

                if field.type == "many2one":
                    old_value = old_value.display_name if old_value else ""
                    new_value = (
                        self.env[field.comodel_name]
                        .browse(new_value)
                        .display_name if new_value else ""
                    )
                else:
                    old_value = old_value or ""
                    new_value = new_value or ""

                changes.append(
                    "<li><b>%s</b>: %s → %s</li>"
                    % (field.string, old_value, new_value)
                )

            if changes:
                payment.with_context(mail_notrack=True).message_post(
                    body=_(
                        "<b>Payment updated by %s</b><ul>%s</ul>"
                    ) % (self.env.user.name, "".join(changes))
                )

        return super(AccountPayment, self).write(vals)