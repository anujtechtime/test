from odoo import models, api, _
from datetime import datetime


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def report_action(self, docids=None, data=None, config=True):
        res = super().report_action(docids, data=data, config=config)

        # ✅ Odoo 13 FIX: read IDs from context
        active_ids = self.env.context.get('active_ids')

        if self.model == 'res.partner' and active_ids:
            partners = self.env['res.partner'].browse(active_ids)
            user = self.env.user
            now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

            for partner in partners:
                partner.message_post(
                    body=_(
                        "<b>%s</b> printed report <i>%s</i> on %s"
                    ) % (user.name, self.name, now),
                    subtype_xmlid='mail.mt_note'
                )

        return res
