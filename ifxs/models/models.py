# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pymssql

class CapwiseCrm(models.Model):
    _inherit = "sale.order"



    def action_done_test(self):
        # try:
        # connection = mysql.connector.connect(host='35.153.243.4',
        #                                      database='rifxcrm',
        #                                      user='rifxcrm_rousr',
        #                                      password="E(+'T_Mc.P/iStH5NJ")
        # _logger.info("pincode**************##################**%s" %connection)
        # print("connection#################",connection)
        # set_count = self.env['ir.config_parameter'].set_param('count.irfx.data', 2000)
        # base_url = self.env['ir.config_parameter'].sudo().get_param('count.irfx.data')
        con = pymssql.connect(host="35.153.243.4", user='rifxcrm_rousr', password="E(+'T_Mc.P/iStH5NJ",
                                   database='rifxcrm', port=1433)
        _logger.info("pincodeconconconconcon##################**%s" %con)
        cursor = con.cursor()
        _logger.info("pincodeconFFFFFFFFFFFFFFFFF##################**%s" %cursor)
        query = 'SELECT c_id FROM v_easy_nl_all_contacts;'
        cursor.execute(query)
        records = cursor.fetchall()
        _logger.info("pinrecordsrecordsrecordsrecordsrecllllllllllllllllllllllllords*%s" %records)
        for red in records:
            if self.count_from < red[0] and self.count_to > red[0]:
                que = """SELECT email , name , nameCompanyIB , address, countryName  FROM v_easy_nl_all_contacts where c_id =%s;""" % red[0]
                cursor.execute(que)
                recdd = cursor.fetchall()
                print("red$$$$$$$$$$$$$$$$$$$$4",recdd) 
                contact = self.env["res.partner"].search([("id","=",red[0])])
                if not contact:
                    for reffg in recdd:
                        contact.create({
                            "id" : red[0],
                            "email" : reffg[0] if reffg else False,
                            "name" : reffg[1] if reffg else False,
                            "website" : reffg[2] if reffg else False,
                            "street" : reffg[3] if reffg else False
                            })




class ifxs(models.Model):
    _name = 'symbol.data'
    _description = 'symbol.data'
    _rec_name = 'trading_account_group'

    symbol = fields.Char()
    trading_account_group = fields.Char("trading account group")
    symbol_value = fields.Float("Symbol Value")



class AccountExtend(models.Model):
    _inherit = "account.move"

    count_from = fields.Integer("count from")
    count_to = fields.Integer("count to")


    Platform_Description = fields.Char("Platform_Description")
    Login = fields.Char("Login")
    Trading_Account_Group = fields.Char("Trading_Account_Group")
    Ticket = fields.Char("Ticket")
    Time = fields.Char("Time")
    Symbol = fields.Char("Symbol")
    Action = fields.Char("Action")
    Price = fields.Char("Price")
    Profit = fields.Char("Profit")
    Country = fields.Char("Country")
    Volume = fields.Char("Volume")
    Symbol = fields.Char("Symbol")


    def action_done_test(self):
        print("self######################",self)
        count_from = self.env['ir.config_parameter'].sudo().get_param('count.irfx.count_from')
        count_to = self.env['ir.config_parameter'].sudo().get_param('count.irfx.count_to')
        if not count_from or not count_to:
            set_count_from = self.env['ir.config_parameter'].set_param('count.irfx.count_from', 0)
            set_count_to = self.env['ir.config_parameter'].set_param('count.irfx.count_to', 2000)
        # base_url = self.env['ir.config_parameter'].sudo().get_param('count.irfx.data')
        count_from = self.env['ir.config_parameter'].sudo().get_param('count.irfx.count_from')
        count_to = self.env['ir.config_parameter'].sudo().get_param('count.irfx.count_to')
        con = pymssql.connect(host="35.153.243.4", user='rifxcrm_rousr', password="E(+'T_Mc.P/iStH5NJ",
                                   database='rifxcrm', port=1433)
        _logger.info("pincodeconconconconcon##################**%s" %con)
        cursor = con.cursor()
        _logger.info("pincodeconFFFFFFFFFFFFFFFFF##################**%s" %cursor)
        query = 'SELECT Order_no FROM v_all_trades;'
        cursor.execute(query)
        records = cursor.fetchall()
        _logger.info("pinrecordsrecordsrecordsrecordsrecllllllllllllllllllllllllords*%s" %records)
        # set_count = self.env['ir.config_parameter'].set_param('count.irfx.data', 2000)
        # base_url = self.env['ir.config_parameter'].sudo().get_param('count.irfx.data')
        for red in records:
            if count_from < red[0] and count_to > red[0]:
                que = """SELECT platform , Login , Group_Name , ticket , time , symbol , action_desc , price , profit , country , Volume  FROM v_all_trades where Order_no =%s;""" % red[0]
                cursor.execute(que)
                recdd = cursor.fetchall()
                contact = self.env["account.move"].search([("id","=",red[0])])
                if not contact:
                    for reffg in recdd:
                        contact.create({
                            "Platform_Description" : reffg[0],
                            "Login" : reffg[1],
                            "Trading_Account_Group" : reffg[2],
                            "Ticket" : reffg[3],
                            "Time" : reffg[4],
                            "Symbol" : reffg[5],
                            "Action" : reffg[6],
                            "Price" : reffg[7],
                            "Profit" : reffg[8],
                            "Country" : reffg[9],
                            "Volume" : reffg[10],
                            "id": red[0]
                            })
                        data_set = red[0]
        set_count_from = self.env['ir.config_parameter'].set_param('count.irfx.count_from', int(data_set))
        set_count_to = self.env['ir.config_parameter'].set_param('count.irfx.count_to', int(data_set) + 2000)