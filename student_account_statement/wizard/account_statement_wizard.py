import io
import base64
import xlsxwriter

from odoo import models, fields

from collections import defaultdict

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

    def action_print_report(self):
        return self.env.ref('student_account_statement.action_report_account_statement').report_action(self)
    


    # def action_export_excel(self):

    #     self.ensure_one()

    #     output = io.BytesIO()

    #     workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    #     sheet = workbook.add_worksheet('Account Statement')

    #     header = workbook.add_format({
    #         'bold': True,
    #         'border': 1,
    #         'align': 'center',
    #     })

    #     normal = workbook.add_format({
    #         'border': 1,
    #     })

    #     partner = self.partner_id

    #     row = 0

    #     sheet.write(row, 0, 'Student', header)
    #     sheet.write(row, 1, partner.name or '', normal)

    #     row += 1

    #     sheet.write(row, 0, 'Department', header)
    #     sheet.write(
    #         row,
    #         1,
    #         partner.department.department if partner.department else '',
    #         normal
    #     )

    #     row += 3

    #     sheet.write(row, 0, 'Invoices', header)

    #     row += 1

    #     sheet.write(row, 0, 'Due Date', header)
    #     sheet.write(row, 1, 'Amount', header)

    #     invoices = self.env['account.move'].search([
    #         ('partner_id', '=', partner.id),
    #         ('type', '=', 'out_invoice')
    #     ], order='invoice_date_due asc')

    #     invoice_total = 0

    #     for inv in invoices:
    #         row += 1
    #         sheet.write(row, 0, str(inv.invoice_date_due or ''), normal)
    #         sheet.write(row, 1, inv.amount_total, normal)

    #         invoice_total += inv.amount_total

    #     row += 1

    #     sheet.write(row, 0, 'Invoice Total', header)
    #     sheet.write(row, 1, invoice_total, header)

    #     row += 3

    #     sheet.write(row, 0, 'Payments', header)

    #     row += 1

    #     sheet.write(row, 0, 'Payment Date', header)
    #     sheet.write(row, 1, 'Amount', header)

    #     payments = self.env['account.payment'].search([
    #         ('partner_id', '=', partner.id)
    #     ], order='payment_date asc')

    #     payment_total = 0

    #     for pay in payments:
    #         row += 1
    #         sheet.write(row, 0, str(pay.payment_date or ''), normal)
    #         sheet.write(row, 1, pay.amount, normal)

    #         payment_total += pay.amount

    #     row += 1

    #     sheet.write(row, 0, 'Payment Total', header)
    #     sheet.write(row, 1, payment_total, header)

    #     row += 2

    #     balance = invoice_total - payment_total

    #     sheet.write(row, 0, 'Balance', header)
    #     sheet.write(row, 1, balance, header)

    #     workbook.close()

    #     output.seek(0)

    #     self.file_name = 'Account_Statement.xlsx'
    #     self.file_data = base64.b64encode(output.read())

    #     return {
    #         'type': 'ir.actions.act_url',
    #         'url': '/web/content/?model=%s&id=%s&field=file_data&download=true&filename=%s'
    #                % (self._name, self.id, self.file_name),
    #         'target': 'self',
    #     }

    

    def action_export_excel(self):
        self.ensure_one()

        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Account Statement')

        header = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'bg_color': '#D9EAD3',
        })

        normal = workbook.add_format({
            'border': 1,
        })

        amount_format = workbook.add_format({
            'border': 1,
            'num_format': '#,##0.00',
        })

        partner = self.partner_id

        sheet.set_column('A:A', 15)
        sheet.set_column('B:C', 18)
        sheet.set_column('D:F', 20)

        row = 0

        # =====================================================
        # STUDENT INFORMATION
        # =====================================================

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

        row += 4

        # =====================================================
        # INVOICES
        # =====================================================

        invoices = self.env['account.move'].search(
            [
                ('partner_id', '=', partner.id),
                ('type', '=', 'out_invoice'),
                ('state', '=', 'posted')
            ],
            order='invoice_date_due asc'
        )

        invoice_by_year = defaultdict(list)

        for inv in invoices:
            if inv.invoice_date_due:
                invoice_by_year[inv.invoice_date_due.year].append({
                    'date': inv.invoice_date_due,
                    'amount': inv.amount_total,
                })

        # =====================================================
        # PAYMENTS
        # =====================================================

        payments = self.env['account.payment'].search(
            [
                ('partner_id', '=', partner.id),
                ('state', '=', 'posted')
            ],
            order='payment_date asc'
        )

        payment_by_year = defaultdict(list)

        for pay in payments:
            if pay.payment_date:
                payment_by_year[pay.payment_date.year].append({
                    'date': pay.payment_date,
                    'amount': pay.amount,
                })

        # =====================================================
        # INSTALLMENTS
        # =====================================================

        installment_by_year = defaultdict(float)

        sale_orders = self.env['sale.order'].search([
            ('partner_id', '=', partner.id),
        ])

        for sale in sale_orders:
            for inst in sale.sale_installment_line_ids:

                if inst.payment_date:
                    installment_by_year[
                        inst.payment_date.year
                    ] += inst.amount_installment

        # =====================================================
        # ALL YEARS
        # =====================================================

        years = sorted(
            set(invoice_by_year.keys())
            | set(payment_by_year.keys())
            | set(installment_by_year.keys())
        )

        # =====================================================
        # TABLE HEADER
        # =====================================================

        sheet.write(row, 0, 'Year', header)
        sheet.write(row, 1, 'Due Date', header)
        sheet.write(row, 2, 'Payment Date', header)
        sheet.write(row, 3, 'Invoice Amount', header)
        sheet.write(row, 4, 'Payment Amount', header)
        sheet.write(row, 5, 'Installment Amount', header)

        row += 1

        grand_invoice_total = 0
        grand_payment_total = 0
        grand_installment_total = 0

        # =====================================================
        # YEAR WISE REPORT
        # =====================================================

        for year in years:

            invoice_lines = invoice_by_year.get(year, [])
            payment_lines = payment_by_year.get(year, [])

            max_rows = max(
                len(invoice_lines),
                len(payment_lines),
                1
            )

            year_invoice_total = 0
            year_payment_total = 0
            year_installment_total = installment_by_year.get(year, 0)

            for i in range(max_rows):

                sheet.write(row, 0, year, normal)

                if i < len(invoice_lines):

                    sheet.write(
                        row,
                        1,
                        str(invoice_lines[i]['date']),
                        normal
                    )

                    sheet.write(
                        row,
                        3,
                        invoice_lines[i]['amount'],
                        amount_format
                    )

                    year_invoice_total += invoice_lines[i]['amount']

                if i < len(payment_lines):

                    sheet.write(
                        row,
                        2,
                        str(payment_lines[i]['date']),
                        normal
                    )

                    sheet.write(
                        row,
                        4,
                        payment_lines[i]['amount'],
                        amount_format
                    )

                    year_payment_total += payment_lines[i]['amount']

                if i == 0:

                    sheet.write(
                        row,
                        5,
                        year_installment_total,
                        amount_format
                    )

                row += 1

            grand_invoice_total += year_invoice_total
            grand_payment_total += year_payment_total
            grand_installment_total += year_installment_total

            sheet.write(row, 0, f'Total {year}', header)
            sheet.write(row, 3, year_invoice_total, header)
            sheet.write(row, 4, year_payment_total, header)
            sheet.write(row, 5, year_installment_total, header)

            row += 2

        # =====================================================
        # GRAND TOTAL
        # =====================================================

        sheet.write(row, 0, 'Grand Total', header)
        sheet.write(row, 3, grand_invoice_total, header)
        sheet.write(row, 4, grand_payment_total, header)
        sheet.write(row, 5, grand_installment_total, header)

        row += 2

        # =====================================================
        # BALANCE
        # =====================================================

        balance = grand_invoice_total - grand_payment_total

        if balance > 0:
            balance_text = "مطلوب %.2f" % abs(balance)
        else:
            balance_text = "يطلب %.2f" % abs(balance)

        sheet.write(row, 0, 'Balance', header)
        sheet.write(row, 1, balance_text, header)

        # =====================================================
        # SAVE FILE
        # =====================================================

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