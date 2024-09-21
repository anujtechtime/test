# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import base64
from odoo.exceptions import ValidationError, UserError


class almaaqal_request_transfering(models.Model):
    _inherit = 'res.partner'

    def print_transfer(self):
        # Generate PDF report
        report = self.env.ref('almaaqal_request_transfering.report_payment_receipt_request_of_transferring')

        pdf_content, _ = report.render_qweb_pdf(res_ids=self.ids)

        sale_ord = self.env["sale.order"].search([("partner_id","=",self.id),("year","=",self.year.id)],limit=1)
        count = 0
        for inv in sale_ord.sale_installment_line_ids:
            if count == 0 and inv.payment_status != 'paid':
                raise ValidationError('الدفعه الاولئ غير مدفوعه!')
            count = count + 1

        # Convert PDF to base64
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')

        # Create attachment
        attachment = self.env['ir.attachment'].create({
            'name': 'Request_of_transferring_shift.pdf',
            'type': 'binary',
            'datas': pdf_base64,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/pdf'
        })

        self.message_post(
            body="Request of transferring (PDF),",
            attachment_ids=[attachment.id]
        )


        return self.env.ref('almaaqal_request_transfering.report_payment_receipt_request_of_transferring').report_action(self)   