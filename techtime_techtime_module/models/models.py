# -*- coding: utf-8 -*-

from odoo import models, fields, api , _
from datetime import datetime, time, date, timedelta



# class techtime_techtime_module(models.Model):
#     _name = 'techtime_techtime_module.techtime_techtime_module'
#     _description = 'techtime_techtime_module.techtime_techtime_module'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class HrEmployeeTarget(models.Model):
    _inherit = "res.partner"
    
    x_studio_sale_order_amount = fields.Monetary("Sale order amount")  
    x_studio_quotation_amount = fields.Monetary("Quotation Amount") 
    x_studio_field_rtv0j = fields.Char("New Text")
    x_studio_sale_order = fields.One2many("sale.order", "partner_id", string="sale order")
    x_studio_field_JriwA = fields.One2many("sale.order","partner_id", string="Quotation number")
    x_studio_quotation_number = fields.Integer("Quotation number") 
    x_studio_invoice_number = fields.Integer("Invoicing Number")

    @api.model
    def create(self, vals):
        result = super(HrEmployeeTarget, self).create(vals)
        result.property_account_receivable_id = 2340
        result.property_account_payable_id = 2370
        return result
    
    @api.onchange('name', 'sale_order_count', 'x_studio_field_rtv0j')
    def _onchange_x_studio_field_rtv0j(self):
        total = sum(self.x_studio_sale_order.mapped('amount_total')) if self.x_studio_sale_order else 0
        self.x_studio_sale_order_amount = total

        total = sum(self.x_studio_field_JriwA.mapped('amount_total')) if self.x_studio_field_JriwA else 0
        self.x_studio_quotation_amount = total

        self.x_studio_quotation_number = len(self.x_studio_field_JriwA)


    @api.onchange('total_invoiced')
    def _onchange_total_invoiced_x(self):
        self.x_studio_invoice_number = len(self.invoice_ids)

    
class HrEmployeeSubscr(models.Model):
    _inherit = "sale.subscription"

    x_studio_field_bqn71  = fields.Char("New Text")
    x_studio_field_date_invoice = fields.Date("Subscription Date")
    x_studio_service_end_date = fields.Datetime("Service End Date")
    x_studio_domain = fields.Char("Domain")
    x_studio_field_adzFP = fields.Date("New Date")
    x_studio_type = fields.Selection([
        ("Google","Google"),
        ("Microsoft","Microsoft"),
        ("Odoo","ERP"),
        ("Managed Service","Managed Service"),("Other","Other")], string='Type')


    @api.onchange('x_studio_field_date_invoice')
    def _onchange_x_studio_field_date_invoice(self):
        if self.x_studio_field_date_invoice:
            self.recurring_next_date = self.x_studio_field_date_invoice - datetime.timedelta(days=10)



class HrEmployeeUserDes(models.Model):
    _inherit = "res.users"

    x_studio_quotation_number = fields.Integer("Quotation number", related="partner_id.x_studio_quotation_number")  
    x_studio_invoice_number = fields.Integer("Invoice Number",  related="partner_id.x_studio_invoice_number")  
    x_studio_sale_order_amount = fields.Monetary("Sale Order Amount", related="partner_id.x_studio_sale_order_amount")
    x_studio_sale_order = fields.One2many("sale.order", related="partner_id.x_studio_sale_order") 
    x_studio_field_rtv0j = fields.Char("New Text", related="partner_id.x_studio_field_rtv0j")
    x_studio_quotation_amount = fields.Monetary("Quotation Amount", related="partner_id.x_studio_quotation_amount")  
    x_studio_field_JriwA = fields.One2many("sale.order", string="Quotation number", related="partner_id.x_studio_field_JriwA")  
    # x_studio_field_j0N6b = fields.One2many("sale.order", string="New One2many", related="partner_id.x_studio_field_j0N6b")    



class HrEmployeejournalCreate(models.TransientModel):
    _inherit = "account.bank.statement.import.journal.creation"

    x_studio_user_data = fields.Char("User Data")
    x_studio_field_Cgnjn = fields.Many2one("res.users", string="Users", related="journal_id.x_studio_field_Cgnjn")   
    # x_studio_user_check = fields.Boolean("New Checkbox", related="journal_id.x_studio_user_check")   



class HrEmployeePayment(models.Model):
    _inherit = "account.payment"

    x_studio_field_T8oud  = fields.Many2one("account.journal", string="Payment Journal") 

    x_studio_field_L1fZY = fields.Boolean("New Checkbox")

    @api.onchange('x_studio_field_T8oud')
    def _onchange_x_studio_field_T8oud(self):
        self.journal_id = self.x_studio_field_T8oud.id

class HrEmployeeJoiur(models.Model):
    _inherit = "account.journal"

    x_studio_field_Cgnjn = fields.Many2one("res.users", string="Users") 
    x_studio_user_data = fields.Char("user data")
