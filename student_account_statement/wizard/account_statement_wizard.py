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

        sheet.set_column('A:A', 15) # Date
        sheet.set_column('B:B', 25) # Invoices
        sheet.set_column('C:C', 25) # Payments
        sheet.set_column('D:D', 25) # Balance
        sheet.set_column('E:E', 25) # Installment

        row = 0

        # Student Info
        sheet.write(row, 0, 'Student Name:', header)
        sheet.write(row, 1, partner.name or '', normal_right)
        row += 1
        
        sheet.write(row, 0, 'Department:', header)
        dept = partner.department.department if hasattr(partner, 'department') and partner.department else ''
        sheet.write(row, 1, dept, normal_right)
        row += 3

        # =====================================================
        # FETCH DATA SAFELY USING SAVEPOINTS
        # =====================================================
        
        invoices = self.env['account.move']
        try:
            with self.env.cr.savepoint():
                invoices = self.env['account.move'].search([
                    ('partner_id', '=', partner.id),
                    ('type', '=', 'out_invoice')
                ], order='invoice_date_due asc')
        except Exception as e:
            print("Error loading invoices:", e)

        payments = self.env['account.payment']
        try:
            with self.env.cr.savepoint():
                payments = self.env['account.payment'].search([
                    ('partner_id', '=', partner.id)
                ], order='payment_date asc')
        except Exception as e:
            print("Error loading payments:", e)

        installment_by_year = defaultdict(float)
        try:
            with self.env.cr.savepoint():
                sale_orders = self.env['sale.order'].search([('partner_id', '=', partner.id)])
                for sale in sale_orders:
                    if hasattr(sale, 'sale_installment_line_ids'):
                        for inst in sale.sale_installment_line_ids:
                            if getattr(inst, 'amount_installment', False) and getattr(inst, 'payment_date', False):
                                year_str = getattr(sale, 'year', str(inst.payment_date.year))
                                installment_by_year[year_str] += inst.amount_installment
        except Exception as e:
            print("Error loading installments:", e)

        # =====================================================
        # BUILD LEDGER LINES
        # =====================================================
        ledger = []

        # Process Invoices safely
        for inv in invoices:
            try:
                with self.env.cr.savepoint():
                    inv_data = inv.read(['invoice_date_due', 'amount_total', 'year'])[0]
                    inv_date = inv_data.get('invoice_date_due')
                    inv_amount = inv_data.get('amount_total', 0.0)
                    
                    inv_year_char = inv_data.get('year')
                    year_str = str(inv_year_char) if inv_year_char else str(inv_date.year if inv_date else '')
                    
                    ledger.append({
                        'date': inv_date,
                        'year': year_str,
                        'invoice': inv_amount,
                        'payment': 0.0,
                    })
            except Exception as e:
                print("Skipping broken invoice:", e)
                continue 

        # Process Payments safely
        for pay in payments:
            try:
                with self.env.cr.savepoint():
                    pay_data = pay.read(['payment_date', 'amount'])[0]
                    pay_date = pay_data.get('payment_date')
                    pay_amount = pay_data.get('amount', 0.0)
                    
                    year_str = str(pay_date.year if pay_date else '')
                    
                    ledger.append({
                        'date': pay_date,
                        'year': year_str,
                        'invoice': 0.0,
                        'payment': pay_amount,
                    })
            except Exception as e:
                print("Skipping broken payment:", e)
                continue 

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
            sheet.merge_range(row, 0, row, 4, f'السنة الدراسية : {year}', title_format)
            row += 1

            sheet.write(row, 0, 'التاريخ', header)
            sheet.write(row, 1, 'فواتير (مطلوبة السداد)', header)
            sheet.write(row, 2, 'دفعات (وصولات مسددة)', header)
            sheet.write(row, 3, 'المدور', header)
            # sheet.write(row, 4, 'القسط الكلي', header)
            row += 1

            year_invoice_total = 0
            year_payment_total = 0
            current_balance = 0
            year_installment_total = installment_by_year.get(year, 0)

            for item in grouped_data[year]:
                inv_amt = item['invoice']
                pay_amt = item['payment']
                
                current_balance = (inv_amt - pay_amt)

                date_str = item['date'].strftime('%Y-%m-%d') if item['date'] else ''
                sheet.write(row, 0, date_str, normal)
                sheet.write(row, 1, inv_amt if inv_amt > 0 else '', amount_format)
                sheet.write(row, 2, pay_amt if pay_amt > 0 else '', amount_format)
                sheet.write(row, 3, current_balance, amount_format)
                # sheet.write(row, 4, '', amount_format)
                
                row += 1
                year_invoice_total += inv_amt
                year_payment_total += pay_amt

            # Year Totals (المجموع)
            sheet.write(row, 0, 'المجموع', header)
            sheet.write(row, 1, year_invoice_total, header)
            sheet.write(row, 2, year_payment_total, header)
            sheet.write(row, 3, '', header)
            sheet.write(row, 4, '', header)
            row += 1
            
            # Total Installment (القسط الكلي)
            sheet.write(row, 0, 'القسط الكلي', header)
            sheet.write(row, 1, '', header)
            sheet.write(row, 2, '', header)
            sheet.write(row, 3, '', header)
            sheet.write(row, 4, year_installment_total, header)
            row += 2

            grand_invoice_total += year_invoice_total
            grand_payment_total += year_payment_total

        # Grand Balance
        final_balance = grand_invoice_total - grand_payment_total
        sheet.write(row, 0, 'الرصيد النهائي (Balance)', header)
        sheet.write(row, 1, final_balance, header)

        workbook.close()
        output.seek(0)

        # Wrap file saving in a savepoint too, to be 100% safe
        try:
            with self.env.cr.savepoint():
                self.file_name = 'Account_Statement.xlsx'
                self.file_data = base64.b64encode(output.read())
        except Exception as e:
            print("Error saving file to wizard:", e)

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=%s&id=%s&field=file_data&download=true&filename=%s'
                   % (self._name, self.id, self.file_name),
            'target': 'self',
        }