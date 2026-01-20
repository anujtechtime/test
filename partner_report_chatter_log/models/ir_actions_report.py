from odoo import http, _
from odoo.http import request
from odoo.addons.web.controllers.main import ReportController
from datetime import datetime


class ReportControllerInherit(ReportController):

    @http.route([
        '/report/docx/<string:report_name>/<string:docids>',
    ], type='http', auth='user')
    def report_docx(self, report_name, docids=None, **data):
        # 🔥 LOG BEFORE DOWNLOAD
        ctx = request.env.context
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
                            "<b>%s</b> printed DOCX report <i>%s</i> on %s"
                        ) % (user.name, report_name, now),
                        subtype_xmlid='mail.mt_note'
                    )

        # ✅ Continue normal DOCX generation
        return super().report_docx(report_name, docids, **data)
