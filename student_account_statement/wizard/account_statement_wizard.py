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
        header = workbook.add_format({'bold': True, 'border': 1, 'align': 'center', 'bg_color': '#D9EAD3'})
        title_format = workbook.add_format({'bold': True, 'font_size': 12, 'align': 'right', 'bg_color': '#FCE4D6'})
        normal = workbook.add_format({'border': 1, 'align': 'center'})
        normal_right = workbook.add_format({'border': 1, 'align': 'right'})
        amount_format = workbook.add_format({'border': 1, 'num_format': '#,##0.00', 'align': 'center'})
        
        partner = self.partner_id

        # Set Column Widths
        sheet.set_column('A:A', 15) # Date
        sheet.set_column('B:B', 25) # Invoices
        sheet.set_column('C:C', 25) # Payments
        sheet.set_column('D:D', 25) # Balance
        sheet.set_column('E:E', 25) # Installment

        row = 0

        # =====================================================
        # STUDENT INFORMATION
        # =====================================================
        sheet.write(row, 0, 'Student Name:', header)
        sheet.write(row, 1, partner.name or '', normal_right)
        row += 1
        
        sheet.write(row, 0, 'Department:', header)
        sheet.write(row, 1, partner.department.department if hasattr(partner, 'department') and partner.department else '', normal_right)
        row += 3

        # =====================================================
        # FETCH DATA (Exactly as you requested)
        # =====================================================
        
        # 1. Invoices
        invoices = self.env['account.move'].search([
            ('partner_id', '=', partner.id),
            ('type', '=', 'out_invoice')
        ], order='invoice_date_due asc')

        # 2. Payments
        payments = self.env['account.payment'].search([
            ('partner_id', '=', partner.id)
        ], order='payment_date asc')

        # 3. Installments (Optional, we will try to fetch it safely)
        installment_by_year = defaultdict(float)
        try:
            sale_orders = self.env['sale.order'].search([('partner_id', '=', partner.id)])
            for sale in sale_orders:
                if hasattr(sale, 'sale_installment_line_ids'):
                    for inst in sale.sale_installment_line_ids:
                        if getattr(inst, 'amount_installment', False) and getattr(inst, 'payment_date', False):
                            year_str = getattr(sale, 'year', str(inst.payment_date.year))
                            installment_by_year[year_str] += inst.amount_installment
        except Exception:
            pass

        # =====================================================
        # BUILD LEDGER LINES
        # =====================================================
        ledger = []

        for inv in invoices:
            # Use the Char field 'year' from the invoice if available, else use year from date
            year_str = inv.year if hasattr(inv, 'year') and inv.year else str(inv.invoice_date_due.year if inv.invoice_date_due else '')
            
            ledger.append({
                'date': inv.invoice_date_due,
                'year': year_str,
                'invoice': inv.amount_total,
                'payment': 0.0,
            })

        for pay in payments:
            # Payments don't usually have a 'year' char field, so we use their date year
            year_str = str(pay.payment_date.year if pay.payment_date else '')
            ledger.append({
                'date': pay.payment_date,
                'year': year_str,
                'invoice': 0.0,
                'payment': pay.amount,
            })

        # Sort lines by date ascending
        ledger.sort(key=lambda x: x['date'] or fields.Date.today())

        # Group by Year
        grouped_data = defaultdict(list)
        for item in ledger:
            grouped_data[item['year']].append(item)

        sorted_years = sorted(grouped_data.keys())

        # =====================================================
        # WRITE TO EXCEL
        # =====================================================
        
        grand_invoice_total = 0
        grand_payment_total = 0

        for year in sorted_years:
            # Year Title
            sheet.merge_range(row, 0, row, 4, f'السنة الدراسية : {year}', title_format)
            row += 1

            # Columns Header
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

            # Write Yearly Lines
            for item in grouped_data[year]:
                inv_amt = item['invoice']
                pay_amt = item['payment']
                
                # Calculate Running Balance
                current_balance += (inv_amt - pay_amt)

                # Write Date
                date_str = item['date'].strftime('%Y-%m-%d') if item['date'] else ''
                sheet.write(row, 0, date_str, normal)
                
                # Write Invoice Amount (only if it's > 0)
                sheet.write(row, 1, inv_amt if inv_amt > 0 else '', amount_format)
                
                # Write Payment Amount (only if it's > 0)
                sheet.write(row, 2, pay_amt if pay_amt > 0 else '', amount_format)
                
                # Write Balance
                sheet.write(row, 3, current_balance, amount_format)
                
                # Installment column (blank for normal rows)
                sheet.write(row, 4, '', amount_format)
                
                row += 1
                year_invoice_total += inv_amt
                year_payment_total += pay_amt

            # =====================================================
            # YEAR TOTALS (المجموع)
            # =====================================================
            sheet.write(row, 0, 'المجموع', header)
            sheet.write(row, 1, year_invoice_total, header)
            sheet.write(row, 2, year_payment_total, header)
            sheet.write(row, 3, '', header)
            sheet.write(row, 4, '', header)
            row += 1
            
            # =====================================================
            # TOTAL INSTALLMENT (القسط الكلي)
            # =====================================================
            sheet.write(row, 0, 'القسط الكلي', header)
            sheet.write(row, 1, '', header)
            sheet.write(row, 2, '', header)
            sheet.write(row, 3, '', header)
            sheet.write(row, 4, year_installment_total, header)
            row += 2

            grand_invoice_total += year_invoice_total
            grand_payment_total += year_payment_total

        # =====================================================
        # GRAND BALANCE AT BOTTOM
        # =====================================================
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