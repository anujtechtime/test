from odoo import models, api, _
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def render_docx(self, docids, data=None):
        # 🔹 Call original DOCX render
        result = super(IrActionsReport, self).render_docx(docids, data=data)

        try:
            # ✅ docids is the KEY (active_ids is empty for DOCX)
            if self.model == 'res.partner' and docids:
                partners = self.env['res.partner'].browse(docids)
                user = self.env.user
                now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

                for partner in partners:
                    partner.message_post(
                        body=_(
                            "<b>%s</b> printed DOCX report <i>%s</i> on %s"
                        ) % (user.name, self.name, now),
                        subtype_xmlid='mail.mt_note'
                    )

        except Exception as e:
            _logger.exception("Failed to log DOCX report print: %s", e)

        return result
