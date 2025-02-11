# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
import logging
import pytz
import threading
from collections import OrderedDict, defaultdict
from datetime import date, datetime, timedelta
from psycopg2 import sql
from geopy.geocoders import Nominatim
import calendar
import xml.dom.minidom
from bs4 import BeautifulSoup
import re
from prettytable import PrettyTable
import pandas as pd
from dateutil.relativedelta import relativedelta

import base64
from dateutil import rrule
from translate import Translator
import convert_numbers
import xlwt
import io
from lxml import etree
import html2text

import requests
import json
from odoo import api, fields, models, tools, SUPERUSER_ID

_logger = logging.getLogger(__name__)

class MrpProductSale(models.Model):
    _inherit = 'sale.order'

    year_of_acceptance_1 = fields.Many2one("techtime_mcc_data.techtime_mcc_data", string="Year of acceptance", related="partner_id.year_of_acceptance_1")

class MrpProductPayment(models.Model):
    _inherit = 'account.payment'

    casher = fields.Selection([('option1', 'حسين'),('option2','مسلم حسن'),('option3','مصطفى يوسف'),('option4','عبد الكاظم')], string="الكاشير")

    casher_bool = fields.Boolean(string="اشتراك نادي الطلبة")

class MrpProductWizard(models.TransientModel):
    _name = 'trail.balance.wizard'

   
    date_start = fields.Date("Date Start")
    date_end = fields.Date("Date End")

    # Method to mark the mrp orders as done
    def action_done(self):
        filename = 'جدول الاحصاء الصباحي.xls'
        string = 'جدول الاحصاء الصباحي.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        worksheet = wb.add_sheet(string , cell_overwrite_ok=True)
        worksheet.cols_right_to_left = True
        header_bold = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour gray25;")
        cell_format = xlwt.easyxf()
        filename = 'Accounting Trial Balance %s.xls' % date.today()
        row = 1
        border_normal = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; font: bold on; pattern: pattern solid, fore_colour gray25;')
        border_1 = xlwt.easyxf('borders: left 1, right 1, top 1, bottom 1;')
        border_2 = xlwt.easyxf('borders: left 2, right 2, top 2, bottom 2;')
        border_color_2 = xlwt.easyxf('borders: top_color blue, bottom_color blue, right_color blue, left_color blue, left 2, right 2, top 2, bottom 2; font: bold on; pattern: pattern solid, fore_colour gray25;')
        # worksheet.col(0).width = 10000
        # worksheet.col(1).width = 15000
        # worksheet.col(2).width = 10000
        worksheet.col(0).width = 5000
        worksheet.col(1).width = 5000

        header_bold = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour gray25; align: horiz centre; font: bold 1,height 240;")


        header_bold_main_header = xlwt.easyxf("font: bold on, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; align: horiz centre; align: vert centre")


        
        main_cell_total = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour ivory; align: horiz centre; align: vert centre")


        main_cell_total_of_total = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour lime; align: horiz centre; align: vert centre")

        rows = 1
        col = 0

        worksheet.write_merge(0, 0, 1, 7, "ميزان مرجعة تفصيلي :جامعه المعقل " or '', header_bold)

        worksheet.write_merge(1, 2, 0, 1, "الدليل " or '', header_bold)


        count = 1

        total_debit = 0
        total_credit = 0
        total_balance = 0
        codde = 0

        # if self.date_start.month == 1:
        #     self.date_end = self.date_start
        if self.date_start.month == 2:
            self.date_end = self.date_start  
            self.date_start = self.date_start.replace(month=1)  
        if self.date_start and not self.date_end:
            for x in range(2):
                if x == 0:
                    if self.date_start.month == 1:
                        start_date =  self.date_start.replace(day=1, month=1, year=self.date_start.year - 1).strftime('%Y/%m/%d')
                        start = str(self.date_start.replace(day=1, month=1, year=self.date_start.year - 1).strftime('%Y/%m'))
                        end = str(self.date_start.replace(day=1, month=12, year=self.date_start.year - 1).strftime('%Y/%m'))

                        given_month = start + "-" + end

                        # Get the name of the month
                        # month_name = calendar.month_name[given_month]

                    if self.date_start.month != 1:    
                        start_date =  self.date_start.replace(day=1, month=1).strftime('%Y/%m/%d')
                        start = str(self.date_start.strftime('%Y/%m'))

                        given_month = int(start[5:7]) - 1

                        # Get the name of the month
                        month_name = calendar.month_name[given_month]
                    end_date = self.date_start.replace(day=1).strftime('%Y/%m/%d')
                    rows = 1
                    data = 0
                    only_debit = 0
                    only_credit = 0
                    groups = {}


                    worksheet.write(rows + 1 , col +2, "مدين", main_cell_total_of_total)
                    worksheet.write(rows + 1 , col + 3 , "دائن ", main_cell_total_of_total)
                    # worksheet.write(rows + 1 , col + 4 , "Balance", main_cell_total_of_total)

                    worksheet.write_merge(rows , rows , col + 2, col + 3 , "مدور شهر (%s)" % given_month, main_cell_total)
                    # worksheet.write_merge(0, 0, 1, 7, "Al-Maaqal University:   Detailed Trial Balance" or '', header_bold)

                    account_result = {}
                    accounts = self.env['account.account'].search([])
                    

                    tables, where_clause, where_params = self.env['account.move.line']._query_get()
                    tables = tables.replace('"', '')
                    if not tables:
                        tables = 'account_move_line'
                    wheres = [""]
                    if where_clause.strip():
                        wheres.append(where_clause.strip())
                    filters = " AND ".join(wheres)
                    # compute the balance, debit and credit for the provided accounts
                    request = (
                    "SELECT account_id AS id, SUM(debit) AS debit, SUM(credit) AS credit, (SUM(debit) - SUM(credit)) AS balance" + \
                    " FROM " + tables + " WHERE account_id IN %s " + filters + "AND date >= '" + start_date + "' AND date < '" + end_date + "' GROUP BY account_id")
                    params = (tuple(accounts.ids),) + tuple(where_params)
                    self.env.cr.execute(request, params)
                    for row in self.env.cr.dictfetchall():
                        account_result[row.pop('id')] = row

                    account_res = []
                    groupsse = {}
                    groupss = {}
                    grs = {}
                    for account in accounts:
                        res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance']) 
                        currency = account.currency_id and account.currency_id or account.company_id.currency_id
                        res['code'] = account.code
                        res['name'] = account.name
                        res["group_id"] = account.group_id.name
                        print("res@@@@@@@@@@@@@@@@@@",res)

                        if account.code[:3] in grs:
                            # If the key already exists, append the item to the list
                            grs[account.code[:3]].append(res['group_id'])
                            if res['group_id'] == False:
                                grs[account.code[:3]] = [res['group_id']]
                        else:
                            # If the key doesn't exist, create a new list with the item
                            grs[account.code[:3]] = [res['group_id']]
                        if account.id in account_result:
                            res['debit'] = account_result[account.id].get('debit')
                            res['credit'] = account_result[account.id].get('credit')
                            res['balance'] = account_result[account.id].get('balance')
                            account_res.append(res)   

                            # if col == 0:
                            #     worksheet.write(rows + 2 , col , res['code'][:3] , header_bold_main_header)
                            #     worksheet.write(rows + 2 , col + 1 , res['name'] , header_bold_main_header)
                                

                            # Iterate through the list
                        if account.code[:3] in groupss:
                            # If the key already exists, append the item to the list
                            groupss[account.code[:3]].append(res)
                        else:
                            # If the key doesn't exist, create a new list with the item
                            groupss[account.code[:3]] = [res]

                    print("grs@@@@@@@@@@@@@@@@",grs)


                    for key, value in groupss.items():
                        values = groupss[key]
                        if col == 0:
                            worksheet.write(rows + 2 , col , key , header_bold_main_header)
                            print("key@@@@@@@@@@@@@@@@",key)
                            print("grs[key][-1]@@@@@@@@@@@@@@@",grs[key])
                            if grs[key][-1] != False:
                                worksheet.write(rows + 2 , col + 1 , grs[key][-1] , header_bold_main_header)
                        exit_code = 0
                        total_debit = 0
                        total_credit = 0
                        total_balance = 0
                        for ddst in values:
                            if col == 0  and grs[key][-1] != False:
                                worksheet.write(rows + 2 , col + 1 , grs[key][-1] , header_bold_main_header)
                            total_debit = total_debit +  ddst['debit']
                            total_credit = total_credit + ddst['credit']
                            total_balance = total_balance + ddst['balance']


                        if key in groupsse:
                            # If the key already exists, append the item to the list
                            groupsse[key].append(total_balance)
                        else:
                            # If the key doesn't exist, create a new list with the item
                            groupsse[key] = [total_balance]

                        if total_balance > 0:    
                            worksheet.write(rows + 2 , col + 2 , total_balance, header_bold_main_header)
                            worksheet.write(rows + 2 , col + 3 , "" , header_bold_main_header)
                            only_debit = only_debit + total_balance

                        if total_balance < 0:       
                            worksheet.write(rows + 2 , col + 3 , abs(total_balance) , header_bold_main_header)
                            worksheet.write(rows + 2 , col + 2 , "" , header_bold_main_header)
                            only_credit = only_credit + abs(total_balance)
                        if total_balance == 0:
                            worksheet.write(rows + 2 , col + 2 , "" , header_bold_main_header)
                            worksheet.write(rows + 2 , col + 3 , "" , header_bold_main_header)    
                        # only_debit = only_debit + total_debit
                        # only_credit = only_credit + total_credit
                        # worksheet.write(rows + 2 , col + 4 , total_balance, header_bold_main_header)
                        rows = rows + 1
                    

                    worksheet.write(rows + 2 , col + 2 , only_debit, header_bold_main_header)
                    worksheet.write(rows + 2 , col + 3 , only_credit , header_bold_main_header)
                    col = col + 2
                    only_debit_for_sum = only_debit
                    only_credit_for_sum = only_credit
                else:
                    start_date =  self.date_start.replace(day=1).strftime('%Y/%m/%d')
                    end_date =  str((self.date_start.replace(day=1) + relativedelta(months=1)).strftime('%Y/%m/%d'))
                    rows = 1
                    data = 0
                    only_debit = 0
                    only_credit = 0
                    only_balance = 0
                    only_balance_debit = 0
                    only_balance_credit = 0
                    groups = {}
                    # start = str(dt.strftime('%Y/%m'))

                    # given_month = int(start[5:7])

                    # # Get the name of the month
                    month_name = calendar.month_name[self.date_start.month]


                    worksheet.write(rows + 1 , col +2, "مدين ", main_cell_total_of_total)
                    worksheet.write(rows + 1 , col + 3 , "دائن ", main_cell_total_of_total)
                    # worksheet.write(rows + 1 , col + 4 , "Balance", main_cell_total_of_total)

                    worksheet.write_merge(rows , rows , col + 2, col + 3 , "شهر (%s)" % self.date_start.month, main_cell_total)
                    # worksheet.write_merge(0, 0, 1, 7, "Al-Maaqal University:   Detailed Trial Balance" or '', header_bold)

                    account_result = {}
                    accounts = self.env['account.account'].search([])
                    

                    tables, where_clause, where_params = self.env['account.move.line']._query_get()
                    tables = tables.replace('"', '')
                    if not tables:
                        tables = 'account_move_line'
                    wheres = [""]
                    if where_clause.strip():
                        wheres.append(where_clause.strip())
                    filters = " AND ".join(wheres)
                    # compute the balance, debit and credit for the provided accounts
                    request = (
                    "SELECT account_id AS id, SUM(debit) AS debit, SUM(credit) AS credit, (SUM(debit) - SUM(credit)) AS balance" + \
                    " FROM " + tables + " WHERE account_id IN %s " + filters + "AND date >= '" + start_date + "' AND date < '" + end_date + "' GROUP BY account_id")
                    params = (tuple(accounts.ids),) + tuple(where_params)
                    self.env.cr.execute(request, params)
                    for row in self.env.cr.dictfetchall():
                        account_result[row.pop('id')] = row

                    account_res = []
                    groupss = {}
                    grs = {}
                    for account in accounts:
                        res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance']) 
                        currency = account.currency_id and account.currency_id or account.company_id.currency_id
                        res['code'] = account.code
                        res['name'] = account.name
                        res["group_id"] = account.group_id.name

                        if account.code[:3] in grs:
                            # If the key already exists, append the item to the list
                            grs[account.code[:3]].append(res['name'])
                        else:
                            # If the key doesn't exist, create a new list with the item
                            grs[account.code[:3]] = [res['name']]
                        if account.id in account_result:
                            res['debit'] = account_result[account.id].get('debit')
                            res['credit'] = account_result[account.id].get('credit')
                            res['balance'] = account_result[account.id].get('balance')
                            account_res.append(res)   

                            # if col == 0:
                            #     worksheet.write(rows + 2 , col , res['code'][:3] , header_bold_main_header)
                            #     worksheet.write(rows + 2 , col + 1 , res['name'] , header_bold_main_header)
                                

                            # Iterate through the list
                        if account.code[:3] in groupss:
                            # If the key already exists, append the item to the list
                            groupss[account.code[:3]].append(res)
                        else:
                            # If the key doesn't exist, create a new list with the item
                            groupss[account.code[:3]] = [res]




                    for key, value in groupss.items():
                        values = groupss[key]
                        if col == 0:
                            worksheet.write(rows + 2 , col , key , header_bold_main_header)
                            worksheet.write(rows + 2 , col + 1 , grs[key] , header_bold_main_header)
                        exit_code = 0
                        total_debit = 0
                        total_credit = 0
                        total_balance = 0
                        for ddst in values:
                            if col == 0:
                                worksheet.write(rows + 2 , col + 1 , ddst['name'] , header_bold_main_header)
                            total_debit = total_debit +  ddst['debit']
                            total_credit = total_credit + ddst['credit']
                            total_balance = total_balance + ddst['balance']
                        worksheet.write(rows + 2 , col + 2 , total_debit, header_bold_main_header)
                        worksheet.write(rows + 2 , col + 3 , total_credit , header_bold_main_header)
                        # worksheet.write(rows + 2 , col + 4 , total_balance, header_bold_main_header)
                        rows = rows + 1

                        only_debit = only_debit + total_debit
                        only_credit = only_credit + total_credit
                        only_balance = only_balance + total_balance
                        # worksheet.write(rows + 2 , col + 4 , total_balance, header_bold_main_header)
                        # rows = rows + 1
                    

                    worksheet.write(rows + 2 , col + 2 , only_debit, header_bold_main_header)
                    worksheet.write(rows + 2 , col + 3 , only_credit , header_bold_main_header)    
                    col = col + 2
                    only_debit_for_sum = only_debit_for_sum + only_debit
                    only_credit_for_sum = only_credit_for_sum + only_credit
                    print("only_debit_for_sum@@@@@@@@@@@@@",only_debit_for_sum)
                    print("only_credit_for_sum@@@@@@@@@@@@",only_credit_for_sum)
                    rows = 1
                    # worksheet.write_merge(rows , rows , col + 2, col + 4 , "Total Sum" , main_cell_total)
                    worksheet.write_merge(rows , rows , col + 2, col + 3 , "مجموع الرصيد " , main_cell_total)
                    worksheet.write_merge(rows , rows , col + 4, col + 5 , "الرصيد " , main_cell_total)

                    worksheet.write_merge(rows -1 , rows - 1, col + 2, col + 4 , "الحركات المرحلة فقط ")

                    col = col + 2



                    worksheet.write(rows + 1 , col , "مدين " , main_cell_total_of_total)
                    worksheet.write(rows + 1 , col + 1 , "دائن ", main_cell_total_of_total)
                    worksheet.write(rows + 1 , col + 2 , "مدين ", main_cell_total_of_total)
                    worksheet.write(rows + 1 , col + 3 , "دائن ", main_cell_total_of_total)


                    start = str(self.date_start.replace(day=1).strftime('%Y/%m/%d'))
                    end = str((self.date_start.replace(day=1) + relativedelta(months=1)).strftime('%Y/%m/%d'))

                    # compute the balance, debit and credit for the provided accounts
                    request = (
                                "SELECT account_id AS id, SUM(debit) AS debit, SUM(credit) AS credit, (SUM(debit) - SUM(credit)) AS balance" + \
                                " FROM " + tables + " WHERE account_id IN %s " + filters + "AND date >= '" + start + "' AND date < '" + end + "' GROUP BY account_id")
                    params = (tuple(accounts.ids),) + tuple(where_params)
                    self.env.cr.execute(request, params)
                    for row in self.env.cr.dictfetchall():
                        account_result[row.pop('id')] = row

                    account_res = []
                    groupss_total = {}
                    for account in accounts:
                        res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance']) 
                        currency = account.currency_id and account.currency_id or account.company_id.currency_id
                        res['code'] = account.code
                        res['name'] = account.name
                        if account.id in account_result:
                            res['debit'] = account_result[account.id].get('debit')
                            res['credit'] = account_result[account.id].get('credit')
                            res['balance'] = account_result[account.id].get('balance')
                            account_res.append(res)   

                        if account.code[:3] in groupss_total:
                            # If the key already exists, append the item to the list
                            groupss_total[account.code[:3]].append(res)
                        else:
                            # If the key doesn't exist, create a new list with the item
                            groupss_total[account.code[:3]] = [res]


                    for key, value in groupss_total.items():
                        values = groupss_total[key]

                        exit_code = 0
                        total_debit = 0
                        total_credit = 0
                        total_balance = 0
                        for ddstk in values:
                            total_debit = total_debit +  ddstk['debit']
                            total_credit = total_credit + ddstk['credit']
                            total_balance = total_balance + ddstk['balance']
                            # worksheet.write(rows + 2 , col , key, header_bold_main_header)
                            # worksheet.write(rows + 2 , col + 1 , ddst['name'], header_bold_main_header)
                        balance_cal = int(groupsse[key][0])    
                        if balance_cal > 0:
                            worksheet.write(rows + 2 , col , total_debit + balance_cal, header_bold_main_header)
                            worksheet.write(rows + 2 , col + 1 , total_credit , header_bold_main_header)

                            only_balance_debit = only_balance_debit + (total_debit + balance_cal - total_credit)
                            worksheet.write(rows + 2 , col + 2 , total_debit + balance_cal - total_credit, header_bold_main_header)
                            only_debit = only_debit + total_balance
                            worksheet.write(rows + 2 , col + 3 , "0" , header_bold_main_header) 

                        if balance_cal < 0:    
                            worksheet.write(rows + 2 , col , total_debit, header_bold_main_header)
                            worksheet.write(rows + 2 , col + 1 , total_credit + abs(balance_cal), header_bold_main_header)


                            only_balance_credit = only_balance_credit + (total_credit + abs(balance_cal) - total_debit)
                            worksheet.write(rows + 2 , col + 3 , total_credit + abs(balance_cal) - total_debit, header_bold_main_header)
                            worksheet.write(rows + 2 , col + 2 , "0" , header_bold_main_header)
                            only_credit = only_credit + abs(total_balance)

                        if balance_cal == 0 and total_debit > 0 and total_credit > 0:  
                            # only_debit = only_debit + total_debit
                            # only_credit = only_credit + total_credit  
                            worksheet.write(rows + 2 , col , total_debit, header_bold_main_header)
                            worksheet.write(rows + 2 , col + 1 , total_credit, header_bold_main_header)
                            worksheet.write(rows + 2 , col + 2 , "0" , header_bold_main_header)
                            worksheet.write(rows + 2 , col + 3 , "0" , header_bold_main_header)

                        if balance_cal == 0 and total_debit == 0 and total_credit == 0:   

                            worksheet.write(rows + 2 , col , "0", header_bold_main_header)
                            worksheet.write(rows + 2 , col + 1 , "0", header_bold_main_header)
                            worksheet.write(rows + 2 , col + 2 , "0" , header_bold_main_header)
                            worksheet.write(rows + 2 , col + 3 , "0" , header_bold_main_header)    
                        # worksheet.write(rows + 2 , col + 4 , total_balance, header_bold_main_header)
                        # rows = rows + 1

                        # only_debit = only_debit + total_debit
                        # only_credit = only_credit + total_credit
                        # only_balance = only_balance + total_balance
                        # # worksheet.write(rows + 2 , col + 4 , total_balance, header_bold_main_header)
                        # # rows = rows + 1
                    
                        # print("groupsse@@@@@@@@@@@@@@@@@",groupsse)
                        # dddddddddddd


                        # worksheet.write(rows + 2 , col , total_debit, header_bold_main_header)
                        # worksheet.write(rows + 2 , col + 1 , total_credit , header_bold_main_header)
                        
                        # if total_balance > 0:
                        #     only_balance_debit = only_balance_debit + total_balance
                        #     worksheet.write(rows + 2 , col + 2 , total_balance, header_bold_main_header)
                        #     only_debit = only_debit + total_balance
                        #     worksheet.write(rows + 2 , col + 3 , "" , header_bold_main_header)  

                        # if total_balance < 0:
                        #     only_balance_credit = only_balance_credit + total_balance
                        #     worksheet.write(rows + 2 , col + 3 , abs(total_balance), header_bold_main_header)
                        #     worksheet.write(rows + 2 , col + 2 , "" , header_bold_main_header)
                        #     only_credit = only_credit + abs(total_balance)


                        # if total_balance == 0:
                        #     worksheet.write(rows + 2 , col + 2 , "" , header_bold_main_header)
                        #     worksheet.write(rows + 2 , col + 3 , "" , header_bold_main_header)    
                            
                        rows = rows + 1                    
                        # only_debit = only_debit + total_debit
                        # only_credit = only_credit + total_credit
                        
                        
                        # worksheet.write(rows + 2 , col + 4 , total_balance, header_bold_main_header)
                        # rows = rows + 1

                        


                    worksheet.write(rows + 2 , col , only_debit_for_sum, header_bold_main_header)
                    worksheet.write(rows + 2 , col + 1 , only_credit_for_sum , header_bold_main_header)
                    worksheet.write(rows + 2 , col + 2 , only_balance_debit , header_bold_main_header)  
                    worksheet.write(rows + 2 , col + 3 , abs(only_balance_credit) , header_bold_main_header)       

                if col == 2: 
                    worksheet.write_merge(rows + 2, rows + 2 , 0 , 1 , "المجموع", header_bold_main_header)  
        else:
            if self.date_start.month == 1:
                dtstart=self.date_start.replace(day=1, month=12, year=self.date_start.year - 1)
            else:
                dtstart=self.date_start.replace(day=1)    
            for dt in rrule.rrule(rrule.MONTHLY, dtstart=dtstart, until=self.date_end):
                rows = 1
                data = 0
                only_debit = 0
                only_credit = 0
                only_balance = 0 
                only_balance_debit = 0
                only_balance_credit = 0
                groups = {}
                start = str(dt.strftime('%Y/%m'))

                given_month = int(start[5:7])

                # Get the name of the month
                month_name = calendar.month_name[given_month]


                worksheet.write(rows + 1 , col +2, "مدين ", main_cell_total_of_total)
                worksheet.write(rows + 1 , col + 3 , "دائن ", main_cell_total_of_total)
                worksheet.write(rows + 1 , col + 4 , "Balance", main_cell_total_of_total)

                worksheet.write_merge(rows , rows , col + 2, col + 3 , str(start[0:7]), main_cell_total)
                # worksheet.write_merge(0, 0, 1, 7, "Al-Maaqal University:   Detailed Trial Balance" or '', header_bold)

                account_result = {}
                accounts = self.env['account.account'].search([])
                

                tables, where_clause, where_params = self.env['account.move.line']._query_get()
                tables = tables.replace('"', '')
                if not tables:
                    tables = 'account_move_line'
                wheres = [""]
                if where_clause.strip():
                    wheres.append(where_clause.strip())
                filters = " AND ".join(wheres)
                # compute the balance, debit and credit for the provided accounts
                request = (
                            "SELECT account_id AS id, SUM(debit) AS debit, SUM(credit) AS credit, (SUM(debit) - SUM(credit)) AS balance" + \
                            " FROM " + tables + " WHERE account_id IN %s " + filters + "AND TO_CHAR(date, 'YY/MM') = '" + start[2:7] + "' GROUP BY account_id")
                params = (tuple(accounts.ids),) + tuple(where_params)
                self.env.cr.execute(request, params)
                for row in self.env.cr.dictfetchall():
                    account_result[row.pop('id')] = row

                account_res = []
                groupss = {}
                grs = {}
                for account in accounts:
                    res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance']) 
                    currency = account.currency_id and account.currency_id or account.company_id.currency_id
                    res['code'] = account.code
                    res['name'] = account.name
                    res["group_id"] = account.group_id.name

                    if account.code[:3] in grs:
                        # If the key already exists, append the item to the list
                        grs[account.code[:3]].append(res['name'])
                    else:
                        # If the key doesn't exist, create a new list with the item
                        grs[account.code[:3]] = [res['name']]
                    if account.id in account_result:
                        res['debit'] = account_result[account.id].get('debit')
                        res['credit'] = account_result[account.id].get('credit')
                        res['balance'] = account_result[account.id].get('balance')
                        account_res.append(res)   

                        # if col == 0:
                        #     worksheet.write(rows + 2 , col , res['code'][:3] , header_bold_main_header)
                        #     worksheet.write(rows + 2 , col + 1 , res['name'] , header_bold_main_header)
                            

                        # Iterate through the list
                    if account.code[:3] in groupss:
                        # If the key already exists, append the item to the list
                        groupss[account.code[:3]].append(res)
                    else:
                        # If the key doesn't exist, create a new list with the item
                        groupss[account.code[:3]] = [res]



                        # rows = rows + 1
                #         print("res@@@@@@@@@@@@@@@@",res)
                # print("grsgrsgrsgrsgrsgrsgrsgrs",grs)

                for key, value in groupss.items():

                    values = groupss[key]
                    if col == 0:
                            worksheet.write(rows + 2 , col , key , header_bold_main_header)
                            worksheet.write(rows + 2 , col + 1 , grs[key] , header_bold_main_header)
                    exit_code = 0
                    total_debit = 0
                    total_credit = 0
                    total_balance = 0
                    for ddst in values:
                        if col == 0:
                            worksheet.write(rows + 2 , col + 1 , ddst['name'] , header_bold_main_header)
                        total_debit = total_debit +  ddst['debit']
                        total_credit = total_credit + ddst['credit']
                        total_balance = total_balance + ddst['balance']
                    worksheet.write(rows + 2 , col + 2 , total_debit, header_bold_main_header)
                    worksheet.write(rows + 2 , col + 3 , total_credit , header_bold_main_header)
                    # worksheet.write(rows + 2 , col + 4 , total_balance, header_bold_main_header)
                    rows = rows + 1
                    only_debit = only_debit + total_debit
                    only_credit = only_credit + total_credit
                    # worksheet.write(rows + 2 , col + 4 , total_balance, header_bold_main_header)
                


                worksheet.write(rows + 2 , col + 2 , only_debit, header_bold_main_header)
                worksheet.write(rows + 2 , col + 3 , only_credit , header_bold_main_header)
                col = col + 2


            rows = 1
            worksheet.write_merge(rows , rows , col + 2, col + 3 , "مجموع الرصيد " , main_cell_total)
            worksheet.write_merge(rows , rows , col + 4, col + 5 , "الرصيد " , main_cell_total)

            worksheet.write_merge(rows -1 , rows - 1, col + 2, col + 4 , "الحركات المرحلة فقط ")

            col = col + 2



            worksheet.write(rows + 1 , col , "مدين " , main_cell_total_of_total)
            worksheet.write(rows + 1 , col + 1 , "دائن ", main_cell_total_of_total)
            worksheet.write(rows + 1 , col + 2 , "مدين ", main_cell_total_of_total)
            worksheet.write(rows + 1 , col + 3 , "دائن ", main_cell_total_of_total)
            start = str(self.date_start.replace(day=1).strftime('%Y/%m/%d'))
            end = str((self.date_end.replace(day=1) + relativedelta(months=1)).strftime('%Y/%m/%d'))


            # compute the balance, debit and credit for the provided accounts
            request = (
                        "SELECT account_id AS id, SUM(debit) AS debit, SUM(credit) AS credit, (SUM(debit) - SUM(credit)) AS balance" + \
                        " FROM " + tables + " WHERE account_id IN %s " + filters + "AND date >= '" + start + "' AND date < '" + end + "' GROUP BY account_id")
            params = (tuple(accounts.ids),) + tuple(where_params)
            self.env.cr.execute(request, params)
            for row in self.env.cr.dictfetchall():
                account_result[row.pop('id')] = row

            account_res = []
            groupss_total = {}
            for account in accounts:
                res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance']) 
                currency = account.currency_id and account.currency_id or account.company_id.currency_id
                res['code'] = account.code
                res['name'] = account.name
                if account.id in account_result:
                    res['debit'] = account_result[account.id].get('debit')
                    res['credit'] = account_result[account.id].get('credit')
                    res['balance'] = account_result[account.id].get('balance')
                    account_res.append(res)   

                if account.code[:3] in groupss_total:
                    # If the key already exists, append the item to the list
                    groupss_total[account.code[:3]].append(res)
                else:
                    # If the key doesn't exist, create a new list with the item
                    groupss_total[account.code[:3]] = [res]


            for key, value in groupss_total.items():
                print(f"Valuessssssss: {key}, Lengthdddddddddd: {len(value)}")
                print("kkeeeeeeeeeeeeeeeeeeeee",key)
                # print("value################",value)
                values = groupss_total[key]

                exit_code = 0
                total_debit = 0
                total_credit = 0
                total_balance = 0
                for ddstk in values:
                    total_debit = total_debit +  ddstk['debit']
                    total_credit = total_credit + ddstk['credit']
                    total_balance = total_balance + ddstk['balance']
                    # print("ddst#############",ddst)
                    # worksheet.write(rows + 2 , col , key, header_bold_main_header)
                    # worksheet.write(rows + 2 , col + 1 , ddst['name'], header_bold_main_header)
                worksheet.write(rows + 2 , col , total_debit, header_bold_main_header)
                worksheet.write(rows + 2 , col + 1 , total_credit , header_bold_main_header)

                if total_balance > 0:
                    worksheet.write(rows + 2 , col + 2 , total_balance, header_bold_main_header)
                    only_balance_debit = only_balance_debit + total_balance

                if total_balance < 0:
                    worksheet.write(rows + 2 , col + 3 , abs(total_balance), header_bold_main_header)
                    only_balance_credit = only_balance_credit + total_balance
                # else:
                #     worksheet.write(rows + 2 , col + 2 , "", header_bold_main_header)  
                #     worksheet.write(rows + 2 , col + 3 , "", header_bold_main_header)        
                rows = rows + 1
                only_debit = only_debit + total_debit
                only_credit = only_credit + total_credit
                
                # worksheet.write(rows + 2 , col + 4 , total_balance, header_bold_main_header)
            


            worksheet.write(rows + 2 , col , only_debit, header_bold_main_header)
            worksheet.write(rows + 2 , col + 1 , only_credit , header_bold_main_header)
            worksheet.write(rows + 2 , col + 2 , only_balance_debit , header_bold_main_header)
            worksheet.write(rows + 2 , col + 3 , abs(only_balance_credit) , header_bold_main_header)
        if col == 2: 
            worksheet.write_merge(rows + 2, rows + 2 , 0 , 1 , "المجموع", header_bold_main_header) 
        # worksheet.write(rows + 2 , col + 2 , res['debit'])
        # worksheet.write(rows + 2 , col + 3 , res['credit'])
        # worksheet.write(rows + 2 , col + 4 , res['balance'])


                # worksheet.write(1, 1, "القسم" or '', header_bold)

                


        
            # format2 = xlwt.easyxf('font:bold True;align: horiz center')
            
            
            
                # worksheet.write(col ,0 , coll.college or '', main_cell_total)
                # worksheet.write(col ,1 , ddept.department or '', main_cell_total)
                    
                    

        fp = io.BytesIO()
        wb.save(fp)
        print(wb)
        out = base64.encodebytes(fp.getvalue())
        attachment = {
                       'name': str(filename),
                       'display_name': str(filename),
                       'datas': out,
                       'type': 'binary'
                   }
        ir_id = self.env['ir.attachment'].create(attachment) 

        xlDecoded = base64.b64decode(out)

        # file_added = "/home/anuj/Desktop/workspace13/Student_report.xlsx"
        # with open(file_added, "wb") as binary_file:
        #     binary_file.write(xlDecoded)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        download_url = '/web/content/' + str(ir_id.id) + '?download=true'
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }

class payrollDeProductWizard(models.TransientModel):
    _name = 'payroll.department.wizard'

   
    date_from = fields.Date("Date Start")
    date_to = fields.Date("Date End")


    
    def send_mis_report_for_department_new(self):
        filename = 'Payslip.xls'
        string = 'Payslip_report.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        
        translator= Translator(to_lang="Arabic")
        translation = translator.translate(calendar.month_name[date.today().month])



        header_bold = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour gray25; align: horiz centre")


        header_bold_main_header = xlwt.easyxf("font: bold on, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; align: horiz centre; align: vert centre")


        
        main_cell_total = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on; pattern: pattern solid, fore_colour ivory; align: horiz centre")


        main_cell_total_of_total = xlwt.easyxf("font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; font: bold on;  align: horiz centre")


        header_bold_extra_tag = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour green; font: color white; align: horiz centre")

        header_bold_extra = xlwt.easyxf("font: bold on; pattern: pattern solid, fore_colour red; font: color white; align: horiz centre")
        cell_format = xlwt.easyxf()
        filename = 'Payslip_Report_%s.xls' % date.today()
        rested = self.env['hr.payslip'].search([])
        row = 2
        border_normal = xlwt.easyxf('borders: left thin, right thin, top thin, bottom thin; font: bold on; pattern: pattern solid, fore_colour gray25;')
        border_1 = xlwt.easyxf('borders: left 1, right 1, top 1, bottom 1;')
        border_2 = xlwt.easyxf('borders: left 2, right 2, top 2, bottom 2;')
        border_color_2 = xlwt.easyxf('borders: top_color blue, bottom_color blue, right_color blue, left_color blue, left 2, right 2, top 2, bottom 2; font: bold on; pattern: pattern solid, fore_colour gray25;')
        


        # worksheet.col(1).width = 15000
        # worksheet.col(2).width = 10000
        # worksheet.row(0).height = 500
        main_cell = xlwt.easyxf('font: bold off, color black;\
                     borders: top_color black, bottom_color black, right_color black, left_color black,\
                              left thin, right thin, top thin, bottom thin;\
                     pattern: pattern solid, fore_color white; align: horiz centre')

        employe_data =0

        department_data = self.env["hr.department"].search([("parent_id",'=',False)])

        for depp in  department_data:
            worksheet = wb.add_sheet(depp.name, cell_overwrite_ok=True)

            worksheet.paper_size_code = 1

            worksheet.cols_right_to_left = True

            worksheet.col(0).width = 2500
            worksheet.col(2).width = 3000
            worksheet.col(1).width = 4500
            worksheet.col(3).width = 3000
            worksheet.col(4).width = 3000
            worksheet.col(5).width = 3000
            worksheet.col(6).width = 3000
            worksheet.col(7).width = 3000
            worksheet.col(8).width = 3000
            worksheet.col(9).width = 3000
            worksheet.col(10).width = 3000
            worksheet.col(11).width = 3000
            worksheet.col(12).width = 3000
            worksheet.col(13).width = 3000
            worksheet.col(14).width = 3000
            worksheet.col(15).width = 3000
            worksheet.col(16).width = 3000
            worksheet.col(17).width = 3000
            worksheet.col(18).width = 3000
            worksheet.col(19).width = 3000

            row = 6
            call = 4
            # print("department_data#############",depp.id)
            # print("parent_id$$$$$$$$$$$$$$$$$",depp.parent_id)

            partner_data = self.env["hr.department"].search([("parent_id",'=',depp.id)], )
            # print("depp###############",partner_data.mapped('id') + [depp.id])

            all_ids = [depp.id] + partner_data.mapped('id') 

            # print("all_ids@@@@@@@@@@@@@@",all_ids)

            
            # partner_data = (4, depp.id)
            # print("partner_data@@@@@@@@@@@@@",partner_data)
            day_deduction_total = 0
            total_basic_total = 0 
            total_wage_total = 0
            compensation_total = 0
            tax_total = 0
            day_deduction_total = 0
            day_deduction_amount_total = 0
            socailsecurity_total = 0
            allowance_total = 0
            reded_total = 0
            basded_total = 0
            total_ded_total = 0
            net_saled_total = 0
            total_day_all_total = 0
            total_aeaa_total = 0
            total_entitlements_total = 0
            certificate_total = 0
            previous_employee = ""
            
            worksheet.write_merge(call - 4, call - 2 , 0, 2, "جامعة الاهلية / قسم الشؤون المالية", header_bold_main_header)
            
            for values_data in all_ids:
                dep = self.env["hr.department"].search([('id','=',values_data)])
                print("depdepdepdepdepdepdepdepdepdepdep",dep.id)

                rested = self.env['hr.payslip'].search([('department','=',dep.id),('date_from','>=',self.date_from),('date_to',"<=",self.date_to)]).sorted(key=lambda r: r.employee_id.id)
                # rested = self.filtered(lambda picking: picking.employee_id.department_id.id == dep.id).sorted(key=lambda r: r.employee_id.job_id.sequence)

                worksheet.write_merge(0, 2, 3, 13, (" رواتب " + depp.name + " لشهر " + " - " + translation + convert_numbers.english_to_arabic(self.date_from.strftime('%Y/%m/%d')) +"-"+convert_numbers.english_to_arabic(self.date_to.strftime('%Y/%m/%d'))), header_bold_main_header)
                worksheet.write(call - 1, 0, dep.name, header_bold)



                

                worksheet.write_merge(call - 1, call - 1, 5, 10, 'المستحقات', header_bold_extra_tag)
                worksheet.write_merge(call - 1, call - 1, 11, 15, 'الاستقطاعات', header_bold_extra)

                # worksheet.write(call, 1, 'رقم القصاصة', header_bold)  # refernce 
                # worksheet.write(call, 1, 'Payslip Name', border_color_2)

                worksheet.write(call, 1, 'اسم الموظف', header_bold) # employee

                worksheet.write(call, 2, 'التخصص الدقيق', header_bold)


                # worksheet.write(call, 3, 'نوع الخدمة', header_bold) # employee type

                # worksheet.write(call, 4, 'نوع الشهادة', header_bold) # certifiactae



                # worksheet.write(call, 5, 'التفاصيل', header_bold) # description

                worksheet.write(call, 3, 'الايام المستقطعة', header_bold) #day deduction
                worksheet.write(call, 4, 'مبلغ ألايام', header_bold) #day deduction amount

                worksheet.write(call, 5, 'الراتب الكلي', header_bold) # wage

                worksheet.write(call, 6, 'الراتب الاسمي', header_bold) #basic salary


                # worksheet.write(call, 4, 'Wage -الراتب الاسميUSD', header_bold)
                worksheet.write(call, 7, 'التعويضية', header_bold) #compensation

                worksheet.write(call, 8, 'التدريب والتأهيل', header_bold) #allowance

                worksheet.write(call, 9, 'م.غ العاملين', header_bold) #allowance
                worksheet.write(call, 10, 'الاعانات', header_bold) #allowance

                worksheet.write(call, 11, 'م.الاستحقاقات', header_bold) #allowance

                

                # worksheet.write(call, 7, 'Basic', header_bold)
                worksheet.write(call, 12, 'الضمان', header_bold) #socaial security
                worksheet.write(call, 13, 'الضريبة', header_bold) #tax
                


                
                worksheet.write(call, 14, 'استقطاع التقاعد', header_bold) #REDED
                worksheet.write(call, 15, 'جامعة البصرة', header_bold) #BASDED
                worksheet.write(call, 16, 'م.الاستقطاعات', header_bold) #total deduction

                worksheet.write(call, 17, 'صافي الراتب', header_bold) # Net Salary

                
                # v.onboard_date >= (datetime.today().date().replace(day=1) - relativedelta(months=1)) and v.onboard_date <= (datetime.today().date() - relativedelta(months=1))
                total_basic = 0 
                total_wage_data = 0
                compensation_data = 0
                tax_data = 0
                day_deduction_data = 0
                day_deduction_amount_data = 0
                socailsecurity_data = 0
                allowance_data = 0
                reded = 0
                basded = 0
                total_ded_data = 0
                net_saled_data = 0
                total_day_all_data = 0
                total_aeaa_data = 0
                total_entitlements_data = 0
                certificate_data = 0
                sequence = 1
                employee_day_deduction_data = 0
                employee_day_deduction_amount_data = 0
                employee_total_wage_data = 0
                employee_total_basic = 0
                employee_compensation_data = 0
                employee_total_day_all_data = 0
                total_aeaa_data = 0
                employee_total_entitlements_data = 0
                employee_socailsecurity_data = 0
                employee_tax_data = 0
                employee_reded = 0
                employee_basded = 0
                employee_total_ded_data = 0
                employee_net_saled_data = 0

                employee_allowance_data = 0
                employee_total_aeaa_data = 0

                for material_line_id in rested:
                    if previous_employee != material_line_id.employee_id.id and previous_employee != "":
                        # row += 1
                        sequence = 1
                        worksheet.write(row, 0, '',main_cell_total)
                        worksheet.write(row, 1, '',main_cell_total)
                        

                        worksheet.write(row, 3, "{:,.2f}".format(employee_day_deduction_data),main_cell_total) #day deduction
                        worksheet.write(row, 4, "{:,.2f}".format(employee_day_deduction_amount_data),main_cell_total) #day deduction amount

                        worksheet.write(row, 5, "{:,.2f}".format(employee_total_wage_data),main_cell_total) # wage

                        worksheet.write(row, 6, "{:,.2f}".format(employee_total_basic),main_cell_total) #basic salary


                        # worksheet.write(call, 4, 'Wage -الراتب الاسميUSD', header_bold)
                        worksheet.write(row, 7, "{:,.2f}".format(employee_compensation_data),main_cell_total) #compensation

                        worksheet.write(row, 8, "{:,.2f}".format(employee_allowance_data),main_cell_total) #allowance


                        worksheet.write(row, 9, "{:,.2f}".format(employee_total_day_all_data),main_cell_total) #allowance
                        worksheet.write(row, 10, "{:,.2f}".format(total_aeaa_data),main_cell_total) #allowance

                        worksheet.write(row, 11, "{:,.2f}".format(employee_total_entitlements_data),main_cell_total) #total of above 3

                        # worksheet.write(call, 7, 'Basic', header_bold)
                        worksheet.write(row, 12, "{:,.2f}".format(employee_socailsecurity_data),main_cell_total) #socaial security
                        worksheet.write(row, 13, "{:,.2f}".format(employee_tax_data),main_cell_total) #tax

                        worksheet.write(row, 14, "{:,.2f}".format(employee_reded),main_cell_total) #REDED
                        worksheet.write(row, 15, "{:,.2f}".format(employee_basded),main_cell_total) #BASDED
                        worksheet.write(row, 16, "{:,.2f}".format(employee_total_ded_data),main_cell_total) #total deduction

                        worksheet.write(row, 17, "{:,.2f}".format(employee_net_saled_data),main_cell_total) # Net Salary
                        employee_day_deduction_data = 0
                        employee_day_deduction_amount_data = 0
                        employee_total_wage_data = 0
                        employee_total_basic = 0
                        employee_compensation_data = 0
                        employee_total_day_all_data = 0
                        total_aeaa_data = 0
                        employee_total_entitlements_data = 0
                        employee_socailsecurity_data = 0
                        employee_tax_data = 0
                        employee_reded = 0
                        employee_basded = 0
                        employee_total_ded_data = 0
                        employee_net_saled_data = 0
                        employee_allowance_data = 0
                        employee_total_aeaa_data = 0
                        row += 1

                    worksheet.write(row, 0, sequence or '',main_cell)
                    # worksheet.write(row, 1, material_line_id.number or '',main_cell)
                    # worksheet.write(row, 1, material_line_id.name or '',main_cell)

                    worksheet.write(row, 1, material_line_id.employee_id.name or '',main_cell)

                    if material_line_id.contract_id.employ_type == 'option1':
                        employe_data = 'تعيين - متقاعد'
                    if material_line_id.contract_id.employ_type == 'option2':
                        employe_data = 'تعيين - غير متقاعد مشمول بالضمان'
                    if material_line_id.contract_id.employ_type == 'option3':
                        employe_data = 'اعارة'
                    if material_line_id.contract_id.employ_type == 'option4':
                        employe_data = 'محاضر خارجي'
                    if material_line_id.contract_id.employ_type == 'option5':
                        employe_data = 'اجر يومي'

                    # worksheet.write(row, 3, employe_data or '',main_cell)


                    if material_line_id.employee_id.certificate_first == 'certificate1': 
                        certificate_data  = 'دكتوراه'
                    if material_line_id.employee_id.certificate_first == 'certificate2': 
                        certificate_data  = 'ماجستير'
                    if material_line_id.employee_id.certificate_first == 'certificate3': 
                        certificate_data  = 'دبلوم عالي'
                    if material_line_id.employee_id.certificate_first == 'certificate4': 
                        certificate_data  = 'بكالوريوس'
                    if material_line_id.employee_id.certificate_first == 'certificate5': 
                        certificate_data  = 'دبلوم معهد'
                    if material_line_id.employee_id.certificate_first == 'certificate6': 
                        certificate_data  = 'اعدادية'
                    if material_line_id.employee_id.certificate_first == 'certificate7': 
                        certificate_data  = 'دون الاعدادية'

                    # worksheet.write(row, 4, certificate_data or '',main_cell)

                    

                    # if material_line_id.description:
                    #     worksheet.write(row, 5, re.sub('<[^>]*>', '', material_line_id.description) or '',main_cell)

                    # if not material_line_id.description:
                    #     worksheet.write(row, 5, material_line_id.description or '',main_cell)
                    worksheet.write(row, 2, material_line_id.employee_id.first_field, main_cell)

                    worksheet.write(row, 3, "{:,.2f}".format(float(material_line_id.contract_id.day_deduction)) or '',main_cell)

                    day_deduction_data = day_deduction_data + material_line_id.contract_id.day_deduction
                    day_deduction_total = day_deduction_total + material_line_id.contract_id.day_deduction


                    employee_day_deduction_data = employee_day_deduction_data +  material_line_id.contract_id.day_deduction

                    worksheet.write(row, 4, "{:,.2f}".format(float((((material_line_id.contract_id.wage + material_line_id.contract_id.training_field) / 30) * material_line_id.contract_id.day_deduction))) or '',main_cell) 

                    day_deduction_amount_data = day_deduction_amount_data + float((((material_line_id.contract_id.wage + material_line_id.contract_id.training_field) / 30) * material_line_id.contract_id.day_deduction))
                    day_deduction_amount_total = day_deduction_amount_total + float((((material_line_id.contract_id.wage + material_line_id.contract_id.training_field) / 30) * material_line_id.contract_id.day_deduction))
                    employee_day_deduction_amount_data = employee_day_deduction_amount_data +  float((((material_line_id.contract_id.wage + material_line_id.contract_id.training_field) / 30) * material_line_id.contract_id.day_deduction))

                    # if material_line_id.contract_id.currency_id.id == 2:
                    #     worksheet.write(row, 4, str(material_line_id.contract_id.wage) + "$" or '',main_cell)

                    # if material_line_id.contract_id.currency_id.id == 90:
                    worksheet.write(row, 5, "{:,.2f}".format(float(material_line_id.contract_id.wage) + float(material_line_id.contract_id.training_field)) + "ع.د" or '',main_cell)
                    total_wage_data = total_wage_data + (float(material_line_id.contract_id.wage) + float(material_line_id.contract_id.training_field))
                    total_wage_total = total_wage_total + (float(material_line_id.contract_id.wage) + float(material_line_id.contract_id.training_field))
                    employee_total_wage_data = employee_total_wage_data + (float(material_line_id.contract_id.wage) + float(material_line_id.contract_id.training_field))
                    total_ent = 0
                    total_comp_ent = 0
                    total_all_ent = 0
                    total_all_day_all = 0
                    total_all_aeaa = 0

                    for iit in material_line_id.line_ids:
                        if iit.code == "BSCC":
                            worksheet.write(row, 6, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            total_basic = total_basic + iit.total
                            total_basic_total = total_basic_total + iit.total
                            employee_total_basic = employee_total_basic + iit.total

                            total_ent = iit.total
                        if not total_basic:
                            worksheet.write(row, 6, '',main_cell)  
                        if iit.code == "CMPS":
                            worksheet.write(row, 7, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            compensation_data = compensation_data + iit.total
                            compensation_total = compensation_total + iit.total
                            employee_compensation_data = employee_compensation_data + iit.total
                            total_comp_ent = iit.total
                        if not compensation_data:
                            worksheet.write(row, 7, '',main_cell)  

                        if iit.code == "TRA" or iit.code == "TRAMU":    
                            worksheet.write(row, 8, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            allowance_data = allowance_data + iit.total
                            allowance_total = allowance_total + iit.total
                            employee_allowance_data = employee_allowance_data + iit.total
                            total_all_ent = iit.total
                        if not allowance_data:
                            worksheet.write(row, 8, '',main_cell)    

                        if iit.code == "DAYALL":
                            worksheet.write(row, 9, "{:,.2f}".format(float(iit.total) - float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction))) or '',main_cell)
                            total_day_all_data = total_day_all_data + (iit.total -float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction)))
                            total_day_all_total = total_day_all_total + (iit.total -float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction)))
                            total_all_day_all = (iit.total -float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction)))

                            employee_total_day_all_data = employee_total_day_all_data + (iit.total -float(((material_line_id.contract_id.wage / 30) * material_line_id.contract_id.day_deduction)))
                            
                        if not total_day_all_data:
                            worksheet.write(row, 9, '',main_cell)
                        if iit.code == "AEAA":
                            worksheet.write(row, 10, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            total_aeaa_data = total_aeaa_data + iit.total
                            total_aeaa_total = total_aeaa_total + iit.total  
                            total_all_aeaa = iit.total

                            employee_total_aeaa_data = employee_total_aeaa_data + iit.total
                        if not total_aeaa_data:
                            worksheet.write(row, 10, '',main_cell)


                        total_entitlements =  total_ent + total_comp_ent + total_all_ent + total_all_day_all + total_all_aeaa
                        print("total_entitlements@@@@@@@@@@@@@@@@@@",total_entitlements)
                        if iit.code == "NET2" or iit.code == "GROSS" or iit.code == "NTS" or iit.code == "NETS" or iit.code == "NTTS" and total_entitlements > 0:
                            print("total_entitlements222222222222222222222222",total_entitlements)
                            worksheet.write(row, 11, "{:,.2f}".format(float(total_entitlements)) or '',main_cell)
                            total_entitlements_data = total_entitlements_data + total_entitlements
                            total_entitlements_total = total_entitlements_total + total_entitlements

                            employee_total_entitlements_data = employee_total_entitlements_data + total_entitlements
                                
                        if not total_entitlements_data:
                            worksheet.write(row, 11, '',main_cell)        
                        # if iit.code == "WAG":    
                        #     worksheet.write(row, 7, iit.total or '',main_cell)
                        if iit.code == "SST":    
                            worksheet.write(row, 12, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            socailsecurity_data = socailsecurity_data + iit.total
                            socailsecurity_total = socailsecurity_total + iit.total

                            employee_socailsecurity_data = employee_socailsecurity_data + iit.total

                        if not socailsecurity_data:
                            worksheet.write(row, 12, '',main_cell) 

                        if iit.code == "TAX":
                            worksheet.write(row, 13, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            tax_data = tax_data + iit.total
                            tax_total = tax_total + iit.total

                            employee_tax_data = employee_tax_data + iit.total

                        if not tax_data:
                            worksheet.write(row, 13, '',main_cell) 

                        if iit.code == "REDED":    
                            worksheet.write(row, 14, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            reded = reded + iit.total
                            reded_total = reded_total + iit.total

                            employee_reded = employee_reded + iit.total
                            
                        if not reded:
                            worksheet.write(row, 14, '',main_cell)


                        if iit.code == "BASDED":    
                            worksheet.write(row, 15, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            basded = basded + iit.total
                            basded_total = basded_total + iit.total

                            employee_basded = employee_basded + iit.total

                        if not basded:
                            worksheet.write(row, 15, '',main_cell)

                        if iit.code == "TTD":    
                            worksheet.write(row, 16, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            total_ded_data = total_ded_data + iit.total
                            total_ded_total = total_ded_total + iit.total

                            employee_total_ded_data = employee_total_ded_data + iit.total
                            
                        if not total_ded_data:
                            worksheet.write(row, 16, '',main_cell)

                        if iit.code == "NET2" or iit.code == "GROSS" or iit.code == "NTS" or iit.code == "NETS" or iit.code == "NTTS":    
                            worksheet.write(row, 17, "{:,.2f}".format(float(iit.total)) or '',main_cell)
                            net_saled_data = net_saled_data + iit.total
                            net_saled_total = net_saled_total + iit.total

                            employee_net_saled_data = employee_net_saled_data + iit.total

                        if not net_saled_data:
                            worksheet.write(row, 17, '',main_cell)    


                    # _logger.info("previous_employee@@@@@@@@@@@@@@@@@@@@@22222222222222%s" % previous_employee)
                    # _logger.info("material_line_id.employee_id.id@@@@@@@@@@@@@@@@@@@@@22222222222222%s" % material_line_id.employee_id.id)

                    # _logger.info("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")

                    

                    previous_employee = material_line_id.employee_id.id
                        

                    row += 1
                    sequence = sequence + 1 

                for x in range(17):
                    worksheet.write(row, x, '',main_cell)
                    worksheet.write(row + 1, x, '',main_cell)
                row = row + 2
                worksheet.write(row, 0, '',main_cell_total)
                worksheet.write(row, 1, '',main_cell_total)

                worksheet.write(row, 3, "{:,.2f}".format(day_deduction_data),main_cell_total) #day deduction
                worksheet.write(row, 4, "{:,.2f}".format(day_deduction_amount_data),main_cell_total) #day deduction amount

                worksheet.write(row, 5, "{:,.2f}".format(total_wage_data),main_cell_total) # wage

                worksheet.write(row, 6, "{:,.2f}".format(total_basic),main_cell_total) #basic salary


                # worksheet.write(call, 4, 'Wage -الراتب الاسميUSD', header_bold)
                worksheet.write(row, 7, "{:,.2f}".format(compensation_data),main_cell_total) #compensation

                worksheet.write(row, 8, "{:,.2f}".format(allowance_data),main_cell_total) #allowance


                worksheet.write(row, 9, "{:,.2f}".format(total_day_all_data),main_cell_total) #allowance
                worksheet.write(row, 10, "{:,.2f}".format(total_aeaa_data),main_cell_total) #allowance

                worksheet.write(row, 11, "{:,.2f}".format(total_entitlements_data),main_cell_total) #total of above 3

                # worksheet.write(call, 7, 'Basic', header_bold)
                worksheet.write(row, 12, "{:,.2f}".format(socailsecurity_data),main_cell_total) #socaial security
                worksheet.write(row, 13, "{:,.2f}".format(tax_data),main_cell_total) #tax

                worksheet.write(row, 14, "{:,.2f}".format(reded),main_cell_total) #REDED
                worksheet.write(row, 15, "{:,.2f}".format(basded),main_cell_total) #BASDED
                worksheet.write(row, 16, "{:,.2f}".format(total_ded_data),main_cell_total) #total deduction

                worksheet.write(row, 17, "{:,.2f}".format(net_saled_data),main_cell_total) # Net Salary
                call = row + 3
                row += 4

            # print("depp@@@@@@@@@@@@@@@@@@@@@@",depp)
            worksheet.write(row - 1, 0, "المجموع الكلي", main_cell_total_of_total) #day deduction

            worksheet.write(row - 1, 1, '',main_cell_total_of_total)

            worksheet.write(row - 1, 3, "{:,.2f}".format(day_deduction_total),main_cell_total_of_total) #day deduction
            worksheet.write(row - 1, 4, "{:,.2f}".format(day_deduction_amount_total),main_cell_total_of_total) #day deduction amount

            worksheet.write(row - 1, 5, "{:,.2f}".format(total_wage_total),main_cell_total_of_total) # wage

            worksheet.write(row - 1, 6, "{:,.2f}".format(total_basic_total),main_cell_total_of_total) #basic salary

            # worksheet.write(call, 4, 'Wage -الراتب الاسميUSD', header_bold)
            worksheet.write(row - 1, 7, "{:,.2f}".format(compensation_total),main_cell_total_of_total) #compensation

            worksheet.write(row - 1, 8, "{:,.2f}".format(allowance_total),main_cell_total_of_total) #allowance

            worksheet.write(row - 1, 9, "{:,.2f}".format(total_day_all_total),main_cell_total_of_total) #allowance
            worksheet.write(row - 1, 10, "{:,.2f}".format(total_aeaa_total),main_cell_total_of_total) #allowance

            worksheet.write(row - 1, 11, "{:,.2f}".format(total_entitlements_total),main_cell_total_of_total) #total of above 3

            # worksheet.write(call, 7, 'Basic', header_bold)
            worksheet.write(row - 1, 12, "{:,.2f}".format(socailsecurity_total),main_cell_total_of_total) #socaial security
            worksheet.write(row - 1, 13, "{:,.2f}".format(tax_total),main_cell_total_of_total) #tax
            worksheet.write(row - 1, 14, "{:,.2f}".format(reded_total),main_cell_total_of_total) #REDED
            worksheet.write(row - 1, 15, "{:,.2f}".format(basded_total),main_cell_total_of_total) #BASDED
            worksheet.write(row - 1, 16, "{:,.2f}".format(total_ded_total),main_cell_total_of_total) #total deduction
            worksheet.write(row - 1, 17, "{:,.2f}".format(net_saled_total),main_cell_total_of_total) # Net Salary

            call = row + 2 + 1
            row += 3 + 1
        fp = io.BytesIO()
        # print("fp@@@@@@@@@@@@@@@@@@",fp)
        wb.save(fp)
        print(wb)
        out = base64.encodebytes(fp.getvalue())
        attachment = {
                       'name': str(filename),
                       'display_name': str(filename),
                       'datas': out,
                       'type': 'binary'
                   }
        ir_id = self.env['ir.attachment'].create(attachment) 
        # print("ir_id@@@@@@@@@@@@@@@@",ir_id)

        xlDecoded = base64.b64decode(out)

        # file_added = "/home/anuj/Desktop/workspace13/payslip_report.xlsx"
        # with open(file_added, "wb") as binary_file:
        #     binary_file.write(xlDecoded)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        download_url = '/web/content/' + str(ir_id.id) + '?download=true'
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new",
        }


    #    def _get_accounts(self, accounts, display_account):
    #     """ compute the balance, debit and credit for the provided accounts
    #         :Arguments:
    #             `accounts`: list of accounts record,
    #             `display_account`: it's used to display either all accounts or those accounts which balance is > 0
    #         :Returns a list of dictionary of Accounts with following key and value
    #             `name`: Account name,
    #             `code`: Account code,
    #             `credit`: total amount of credit,
    #             `debit`: total amount of debit,
    #             `balance`: total amount of balance,
    #     """

    #     account_result = {}
    #     # Prepare sql query base on selected parameters from wizard
    #     tables, where_clause, where_params = self.env[
    #         'account.move.line']._query_get()
    #     tables = tables.replace('"', '')
    #     if not tables:
    #         tables = 'account_move_line'
    #     wheres = [""]
    #     if where_clause.strip():
    #         wheres.append(where_clause.strip())
    #     filters = " AND ".join(wheres)
    #     # compute the balance, debit and credit for the provided accounts
    #     request = (
    #                 "SELECT account_id AS id, SUM(debit) AS debit, SUM(credit) AS credit, (SUM(debit) - SUM(credit)) AS balance" + \
    #                 " FROM " + tables + " WHERE account_id IN %s " + filters + " GROUP BY account_id")
    #     params = (tuple(accounts.ids),) + tuple(where_params)
    #     self.env.cr.execute(request, params)
    #     for row in self.env.cr.dictfetchall():
    #         account_result[row.pop('id')] = row

    #     account_res = []
    #     for account in accounts:
    #         res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance'])
    #         currency = account.currency_id and account.currency_id or account.company_id.currency_id
    #         res['code'] = account.code
    #         res['name'] = account.name
    #         if account.id in account_result:
    #             res['debit'] = account_result[account.id].get('debit')
    #             res['credit'] = account_result[account.id].get('credit')
    #             res['balance'] = account_result[account.id].get('balance')
    #         if display_account == 'all':
    #             account_res.append(res)
    #         if display_account == 'not_zero' and not currency.is_zero(
    #                 res['balance']):
    #             account_res.append(res)
    #         if display_account == 'movement' and (
    #                 not currency.is_zero(res['debit']) or not currency.is_zero(
    #                 res['credit'])):
    #             account_res.append(res)
    #     return account_res

    # @api.model
    # def _get_report_values(self, docids, data=None):
    #     if not data.get('form') or not self.env.context.get('active_model'):
    #         raise UserError(
    #             _("Form content is missing, this report cannot be printed."))

    #     self.model = self.env.context.get('active_model')
    #     docs = self.env[self.model].browse(
    #         self.env.context.get('active_ids', []))
    #     display_account = data['form'].get('display_account')
    #     accounts = docs if self.model == 'account.account' else self.env[
    #         'account.account'].search([])
    #     account_res = self.with_context(
    #         data['form'].get('used_context'))._get_accounts(accounts,
    #                                                         display_account)
    #     return {
    #         'doc_ids': self.ids,
    #         'doc_model': self.model,
    #         'data': data['form'],
    #         'docs': docs,
    #         'time': time,
    #         'Accounts': account_res,
    #     }    

