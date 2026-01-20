from odoo import models, api, _
from datetime import datetime


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.model
    def _render_qweb_pdf(self, res_ids=None, data=None):
        pdf, _ = super()._render_qweb_pdf(res_ids=res_ids, data=data)

        if self.model == 'res.partner' and res_ids:
            partners = self.env['res.partner'].browse(res_ids)
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

        return pdf, _
