from odoo import models, api, _
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    @api.model
    def _get_report_from_name(self, report_name):
        report = super()._get_report_from_name(report_name)

        ctx = self.env.context
        active_model = ctx.get('active_model')
        active_ids = ctx.get('active_ids')

        _logger.warning(
            "REPORT PRINT DETECTED | report=%s model=%s ids=%s",
            report_name, active_model, active_ids
        )

        if active_model == 'res.partner' and active_ids:
            partners = self.env['res.partner'].browse(active_ids)
            user = self.env.user
            now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

            for partner in partners:
                partner.message_post(
                    body=_(
                        "<b>%s</b> printed report <i>%s</i> on %s"
                    ) % (user.name, report.name, now),
                    subtype_xmlid='mail.mt_note'
                )

        return report
