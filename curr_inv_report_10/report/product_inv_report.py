# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.

# import logging
# from datetime import timedelta
# from datetime import datetime
# from functools import partial

# import psycopg2
# import pytz

# from odoo import api, fields, models, tools, _
# from odoo.tools import float_is_zero
# from odoo.exceptions import UserError
# from odoo.http import request
# import odoo.addons.decimal_precision as dp
# from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

# _logger = logging.getLogger(__name__)

# class ProdInvReportXlsx(ReportXlsx):
#     def generate_xlsx_report(self, workbook, data, cust_invoices):
#         import sys
#         reload(sys)
#         sys.setdefaultencoding('utf8')

#         search_arr = []
#         search_arr.append(('qty', '>', 0))
#         if data['product']:
#             products = data['product']
#             search_arr.append(('product_id', '=', products))

#         sr_no = 0
#         stock_history_list = []

#         for shl in self.env['stock.quant'].search(search_arr, order='product_id ASC'):
#             sr_no = sr_no + 1

#             stock_location = shl.location_id.name
#             product_id = shl.product_id.id
#             product = shl.product_id.name
#             company = shl.company_id.name
#             default_code = shl.product_id.default_code
#             unit_of_measure = shl.product_uom_id.name
#             quantity = shl.qty
#             inventory_value = shl.inventory_value
#             cost_price = shl.product_id.standard_price
#             sale_price = shl.product_id.lst_price

#             result = [
#                 sr_no,
#                 stock_location,
#                 default_code,
#                 unit_of_measure,
#                 quantity,
#                 inventory_value,
#                 product_id,
#                 product,
#                 cost_price,
#                 sale_price
#             ]

#             stock_history_list.append(result)

#         worksheet = workbook.add_worksheet()
#         head_option = workbook.add_format({'bold': 1, 'bg_color': '#fdd5b1', 'border': 1, 'border_color': '#000000', 'font_size': 12})
#         head_option2 = workbook.add_format({'bold': 1, 'bg_color': '#fdd5b1', 'border': 1, 'border_color': '#000000', 'font_size': 12, 'align': 'center'})
#         date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
#         worksheet.write('A1', 'Sr. No.', head_option)
#         worksheet.write('B1', 'Product', head_option)
#         worksheet.write('C1', 'Default Code', head_option)
#         worksheet.write('D1', 'Cost Price', head_option)
#         worksheet.write('E1', 'Sale Price', head_option)
#         worksheet.write('F1', 'Unit of Measure', head_option)
#         worksheet.write('G1', 'QTY on hand', head_option)

#         row = 1
#         col = 0

#         for sr_no, stock_location, default_code, unit_of_measure, quantity, inventory_value, product_id, product, cost_price, sale_price in (stock_history_list):
#             sr_no = str(sr_no)
#             worksheet.write(row, col, sr_no)
#             worksheet.write(row, col+1, product)
#             worksheet.write(row, col+2, default_code)
#             worksheet.write(row, col+3, cost_price)
#             worksheet.write(row, col+4, sale_price)
#             worksheet.write(row, col+5, unit_of_measure)
#             worksheet.write(row, col+6, quantity)
#             row += 1

#         worksheet.write(row, col, 'Total')
#         c_format = 'D'+str(row)
#         d_format = 'E'+str(row)
#         f_format = 'G'+str(row)

#         worksheet.write_formula(row, col+3, '=SUM(D2:'+c_format+')')
#         worksheet.write_formula(row, col+4, '=SUM(E2:'+d_format+')')
#         worksheet.write_formula(row, col+6, '=SUM(G2:'+f_format+')')

#         workbook.close()

# ProdInvReportXlsx('report.prod_inv.sale.order.xlsx', 'sale.order')
