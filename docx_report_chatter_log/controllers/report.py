from odoo import http, _
from odoo.http import request
from odoo.addons.web.controllers.main import ReportController
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class ReportControllerInherit(ReportController):

    @http.route(['/report/download'], type='http', auth='user')
    def report_download(self, data, context=None):
        # 🔒 ALWAYS call super first (important in Odoo 13)
        response = super().report_download(data, context=context)

        try:
            ctx = request.env.context or {}
            active_model = ctx.get('active_model')
            active_ids = ctx.get('active_ids')

            if active_model and active_ids:
                records = request.env[active_model].browse(active_ids)
                user = request.env.user
                now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

                for rec in records:
                    if hasattr(rec, 'message_post'):
                        rec.message_post(
                            body=_(
                                "<b>%s</b> downloaded a report on %s"
                            ) % (user.name, now),
                            subtype_xmlid='mail.mt_note'
                        )

        except Exception as e:
            # ❗ Never block report download
            _logger.exception("Report download chatter log failed: %s", e)

        return response
