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


class ReportTrialBalancepageeight(models.AbstractModel):
    _name = 'report.base_accounting_kit.report_trial_balance_new_page_eight'
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
        print("params@@@@@@@@@@@@@@@@@@@",params)
        self.env.cr.execute(request, params)
        for row in self.env.cr.dictfetchall():
            print("row####################33",row)
            account_result[row.pop('id')] = row

        account_res = []
        for account in accounts:
            res = dict((fn, 0.0) for fn in ['credit', 'debit', 'balance'])
            currency = account.currency_id and account.currency_id or account.company_id.currency_id
            res['code'] = account.code
            res['name'] = account.name
            res["group_id"] = account.group_id.name
            # print("account_result@@@@@@@@@@@@@@@",account_result)
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
        print("account_res@@@@@@@@@@@@@@@",account_res)  
        groups = {}

        # Iterate through each dictionary in the list
        for d in account_res:
            # Extract the value that you want to group by
            group_key = d['group_id']

            credit_to_sum = float(d['credit'])
            debit_to_sum = float(d['debit'])

            group_code = self.env['account.group'].search([("name","=",d['group_id'])])
            
            # Check if the group key already exists in the groups dictionary
            if group_key in groups:
                # If the key exists, append the dictionary to the list associated with that key
                # groups[group_key].append(d)

                print("groups[group_key]['sum_credit']@@@@@@@@@@@@@@@",groups[group_key])
                groups[group_key]['sum_credit'] += float(credit_to_sum)
                groups[group_key]['sum_debit'] += float(debit_to_sum)

                if group_code:
                    groups[group_key]['code'] = group_code.code_prefix
                else:
                    groups[group_key]['code'] = False 

                # Append the dictionary to the list associated with that key
                groups[group_key]['dictionaries'].append(d)

            else:
                # If the key doesn't exist, create a new list with the current dictionary as its first element
                groups[group_key] = {'sum_credit': credit_to_sum, 'sum_debit' : debit_to_sum, 'code' : group_code.code_prefix, 'dictionaries' : [d]}


        # Now 'groups' will contain dictionaries grouped by the 'group' key
        print("groups@@@@@@@@@@@@",groups)
        

        return groups

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

        print("accounts@@@@@@@@@@@@@@@@@@@",accounts)    
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

