from odoo import models, api, _
from datetime import datetime


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def report_action(self, docids, data=None, config=True):
        res = super().report_action(docids, data=data, config=config)

        if self.model == 'res.partner' and docids:
            partners = self.env['res.partner'].browse(docids)
            user = self.env.user
            now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

            for partner in partners:
                partner.message_post(
                    body=_(
                        "<b>%s</b> printed report <i>%s</i> on %s"
                    ) % (user.name, self.name, now),
                    message_type='comment',
                    subtype_xmlid='mail.mt_note'
                )

        return res
