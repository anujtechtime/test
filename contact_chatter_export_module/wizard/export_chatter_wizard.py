from odoo import models, fields
import base64
import io
import xlsxwriter


class PartnerChatterExportWizard(models.TransientModel):
    _name = 'partner.chatter.export.wizard'
    _description = 'Export Contact Chatter'

    partner_id = fields.Many2one('res.partner', required=True)
    file = fields.Binary('File')
    file_name = fields.Char('File Name')

    def export_chatter(self):

        messages = self.env['mail.message'].sudo().search([
            ('model', '=', 'res.partner'),
            ('res_id', '=', self.partner_id.id)
        ], order="date asc")

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet('Chatter')

        headers = ['Date', 'Author', 'Type', 'Message']
        for col, header in enumerate(headers):
            sheet.write(0, col, header)

        row = 1

        for msg in messages:

            # Export normal chatter message
            if msg.body:
                sheet.write(row, 0, str(msg.date or ''))
                sheet.write(row, 1, msg.author_id.name or '')
                sheet.write(row, 2, msg.message_type or 'message')
                sheet.write(row, 3, msg.body or '')
                row += 1

            # Export tracking values (field changes)
            for track in msg.tracking_value_ids:

                old_value = (
                    track.old_value_char
                    or track.old_value_text
                    or track.old_value_integer
                    or track.old_value_float
                    or ''
                )

                new_value = (
                    track.new_value_char
                    or track.new_value_text
                    or track.new_value_integer
                    or track.new_value_float
                    or ''
                )

                change_text = "%s : %s → %s" % (
                    track.field_desc,
                    old_value,
                    new_value
                )

                sheet.write(row, 0, str(msg.date or ''))
                sheet.write(row, 1, msg.author_id.name or '')
                sheet.write(row, 2, "Field Change")
                sheet.write(row, 3, change_text)

                row += 1

        workbook.close()
        output.seek(0)

        file_data = base64.b64encode(output.read())

        self.file = file_data
        self.file_name = "contact_chatter.xlsx"

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=partner.chatter.export.wizard&id=%s&field=file&download=true&filename=%s'
                   % (self.id, self.file_name),
            'target': 'self',
        }