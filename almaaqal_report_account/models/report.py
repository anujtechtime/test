# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

import time

from odoo import api, models, _
from odoo.exceptions import UserError


class ReportTrialBalancepagetwo(models.AbstractModel):
    _name = 'report.almaaqal_report_account.report_new_report'
    _description = 'Trial Balance Report New'

    def _get_accounts(self, accounts, display_account, date_from, date_to):
        # print("used_context##############3",data.get('used_context'))
        """ compute the balance, debit and credit for the provided accounts
            :Arguments:
                `accounts`: list of accounts record,
                `display_account`: it's used to display either all accounts or those accounts which balance is > 0
            :Returns a list of dictionary of Accounts with following key and value
                `name`: Account name,
                `code`: Account code,
                `credit`: total amount of credit,
                `debit`: total amount of debit,
                `balance`: total amount of balance,
        """

        account_result = {}
        # Prepare sql query base on selected parameters from wizard
        tables, where_clause, where_params = self.env[
            'account.move.line']._query_get()
        tables = tables.replace('"', '')
        if not tables:
            tables = 'account_move_line'
        wheres = [""]
        if where_clause.strip():
            wheres.append(where_clause.strip())
        filters = " AND ".join(wheres)
        # compute the balance, debit and credit for the provided accounts

        print("self.endwwwwwwwwwwwwwwwww",filters)
        requested = (
            "SELECT account_id AS id, "
            "SUM(CASE WHEN EXTRACT(YEAR FROM account_move_line.date) = "  + str(int(date_from[:4]) - 1) + " THEN account_move_line.debit - account_move_line.credit ELSE 0 END) AS prev_year_balance, "
            "SUM(CASE WHEN EXTRACT(YEAR FROM account_move_line.date) = " + date_from[:4] + " THEN account_move_line.debit - account_move_line.credit ELSE 0 END) AS curr_year_balance "
            "FROM " + tables + " "
            "WHERE account_id IN %s " + filters + " "
            "GROUP BY account_id"
        )


        params = (tuple(accounts.ids),) + tuple(where_params)
        self.env.cr.execute(requested, params)
        for row in self.env.cr.dictfetchall():
            account_result[row.pop('id')] = row
            print("row@@@@@@@@@@@@@@@@@@@",row)


        # request = (
        #             "SELECT account_id AS id, SUM(debit) AS debit, SUM(credit) AS credit, (SUM(debit) - SUM(credit)) AS balance" + \
        #             " FROM " + tables + " WHERE account_id IN %s " + filters + " GROUP BY account_id")
        # params = (tuple(accounts.ids),) + tuple(where_params)
        # self.env.cr.execute(request, params)
        # for row in self.env.cr.dictfetchall():
        #     account_result[row.pop('id')] = row

        account_res = []
        for account in accounts:
            res = dict((fn, 0.0) for fn in ['prev_year_balance', 'curr_year_balance'])
            currency = account.currency_id and account.currency_id or account.company_id.currency_id
            res['code'] = account.code
            res['name'] = account.name
            if account.id in account_result:
                res['curr_year_balance'] = account_result[account.id].get('curr_year_balance')
                res['prev_year_balance'] = account_result[account.id].get('prev_year_balance')
            
            account_res.append(res)
            
            # print("account_res@@@@@@@@@@@@@@@@22222222222222",account_res)    
        return account_res

    @api.model
    def _get_report_values(self, docids, data=None):
        print("data##########333344444444444444444",data['form'].get('used_context').get('date_from'))
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(
                _("Form content is missing, this report cannot be printed."))

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(
            self.env.context.get('active_ids', []))
        display_account = data['form'].get('display_account')
        accounts = docs if self.model == 'account.account' else self.env[
            'account.account'].search([])
        date_from = data['form'].get('used_context').get('date_from')    
        date_to =date_from = data['form'].get('used_context').get('date_to')   
        account_res = self.with_context(
            data['form'].get('used_context'))._get_accounts(accounts,
                                                            display_account, date_from, date_to)
        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': account_res,
        }




class ReportAccountBalanceNew(models.AbstractModel):
    _name = 'report.almaaqal_report_account.report_new_report_new'
    _description = 'Trial Balance Report New'

    def _get_accounts(self, accounts, display_account, date_from, date_to):
        # print("used_context##############3",data.get('used_context'))
        """ compute the balance, debit and credit for the provided accounts
            :Arguments:
                `accounts`: list of accounts record,
                `display_account`: it's used to display either all accounts or those accounts which balance is > 0
            :Returns a list of dictionary of Accounts with following key and value
                `name`: Account name,
                `code`: Account code,
                `credit`: total amount of credit,
                `debit`: total amount of debit,
                `balance`: total amount of balance,
        """

        account_result = {}
        # Prepare sql query base on selected parameters from wizard
        tables, where_clause, where_params = self.env[
            'account.move.line']._query_get()
        tables = tables.replace('"', '')
        if not tables:
            tables = 'account_move_line'
        wheres = [""]
        if where_clause.strip():
            wheres.append(where_clause.strip())
        filters = " AND ".join(wheres)
        # compute the balance, debit and credit for the provided accounts

        print("self.endwwwwwwwwwwwwwwwww",filters)
        requested = (
            "SELECT account_id AS id, "
            "SUM(CASE WHEN EXTRACT(YEAR FROM account_move_line.date) = "  + str(int(date_from[:4]) - 1) + " THEN account_move_line.debit - account_move_line.credit ELSE 0 END) AS prev_year_balance, "
            "SUM(CASE WHEN EXTRACT(YEAR FROM account_move_line.date) = " + date_from[:4] + " THEN account_move_line.debit - account_move_line.credit ELSE 0 END) AS curr_year_balance "
            "FROM " + tables + " "
            "WHERE account_id IN %s " + filters + " "
            "GROUP BY account_id"
        )


        params = (tuple(accounts.ids),) + tuple(where_params)
        self.env.cr.execute(requested, params)
        for row in self.env.cr.dictfetchall():
            account_result[row.pop('id')] = row
            print("row@@@@@@@@@@@@@@@@@@@",row)


        # request = (
        #             "SELECT account_id AS id, SUM(debit) AS debit, SUM(credit) AS credit, (SUM(debit) - SUM(credit)) AS balance" + \
        #             " FROM " + tables + " WHERE account_id IN %s " + filters + " GROUP BY account_id")
        # params = (tuple(accounts.ids),) + tuple(where_params)
        # self.env.cr.execute(request, params)
        # for row in self.env.cr.dictfetchall():
        #     account_result[row.pop('id')] = row

        account_res = []
        for account in accounts:
            res = dict((fn, 0.0) for fn in ['prev_year_balance', 'curr_year_balance'])
            currency = account.currency_id and account.currency_id or account.company_id.currency_id
            res['code'] = account.code
            res['name'] = account.name
            if account.id in account_result:
                res['curr_year_balance'] = account_result[account.id].get('curr_year_balance')
                res['prev_year_balance'] = account_result[account.id].get('prev_year_balance')
            
            account_res.append(res)
            
            # print("account_res@@@@@@@@@@@@@@@@22222222222222",account_res)    
        return account_res

    @api.model
    def _get_report_values(self, docids, data=None):
        print("data##########333344444444444444444",data['form'].get('used_context').get('date_from'))
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(
                _("Form content is missing, this report cannot be printed."))

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(
            self.env.context.get('active_ids', []))
        display_account = data['form'].get('display_account')
        accounts = docs if self.model == 'account.account' else self.env[
            'account.account'].search([])
        date_from = data['form'].get('used_context').get('date_from')    
        date_to =date_from = data['form'].get('used_context').get('date_to')   
        account_res = self.with_context(
            data['form'].get('used_context'))._get_accounts(accounts,
                                                            display_account, date_from, date_to)
        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': account_res,
        }



class ReportAccountBalanceTwo(models.AbstractModel):
    _name = 'report.almaaqal_report_account.report_new_report_two'
    _description = 'Trial Balance Report New'

    def _get_accounts(self, accounts, display_account, date_from, date_to):
        # print("used_context##############3",data.get('used_context'))
        """ compute the balance, debit and credit for the provided accounts
            :Arguments:
                `accounts`: list of accounts record,
                `display_account`: it's used to display either all accounts or those accounts which balance is > 0
            :Returns a list of dictionary of Accounts with following key and value
                `name`: Account name,
                `code`: Account code,
                `credit`: total amount of credit,
                `debit`: total amount of debit,
                `balance`: total amount of balance,
        """

        account_result = {}
        # Prepare sql query base on selected parameters from wizard
        tables, where_clause, where_params = self.env[
            'account.move.line']._query_get()
        tables = tables.replace('"', '')
        if not tables:
            tables = 'account_move_line'
        wheres = [""]
        if where_clause.strip():
            wheres.append(where_clause.strip())
        filters = " AND ".join(wheres)
        # compute the balance, debit and credit for the provided accounts

        print("self.endwwwwwwwwwwwwwwwww",filters)
        requested = (
            "SELECT account_id AS id, "
            "SUM(CASE WHEN EXTRACT(YEAR FROM account_move_line.date) = "  + str(int(date_from[:4]) - 1) + " THEN account_move_line.debit - account_move_line.credit ELSE 0 END) AS prev_year_balance, "
            "SUM(CASE WHEN EXTRACT(YEAR FROM account_move_line.date) = " + date_from[:4] + " THEN account_move_line.debit - account_move_line.credit ELSE 0 END) AS curr_year_balance "
            "FROM " + tables + " "
            "WHERE account_id IN %s " + filters + " "
            "GROUP BY account_id"
        )


        params = (tuple(accounts.ids),) + tuple(where_params)
        self.env.cr.execute(requested, params)
        for row in self.env.cr.dictfetchall():
            account_result[row.pop('id')] = row
            print("row@@@@@@@@@@@@@@@@@@@",row)


        # request = (
        #             "SELECT account_id AS id, SUM(debit) AS debit, SUM(credit) AS credit, (SUM(debit) - SUM(credit)) AS balance" + \
        #             " FROM " + tables + " WHERE account_id IN %s " + filters + " GROUP BY account_id")
        # params = (tuple(accounts.ids),) + tuple(where_params)
        # self.env.cr.execute(request, params)
        # for row in self.env.cr.dictfetchall():
        #     account_result[row.pop('id')] = row

        account_res = []
        for account in accounts:
            res = dict((fn, 0.0) for fn in ['prev_year_balance', 'curr_year_balance'])
            currency = account.currency_id and account.currency_id or account.company_id.currency_id
            res['code'] = account.code
            res['name'] = account.name
            if account.id in account_result:
                res['curr_year_balance'] = account_result[account.id].get('curr_year_balance')
                res['prev_year_balance'] = account_result[account.id].get('prev_year_balance')
            
            account_res.append(res)
            
            # print("account_res@@@@@@@@@@@@@@@@22222222222222",account_res)    
        return account_res

    @api.model
    def _get_report_values(self, docids, data=None):
        print("data##########333344444444444444444",data['form'].get('used_context').get('date_from'))
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(
                _("Form content is missing, this report cannot be printed."))

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(
            self.env.context.get('active_ids', []))
        display_account = data['form'].get('display_account')
        accounts = docs if self.model == 'account.account' else self.env[
            'account.account'].search([])
        date_from = data['form'].get('used_context').get('date_from')    
        date_to =date_from = data['form'].get('used_context').get('date_to')   
        account_res = self.with_context(
            data['form'].get('used_context'))._get_accounts(accounts,
                                                            display_account, date_from, date_to)
        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': account_res,
        }




class ReportTrialBalanceThree(models.AbstractModel):
    _name = 'report.almaaqal_report_account.report_new_report_three'
    _description = 'Trial Balance Report New'

    def _get_accounts(self, accounts, display_account):
        """ compute the balance, debit and credit for the provided accounts
            :Arguments:
                `accounts`: list of accounts record,
                `display_account`: it's used to display either all accounts or those accounts which balance is > 0
            :Returns a list of dictionary of Accounts with following key and value
                `name`: Account name,
                `code`: Account code,
                `credit`: total amount of credit,
                `debit`: total amount of debit,
                `balance`: total amount of balance,
        """

        account_result = {}
        # Prepare sql query base on selected parameters from wizard
        tables, where_clause, where_params = self.env[
            'account.move.line']._query_get()
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
                    " FROM " + tables + " WHERE account_id IN %s " + filters + " GROUP BY account_id")
        params = (tuple(accounts.ids),) + tuple(where_params)
        self.env.cr.execute(request, params)
        for row in self.env.cr.dictfetchall():
            account_result[row.pop('id')] = row

        account_res = []
        for account in accounts:
            res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance'])
            currency = account.currency_id and account.currency_id or account.company_id.currency_id
            res['code'] = account.code
            res['name'] = account.name
            if account.id in account_result:
                res['debit'] = account_result[account.id].get('debit')
                res['credit'] = account_result[account.id].get('credit')
                res['balance'] = account_result[account.id].get('balance')
            if display_account == 'all':
                account_res.append(res)
            if display_account == 'not_zero' and not currency.is_zero(
                    res['balance']):
                account_res.append(res)
            if display_account == 'movement' and (
                    not currency.is_zero(res['debit']) or not currency.is_zero(
                    res['credit'])):
                account_res.append(res)
        return account_res

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(
                _("Form content is missing, this report cannot be printed."))

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(
            self.env.context.get('active_ids', []))
        display_account = data['form'].get('display_account')
        accounts = docs if self.model == 'account.account' else self.env[
            'account.account'].search([])
        account_res = self.with_context(
            data['form'].get('used_context'))._get_accounts(accounts,
                                                            display_account)
        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': account_res,
        }


class ReportTrialBalancefour(models.AbstractModel):
    _name = 'report.almaaqal_report_account.report_new_report_four'
    _description = 'Trial Balance Report New'

    def _get_accounts(self, accounts, display_account):
        """ compute the balance, debit and credit for the provided accounts
            :Arguments:
                `accounts`: list of accounts record,
                `display_account`: it's used to display either all accounts or those accounts which balance is > 0
            :Returns a list of dictionary of Accounts with following key and value
                `name`: Account name,
                `code`: Account code,
                `credit`: total amount of credit,
                `debit`: total amount of debit,
                `balance`: total amount of balance,
        """

        account_result = {}
        # Prepare sql query base on selected parameters from wizard
        tables, where_clause, where_params = self.env[
            'account.move.line']._query_get()
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
                    " FROM " + tables + " WHERE account_id IN %s " + filters + " GROUP BY account_id")
        params = (tuple(accounts.ids),) + tuple(where_params)
        self.env.cr.execute(request, params)
        for row in self.env.cr.dictfetchall():
            account_result[row.pop('id')] = row

        account_res = []
        for account in accounts:
            res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance'])
            currency = account.currency_id and account.currency_id or account.company_id.currency_id
            res['code'] = account.code
            res['name'] = account.name
            if account.id in account_result:
                res['debit'] = account_result[account.id].get('debit')
                res['credit'] = account_result[account.id].get('credit')
                res['balance'] = account_result[account.id].get('balance')
            if display_account == 'all':
                account_res.append(res)
            if display_account == 'not_zero' and not currency.is_zero(
                    res['balance']):
                account_res.append(res)
            if display_account == 'movement' and (
                    not currency.is_zero(res['debit']) or not currency.is_zero(
                    res['credit'])):
                account_res.append(res)
        return account_res

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model'):
            raise UserError(
                _("Form content is missing, this report cannot be printed."))

        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(
            self.env.context.get('active_ids', []))
        display_account = data['form'].get('display_account')
        accounts = docs if self.model == 'account.account' else self.env[
            'account.account'].search([])
        account_res = self.with_context(
            data['form'].get('used_context'))._get_accounts(accounts,
                                                            display_account)
        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'Accounts': account_res,
        }
