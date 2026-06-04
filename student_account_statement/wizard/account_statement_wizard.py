import io
import base64
import xlsxwriter

from odoo import models, fields


class AccountStatementWizard(models.TransientModel):
    _name = 'account.statement.wizard'
    _description = 'Account Statement Wizard'

    partner_id = fields.Many2one(
        'res.partner',
        string='Student',
        required=True
    )

    file_data = fields.Binary()
    file_name = fields.Char()

    def action_export_excel(self):

        self.ensure_one()

        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Account Statement')

        header = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
        })

        normal = workbook.add_format({
            'border': 1,
        })

        partner = self.partner_id

        row = 0

        sheet.write(row, 0, 'Student', header)
        sheet.write(row, 1, partner.name or '', normal)

        row += 1

        sheet.write(row, 0, 'Department', header)
        sheet.write(
            row,
            1,
            partner.department.department if partner.department else '',
            normal
        )

        row += 3

        sheet.write(row, 0, 'Invoices', header)

        row += 1

        sheet.write(row, 0, 'Due Date', header)
        sheet.write(row, 1, 'Amount', header)

        invoices = self.env['account.move'].search([
            ('partner_id', '=', partner.id),
            ('type', '=', 'out_invoice')
        ], order='invoice_date_due asc')

        invoice_total = 0

        for inv in invoices:
            row += 1
            sheet.write(row, 0, str(inv.invoice_date_due or ''), normal)
            sheet.write(row, 1, inv.amount_total, normal)

            invoice_total += inv.amount_total

        row += 1

        sheet.write(row, 0, 'Invoice Total', header)
        sheet.write(row, 1, invoice_total, header)

        row += 3

        sheet.write(row, 0, 'Payments', header)

        row += 1

        sheet.write(row, 0, 'Payment Date', header)
        sheet.write(row, 1, 'Amount', header)

        payments = self.env['account.payment'].search([
            ('partner_id', '=', partner.id)
        ], order='payment_date asc')

        payment_total = 0

        for pay in payments:
            row += 1
            sheet.write(row, 0, str(pay.payment_date or ''), normal)
            sheet.write(row, 1, pay.amount, normal)

            payment_total += pay.amount

        row += 1

        sheet.write(row, 0, 'Payment Total', header)
        sheet.write(row, 1, payment_total, header)

        row += 2

        balance = invoice_total - payment_total

        sheet.write(row, 0, 'Balance', header)
        sheet.write(row, 1, balance, header)

        workbook.close()

        output.seek(0)

        self.file_name = 'Account_Statement.xlsx'
        self.file_data = base64.b64encode(output.read())

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=%s&id=%s&field=file_data&download=true&filename=%s'
                   % (self._name, self.id, self.file_name),
            'target': 'self',
        }