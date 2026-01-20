from odoo import http, _
from odoo.http import request
from odoo.addons.web.controllers.main import ReportController
from datetime import datetime
import json
import base64


class ReportControllerInherit(ReportController):

    @http.route(['/report/download'], type='http', auth='user')
    def report_download(self, data, context=None):
        # Parse request
        request_content = json.loads(data)
        report_name = request_content[0]
        report_type = request_content[1]
        docids = request_content[2]

        ctx = request.env.context
        active_model = ctx.get('active_model')
        active_ids = ctx.get('active_ids')

        # 🔥 LOG HERE (THIS ALWAYS FIRES)
        if active_model and active_ids:
            records = request.env[active_model].browse(active_ids)
            user = request.env.user
            now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

            for rec in records:
                if hasattr(rec, 'message_post'):
                    rec.message_post(
                        body=_(
                            "<b>%s</b> downloaded %s report <i>%s</i> on %s"
                        ) % (user.name, report_type.upper(), report_name, now),
                        subtype_xmlid='mail.mt_note'
                    )

        # Continue normal flow
        return super().report_download(data, context=context)
