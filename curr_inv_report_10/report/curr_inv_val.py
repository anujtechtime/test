# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from datetime import timedelta
from datetime import datetime
from functools import partial

import psycopg2
import pytz

from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
from odoo.http import request
import odoo.addons.decimal_precision as dp
# from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

_logger = logging.getLogger(__name__)

class curr_inv_val_pdf_report(models.AbstractModel):
    _name = 'report.stock.curr_inv_report_pdf'

    @api.model
    def curr_inv_report_pdf_tr(self, data):
        import sys
        reload(sys)
        sys.setdefaultencoding('utf8')

        search_arr = []
        is_stock_move = "no"
        if data['is_stock_move']:
            is_stock_move = data['is_stock_move']
        if data['product']:
            products = data['product']
            search_arr.append(('product_id', '=', products))
        if data['gold_purity']:
            product_uom = data['gold_purity']
            search_arr.append(('gold_purity', '=', product_uom))
        if data['location_id']:
            location_id = data['location_id']
            search_arr.append(('location_id', '=', location_id))

        sr_no = 0
        stock_history_list = []
        stock_history_list_final = []

        for shl in self.env['stock.quant'].search(search_arr, order='product_id ASC'):
            if data['make']:
                if data['make'] != shl.product_id.make:
                    continue
            if data['categ_id']:
                if data['categ_id'] != shl.product_id.categ_id.id:
                    continue
            if shl.product_id.categ_id.id in (1,2,56,57,58):
                continue
            stock_location = shl.location_id.name
            stock_loc_usage = shl.location_id.usage
            product_id = shl.product_id.id
            product = shl.product_id.name
            barcode = shl.product_id.barcode
            gold_gram = shl.gold_gram
            gold_purity = shl.product_id.gold_purity
            company = shl.location_id.company_id.name
            incoming_date = shl.in_date
            unit_of_measure = shl.product_uom_id.name
            quantity = shl.qty
            inventory_value = shl.inventory_value
            category = shl.product_id.categ_id.name
            make = shl.product_id.make

            if stock_loc_usage == "internal" and quantity != 0:
                result = [
                    stock_location,
                    company,
                    incoming_date,
                    unit_of_measure,
                    quantity,
                    inventory_value,
                    product_id,
                    product,
                    gold_gram,
                    gold_purity,
                    barcode,
                    category,
                    make
                ]
                stock_history_list.append(result)

        total_quantity = {}
        total_inventory_val = {}
        total_gold_gram = {}
        for stock_location, company, incoming_date, unit_of_measure, quantity, inventory_value, product_id, product, gold_gram, gold_purity, barcode, category, make in (stock_history_list):
            if product_id in total_quantity:
                total_quantity[product_id] = total_quantity[product_id] + quantity
                total_inventory_val[product_id] = total_inventory_val[product_id] + inventory_value
                total_gold_gram[product_id] = total_gold_gram[product_id] + (gold_gram * quantity)
            else:
                total_quantity[product_id] = quantity
                total_inventory_val[product_id] = inventory_value
                total_gold_gram[product_id] = gold_gram * quantity

        default_product_id = 0
        main_total_quantity = 0
        main_total_inventory_val = 0
        main_total_gold_gram = 0
        for stock_location, company, incoming_date, unit_of_measure, quantity, inventory_value, product_id, product, gold_gram, gold_purity, barcode, category, make in (stock_history_list):
            if total_quantity[product_id] == 0:
                continue
            if default_product_id != product_id:
                default_product_id = product_id
                sr_no = sr_no + 1
                result = {
                    'sr_no': sr_no,
                    'stock_location': stock_location,
                    'company': company,
                    'incoming_date': incoming_date,
                    'unit_of_measure': unit_of_measure,
                    'quantity': total_quantity[product_id],
                    'inventory_value': total_inventory_val[product_id],
                    'product_id': product_id,
                    'product': product,
                    'gold_gram': gold_gram,
                    'gold_gram_subtotal': total_gold_gram[product_id],
                    'gold_purity': gold_purity,
                    'barcode': barcode,
                    'category': category,
                    'make': make
                }
                stock_history_list_final.append(result)

                main_total_quantity += total_quantity[product_id]
                main_total_inventory_val += total_inventory_val[product_id]
                main_total_gold_gram += total_gold_gram[product_id]

        return {
            'curr_inv_report_pdf_row': stock_history_list_final,
            'total_qty': main_total_quantity,
            'total_gold_gram': main_total_gold_gram,
            'total_inventory_val': main_total_inventory_val,
            'is_stock_move': is_stock_move
        }

    def render_html(self, docids, data=None):
        data = dict(data or {})
        data.update(self.curr_inv_report_pdf_tr(data))
        return self.env['report'].render('stock.curr_inv_report_pdf', data)

# class DOReportXlsx(ReportXlsx):
#     def generate_xlsx_report(self, workbook, data, cust_invoices):
#         import sys
#         reload(sys)
#         sys.setdefaultencoding('utf8')

#         search_arr = []
#         is_stock_move = "no"
#         if data['is_stock_move']:
#             is_stock_move = data['is_stock_move']
#         if data['product']:
#             products = data['product']
#             search_arr.append(('product_id', '=', products))
#         if data['gold_purity']:
#             product_uom = data['gold_purity']
#             search_arr.append(('gold_purity', '=', product_uom))
#         if data['location_id']:
#             location_id = data['location_id']
#             search_arr.append(('location_id', '=', location_id))

#         sr_no = 0
#         stock_history_list = []

#         for shl in self.env['stock.quant'].search(search_arr, order='product_id ASC'):
#             if data['make']:
#                 if data['make'] != shl.product_id.make:
#                     continue
#             if data['categ_id']:
#                 if data['categ_id'] != shl.product_id.categ_id.id:
#                     continue
#             if shl.product_id.categ_id.id in (1,2,56,57,58):
#                 continue
#             stock_location = shl.location_id.name
#             stock_loc_usage = shl.location_id.usage
#             product_id = shl.product_id.id
#             product = shl.product_id.name
#             barcode = shl.product_id.barcode
#             gold_gram = shl.gold_gram
#             gold_purity = shl.product_id.gold_purity
#             company = shl.location_id.company_id.name
#             incoming_date = shl.in_date
#             unit_of_measure = shl.product_uom_id.name
#             quantity = shl.qty
#             inventory_value = shl.inventory_value
#             category = shl.product_id.categ_id.name
#             make = shl.product_id.make

#             if stock_loc_usage == "internal" and quantity != 0:
#                 result = [
#                     stock_location,
#                     company,
#                     incoming_date,
#                     unit_of_measure,
#                     quantity,
#                     inventory_value,
#                     product_id,
#                     product,
#                     gold_gram,
#                     gold_purity,
#                     barcode,
#                     category,
#                     make
#                 ]

#                 stock_history_list.append(result)

#         worksheet = workbook.add_worksheet()
#         #head_option = workbook.add_format({'bold': 1, 'bg_color': '#fdd5b1', 'border': 1, 'border_color': '#000000', 'font_size': 12})
#         #head_option2 = workbook.add_format({'bold': 1, 'bg_color': '#fdd5b1', 'border': 1, 'border_color': '#000000', 'font_size': 12, 'align': 'center'})
#         head_option = workbook.add_format({'font_size': 12})
#         head_option2 = workbook.add_format({'font_size': 12})
#         date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
#         worksheet.write('A1', 'Sr. No.', head_option)
#         worksheet.write('B1', 'Product', head_option)
#         worksheet.write('C1', 'Barcode', head_option)
#         worksheet.write('D1', 'Weight', head_option)
#         worksheet.write('E1', 'Purity', head_option)
#         worksheet.write('F1', 'Company', head_option)
#         worksheet.write('G1', 'Incoming Date', head_option)
#         worksheet.write('H1', 'Make', head_option)
#         worksheet.write('I1', 'Internal Category', head_option)
#         worksheet.write('J1', 'Product QTY', head_option)
#         worksheet.write('K1', 'Inventory Value', head_option)
#         worksheet.write('L1', 'Subtotal Weight', head_option)
#         if is_stock_move == "yes":
#             worksheet.write('M1', 'Stock Location', head_option)

#         row = 1
#         col = 0

#         total_quantity = {}
#         total_inventory_val = {}
#         total_gold_gram = {}
#         for stock_location, company, incoming_date, unit_of_measure, quantity, inventory_value, product_id, product, gold_gram, gold_purity, barcode, category, make in (stock_history_list):
#             if product_id in total_quantity:
#                 total_quantity[product_id] = total_quantity[product_id] + quantity
#                 total_inventory_val[product_id] = total_inventory_val[product_id] + inventory_value
#                 total_gold_gram[product_id] = total_gold_gram[product_id] + (gold_gram * quantity)
#             else:
#                 total_quantity[product_id] = quantity
#                 total_inventory_val[product_id] = inventory_value
#                 total_gold_gram[product_id] = gold_gram * quantity

#         default_product_id = 0
#         main_total_quantity = 0
#         main_total_inventory_val = 0
#         main_total_gold_gram = 0
#         for stock_location, company, incoming_date, unit_of_measure, quantity, inventory_value, product_id, product, gold_gram, gold_purity, barcode, category, make in (stock_history_list):
#             if total_quantity[product_id] == 0:
#                 continue
#             if default_product_id != product_id:
#                 default_product_id = product_id
#                 sr_no = sr_no + 1
#                 worksheet.write(row, col, sr_no, head_option)
#                 worksheet.write(row, col+1, product, head_option)
#                 worksheet.write(row, col+2, barcode, head_option)
#                 worksheet.write(row, col+3, gold_gram, head_option)
#                 worksheet.write(row, col+4, gold_purity, head_option)
#                 worksheet.write(row, col+5, '', head_option)
#                 worksheet.write(row, col+6, '', head_option)
#                 worksheet.write(row, col+7, make, head_option)
#                 worksheet.write(row, col+8, category, head_option)
#                 worksheet.write(row, col+9, total_quantity[product_id], head_option)
#                 worksheet.write(row, col+10, total_inventory_val[product_id], head_option)
#                 worksheet.write(row, col+11, total_gold_gram[product_id], head_option)

#                 main_total_quantity += total_quantity[product_id]
#                 main_total_inventory_val += total_inventory_val[product_id]
#                 main_total_gold_gram += total_gold_gram[product_id]

#                 if is_stock_move == "yes":
#                     worksheet.write(row, col+12, stock_location, head_option)
#                 row += 1

#             # sr_no = str(sr_no)
#             # worksheet.write(row, col, sr_no)
#             # worksheet.write(row, col+1, product)
#             # worksheet.write(row, col+2, barcode)
#             # worksheet.write(row, col+3, gold_gram)
#             # worksheet.write(row, col+4, company)
#             # worksheet.write(row, col+5, incoming_date, date_format)
#             # worksheet.write(row, col+6, unit_of_measure)
#             # worksheet.write(row, col+7, quantity)
#             # worksheet.write(row, col+8, inventory_value)
#             # if is_stock_move == "yes":
#             #     worksheet.write(row, col+9, stock_location)
#             # row += 1

#         worksheet.write(row, col+8, "Total", head_option)
#         worksheet.write(row, col+9, main_total_quantity, head_option)
#         worksheet.write(row, col+10, main_total_inventory_val, head_option)
#         worksheet.write(row, col+11, main_total_gold_gram, head_option)

#         workbook.close()

# DOReportXlsx('report.cur_inv.sale.order.xlsx', 'sale.order')
