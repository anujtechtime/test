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

    def action_export_excel(self):
        self.ensure_one()

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Account Statement')

        # Formats
        header = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center',
            'bg_color': '#D9EAD3',
        })
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center',
        })
        normal = workbook.add_format({
            'border': 1,
        })
        amount_format = workbook.add_format({
            'border': 1,
            'num_format': '#,##0.00',
        })
        
        partner = self.partner_id

        sheet.set_column('A:A', 15) # Date
        sheet.set_column('B:B', 20) # Invoice
        sheet.set_column('C:C', 20) # Payment
        sheet.set_column('D:D', 20) # Balance
        sheet.set_column('E:E', 20) # Total Installment

        row = 0

        # =====================================================
        # STUDENT INFORMATION
        # =====================================================
        sheet.write(row, 0, 'Student Name:', header)
        sheet.write(row, 1, partner.name or '', normal)

        row += 1
        sheet.write(row, 0, 'Department:', header)
        sheet.write(
            row,
            1,
            partner.department.department if partner.department else '',
            normal
        )

        row += 3

        # =====================================================
        # FETCH DATA (Using Journal Items as requested)
        # =====================================================
        
        # 1. Invoices (فواتير الطلاب IQD)
        invoice_lines = self.env['account.move.line'].search([
            ('partner_id', '=', partner.id),
            ('journal_id.name', 'ilike', 'فواتير الطلاب IQD'),
            ('parent_state', '=', 'posted')
        ])

        # 2. Payments (صندوق النقد العراقي)
        payment_lines = self.env['account.move.line'].search([
            ('partner_id', '=', partner.id),
            ('journal_id.name', 'ilike', 'صندوق النقد العراقي'),
            ('parent_state', '=', 'posted')
        ])

        # 3. Installments (القسط الكلي) from Sale Orders
        # Assuming your installment data comes from sale orders related to this partner
        installment_by_year = defaultdict(float)
        sale_orders = self.env['sale.order'].search([
            ('partner_id', '=', partner.id),
        ])
        
        for sale in sale_orders:
            if hasattr(sale, 'sale_installment_line_ids'):
                for inst in sale.sale_installment_line_ids:
                    if inst.payment_date:
                        # Grouping by academic year (assuming we can get it from the SO)
                        year_str = sale.year.name if hasattr(sale, 'year') and sale.year else str(inst.payment_date.year)
                        installment_by_year[year_str] += inst.amount_installment

        # =====================================================
        # BUILD LEDGER LINES
        # =====================================================
        ledger = []

        for line in invoice_lines:
            ledger.append({
                'date': line.date,
                'year': line.move_id.year.name if hasattr(line.move_id, 'year') and line.move_id.year else str(line.date.year),
                'invoice': line.debit, # Debit increases what student owes
                'payment': line.credit,
            })

        for line in payment_lines:
            ledger.append({
                'date': line.date,
                'year': line.move_id.year.name if hasattr(line.move_id, 'year') and line.move_id.year else str(line.date.year),
                'invoice': line.debit,
                'payment': line.credit, # Credit means payment received
            })

        # Sort ascending by date (Requirement #4 & #8)
        ledger.sort(key=lambda x: x['date'])

        # Group by Academic Year (Requirement #5)
        grouped_data = defaultdict(list)
        for item in ledger:
            grouped_data[item['year']].append(item)

        # Ensure years are sorted
        sorted_years = sorted(grouped_data.keys())

        # =====================================================
        # WRITE TO EXCEL
        # =====================================================
        
        grand_invoice_total = 0
        grand_payment_total = 0
        grand_installment_total = 0

        for year in sorted_years:
            # Write Year Title
            sheet.merge_range(row, 0, row, 4, f'السنة الدراسية : {year}', title_format)
            row += 1

            # Table Headers
            sheet.write(row, 0, 'التاريخ', header)
            sheet.write(row, 1, 'فواتير (مطلوبة السداد)', header)
            sheet.write(row, 2, 'دفعات (وصولات مسددة)', header)
            sheet.write(row, 3, 'المدور', header)
            sheet.write(row, 4, 'القسط الكلي', header)
            row += 1

            year_invoice_total = 0
            year_payment_total = 0
            current_balance = 0
            
            year_installment_total = installment_by_year.get(year, 0)

            # Yearly Rows
            for item in grouped_data[year]:
                inv_amt = item['invoice']
                pay_amt = item['payment']
                
                # Balance = Column 1 - Column 2 (Cumulative)
                current_balance += (inv_amt - pay_amt)

                sheet.write(row, 0, item['date'].strftime('%Y-%m-%d'), normal)
                sheet.write(row, 1, inv_amt if inv_amt > 0 else '', amount_format)
                sheet.write(row, 2, pay_amt if pay_amt > 0 else '', amount_format)
                sheet.write(row, 3, current_balance, amount_format)
                
                # Write Installment only on the first row of the year
                if row == len(grouped_data[year]) + 3: # Simple check, adjust if needed
                    pass
                
                row += 1
                year_invoice_total += inv_amt
                year_payment_total += pay_amt

            # Write Total Installment for this year on the first row
            # (Re-calculating row index to place it correctly)
            
            # Year Totals Row (المجموع)
            sheet.write(row, 0, 'المجموع', header)
            sheet.write(row, 1, year_invoice_total, header)
            sheet.write(row, 2, year_payment_total, header)
            sheet.write(row, 3, '', header)
            sheet.write(row, 4, year_installment_total, header)
            row += 1
            
            # Write Total Installment text row (القسط الكلي)
            sheet.write(row, 0, 'القسط الكلي', header)
            sheet.write(row, 4, year_installment_total, header)
            row += 2

            grand_invoice_total += year_invoice_total
            grand_payment_total += year_payment_total
            grand_installment_total += year_installment_total

        # Final Balance at the bottom
        final_balance = grand_invoice_total - grand_payment_total
        sheet.write(row, 0, 'الرصيد النهائي (Balance)', header)
        sheet.write(row, 1, final_balance, header)

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