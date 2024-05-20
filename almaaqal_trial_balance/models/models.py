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
import xlwt
import io
from lxml import etree
import html2text

import requests
import json
from odoo import api, fields, models, tools, SUPERUSER_ID

_logger = logging.getLogger(__name__)


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

        if self.date_start.month == 1:
            self.date_end = self.date_start
        if self.date_start.month == 2:
            self.date_end = self.date_start  
            self.date_start = self.date_start.replace(month=1)  
        if self.date_start and not self.date_end:
            for x in range(2):
                if x == 0:
                    start_date =  self.date_start.replace(day=1, month=1).strftime('%Y/%m/%d')
                    end_date = self.date_start.replace(day=1).strftime('%Y/%m/%d')
                    rows = 1
                    data = 0
                    only_debit = 0
                    only_credit = 0
                    groups = {}
                    start = str(self.date_start.strftime('%Y/%m'))

                    given_month = int(start[5:7]) - 1

                    # Get the name of the month
                    month_name = calendar.month_name[given_month]


                    worksheet.write(rows + 1 , col +2, "مدين", main_cell_total_of_total)
                    worksheet.write(rows + 1 , col + 3 , "دائن ", main_cell_total_of_total)
                    # worksheet.write(rows + 1 , col + 4 , "Balance", main_cell_total_of_total)

                    worksheet.write_merge(rows , rows , col + 2, col + 3 , "مدور شهر (%s)" % int(given_month), main_cell_total)
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

                            only_balance_debit = only_balance_debit + total_debit + balance_cal
                            worksheet.write(rows + 2 , col + 2 , total_debit + balance_cal - total_credit, header_bold_main_header)
                            only_debit = only_debit + total_balance
                            worksheet.write(rows + 2 , col + 3 , "0" , header_bold_main_header) 

                        if balance_cal < 0:    
                            worksheet.write(rows + 2 , col , total_debit, header_bold_main_header)
                            worksheet.write(rows + 2 , col + 1 , total_credit + abs(balance_cal), header_bold_main_header)


                            only_balance_credit = only_balance_credit + total_credit + abs(balance_cal)
                            worksheet.write(rows + 2 , col + 3 , total_credit + abs(balance_cal) - total_debit, header_bold_main_header)
                            worksheet.write(rows + 2 , col + 2 , "0" , header_bold_main_header)
                            only_credit = only_credit + abs(total_balance)

                        if balance_cal == 0 and total_debit > 0 and total_credit > 0:  
                            only_debit = only_debit + total_debit
                            only_credit = only_credit + total_credit  
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
            for dt in rrule.rrule(rrule.MONTHLY, dtstart=self.date_start.replace(day=1), until=self.date_end):
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

