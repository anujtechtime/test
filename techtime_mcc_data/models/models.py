# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)


# class techtime_mcc_data(models.Model):
#     _name = 'techtime_mcc_data.techtime_mcc_data'
#     _description = 'techtime_mcc_data.techtime_mcc_data'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class techtime_mcc_data(models.Model):
    _name = 'techtime_mcc_data.techtime_mcc_data'
    _description = 'techtime_mcc_data.techtime_mcc_data'

    name = fields.Char("Year")

class techtime_new_data(models.Model):
    _name = 'new.work'
    _description = 'new.work'

    name = fields.Char("نافذة القبول")        

class DataDDFHrEmployee(models.Model):
    _inherit = "hr.employee"

    iban = fields.Char("IBAN")
    Account_number = fields.Char("Account Number")



class DataHrEmployee(models.Model):
    _inherit = "hr.job"

    sequence = fields.Char("Sequence")


class DataMphine(models.Model):
    _inherit = "res.partner"

    data_one = fields.Many2one("new.work", string="نافذة القبول")

    year_of_acceptance_1 = fields.Many2one("techtime_mcc_data.techtime_mcc_data", string="Year of acceptance")
    file_upload = fields.Binary(string='File', attachment=True)
    attachment_upload = fields.Binary(string='Attachment', attachment=True)

    year_of_graduation = fields.Char("Year Of Graduation")
    academic_branch = fields.Char("Academi Branch")

    def get_college_data(self):
        print("self################",self)
        print("request@@@@@@@@@@@@@@@",request)
        dct = {}

        college_value = request.env["faculty.faculty"].sudo().search([])
        print("college_value@@@@@@@@@@",college_value)
        dicts = []
        for coll in college_value:
            dct = {
            'college_name' : coll.college,
            'college_id' : coll.id
            }
            dicts.append(dct)
        return dicts

    def get_new_data(self):
        print("self################",self)
        print("request@@@@@@@@@@@@@@@",request)
        dct = {}

        college_value = request.env["new.work"].sudo().search([])
        print("college_value@@@@@@@@@@",college_value)
        dicts = []
        for coll in college_value:
            dct = {
            'new_name' : coll.name,
            'new_id' : coll.id
            }
            dicts.append(dct)
        return dicts    

    def get_year_acceptance_data(self):
        print("self################",self)
        print("request@@@@@@@@@@@@@@@",request)
        dct = {}

        college_value = request.env["techtime_mcc_data.techtime_mcc_data"].sudo().search([])
        print("college_value@@@@@@@@@@",college_value)
        dicts = []
        for coll in college_value:
            dct = {
            'year_acceptance_name' : coll.name,
            'year_acceptance_id' : coll.id
            }
            dicts.append(dct)
        return dicts

    def get_student_type_data(self):
        print("self################",self)
        print("request@@@@@@@@@@@@@@@",request)
        dct = {}

        college_value = request.env["level.level"].sudo().search([])
        print("college_value@@@@@@@@@@",college_value)
        dicts = []
        for coll in college_value:
            dct = {
            'student_name' : coll.Student,
            'student_id' : coll.id
            }
            dicts.append(dct)
        return dicts    


    def get_department_data(self):
        print("self################",self)
        print("request@@@@@@@@@@@@@@@",request)
        dct = {}

        college_value = request.env["department.department"].sudo().search([])
        print("college_value@@@@@@@@@@",college_value)
        dicts = []
        for coll in college_value:
            dct = {
            'department_name' : coll.department,
            'department_id' : coll.id
            }
            dicts.append(dct)
        return dicts 

    def get_year_data(self):
        print("self################",self)
        print("request@@@@@@@@@@@@@@@",request)
        dct = {}

        college_value = request.env["year.year"].sudo().search([])
        print("college_value@@@@@@@@@@",college_value)
        dicts = []
        for coll in college_value:
            dct = {
            'year_name' : coll.year,
            'year_id' : coll.id
            }
            dicts.append(dct)
        return dicts        

class CrmTeamDateAccount(models.Model):

    _inherit = "purchase.order.line"

    qty_received = fields.Float("Received Qty", related="product_qty", inverse='_inverse_qty_received', compute_sudo=True, store=True, digits='Product Unit of Measure')


class DataLevelValueData(models.TransientModel):
    _inherit = 'level.value'
   

    Status = fields.Selection([('currecnt_student','Current student'),('succeeded','Succeeded'),('failed','Falied'),('transferred_from_us','Transferred From Us'),('graduated','Graduated')], string="Status")
    contact_type = fields.Selection([("student","طالب"),("teacher", "مدرس")], string="Contact Type", tracking=True)

    def action_confirm_change_level(self):
        print("res@@@@@@@@@@@@@@@@@@@@@@@@@@26666",self._context.get("active_id"))
        for idds in self._context.get("active_id"):
            print("idds@@@@@@@@@@@@@@@@@",idds)
            levels_sale_order = self.env["res.partner"].browse(int(idds))
            print("levels_sale_order@@@@@@@@@@@@@@@@@@@@@@@@",levels_sale_order)
            if self.level:
                levels_sale_order.level = self.level
                # levels_sale_order.partner_id.level = self.level

            if self.year:    
                levels_sale_order.year = self.year
                # levels_sale_order.partner_id.year = self.year

            if self.Status:    
                levels_sale_order.Status = self.Status
                # levels_sale_order.partner_id.Status = self.Status
                
            if self.contact_type:
                levels_sale_order.contact_type = self.contact_type

class ContractmDateAccount(models.Model):

    _inherit = "hr.contract"

    employ_type  = fields.Selection([('option1','تعيين - متقاعد'),
        ('option2','تعيين - غير متقاعد مشمول بالضمان'),
        ('option3','اعارة'),
        ('option4', 'محاضر خارجي'),
        ('option5','اجر يومي')], string="Employee Type")
    basic_salary = fields.Float('Basic Salary')


    social_security = fields.Float("Social Security")

    compensation = fields.Float("Compensation")

    compensation1 = fields.Float("Compensation One")

    training_field = fields.Float("Training")


    married_with_house_wife = fields.Boolean("Married Male with house wife")
    married_with_working_wife = fields.Boolean("Married Male with working wife")

    married_with_non_working_husband = fields.Boolean("Married Female with non-working husband")
    married_with_working_husband = fields.Boolean("Married Female with working husband")



    single_male = fields.Boolean("Single Male")

    male_female_with_children = fields.Integer("Female with No. of children")

    divorced_male = fields.Boolean("Divorced Male")

    # sinle_female = fields.Boolean("Single Female")

    divorced_female = fields.Boolean("Divorced Female")

    if_age_is_above_63 = fields.Boolean("Age is above 63")

    tota_before = fields.Float("Total after")

    total_salary = fields.Float("Total Salary")



    # tax = fields.Float("Tax")
    # tax_other = fields.Float("Tax Other")
    # traning = fields.Float("Traning")
    # allowance = fields.Float("Allowance")
    day_deduction = fields.Float("Day-Deduction")

    basic_salary_one = fields.Float("Basic Salary")
    compensation_one = fields.Float("Compensation")

    # result = 0
    # if inputs.deductiondays and inputs.deductiondays.amount:
    #  result = contract.compensation1 - (contract.wage / 30 * inputs.deductiondays.amount)
    # if result < 0:
    #  result = contract.basic_salary - (contract.wage / 30 * inputs.deductiondays.amount)

    def change_the_day_deduction(self):
        for ddt in self:
            ddt.day_deduction = 0
            ddt._inverse_wage()


    @api.onchange('wage','compensation','day_deduction','social_security','married_with_house_wife','married_with_working_wife','married_with_non_working_husband','married_with_working_husband','single_male','male_female_with_children','divorced_male','sinle_female','divorced_female','if_age_is_above_63')
    def _inverse_wage(self):
        self.total_salary = 0
        if self.wage:
            self.basic_salary = float(self.wage) * 0.77 - (((self.wage/30) * self.day_deduction) * 0.77)
            self.compensation = float(self.wage) * 0.23  - (((self.wage/30) * self.day_deduction) * 0.23) 
            self.basic_salary_one = float(self.wage) * 0.77 - (((self.wage/30) * self.day_deduction) * 0.77)
            self.compensation_one = float(self.wage) * 0.23  - (((self.wage/30) * self.day_deduction) * 0.23)
            self.social_security = float(self.basic_salary) * 0.05 
            self.compensation1 = float(self.wage) * 0.23  - (((self.wage/30) * self.day_deduction) * 0.23)
            if self.employ_type != 'option1':
                self.total_salary = self.social_security + self.compensation
                if self.married_with_house_wife:
                    self.total_salary = self.social_security + self.compensation + 375000  
                if self.married_with_working_wife:
                    self.total_salary = self.social_security + self.compensation + 208333
                if self.married_with_non_working_husband:
                    self.total_salary = self.social_security + self.compensation + 416666
                if self.married_with_working_husband:
                    self.total_salary = self.social_security + self.compensation + 208333
                if self.single_male:
                    self.total_salary = self.social_security + self.compensation + 208333
                if self.male_female_with_children:
                    self.total_salary = self.total_salary + self.male_female_with_children * 16666    
    
                if self.divorced_male:
                    self.total_salary = self.total_salary + 208333 # 

                if self.divorced_female:
                    self.total_salary = self.total_salary + 266666
                
                if self.if_age_is_above_63:
                    self.total_salary = self.total_salary + 25000  

            if self.employ_type == 'option1':
                self.total_salary = self.compensation
                if self.married_with_house_wife:
                    self.total_salary = self.compensation + 375000
                if self.married_with_working_wife:
                    self.total_salary = self.compensation + 208333
                if self.married_with_non_working_husband:
                    self.total_salary = self.compensation + 416666
                if self.married_with_working_husband:
                    self.total_salary = self.compensation + 208333  # 828,000.00 + 208333 = 1036333
                if self.single_male:
                    self.total_salary = self.compensation + 208333 

                if self.male_female_with_children: # 0 + 16666 = 16666
                    self.total_salary = self.total_salary + self.male_female_with_children * 16666   
                if self.divorced_male:
                    self.total_salary = self.total_salary + 208333 

                if self.divorced_female:
                    self.total_salary = self.total_salary + 266666
                
                if self.if_age_is_above_63:
                    self.total_salary = self.total_salary + 25000     
            
            
            


            value_data = self.basic_salary + self.compensation - self.total_salary 

            if value_data > 1000000:
                self.tota_before =  ((value_data - 83333) * 0.15) + 5833 #((2563667 - 83333) * 0.15) + 5833 = 377883.1

            if value_data > 500000 and value_data <= 1000000:
                self.tota_before =  ((value_data - 41666) * 0.10) + 1666

            if value_data > 250000 and value_data <= 500000:
                self.tota_before =  ((value_data - 20833) * 0.05) + 625 

            if value_data > 0 and value_data <= 250000:
                self.tota_before =  value_data * 0.03               


class CrmTeamSaleOrderccount(models.Model):

    _inherit = "sale.order"

    invoice_count_new = fields.Integer("Invoice data New ", readonly=False)

    @api.onchange('invoice_count_new','invoice_count')
    def _inverse_invoice_count_new(self):
        _logger.info("eeeeeeeeeeeeeeeeeeee************11111111111111#####**%s" %self)
        for ddts in self:
            ddts.invoice_count_new = ddts.invoice_count




class ContraDataDept(models.Model):
    _inherit="account.move"

    def change_the_value_department(self):
        _logger.info("self************11111111111111#####**%s" %self)
        for ddtt in self:
            if ddtt.partner_id:
                _logger.info("ddtt.partner_id************11111111111111#####**%s" %ddtt.partner_id)
                ddtt.update({
                    "college" : ddtt.partner_id.college.id if ddtt.partner_id.college else False,
                    "student" : ddtt.partner_id.student_type.id if ddtt.partner_id.student_type else False,
                    "department" : ddtt.partner_id.department.id if ddtt.partner_id.department else False,
                    "Subject" : ddtt.partner_id.shift if ddtt.partner_id.shift else False,
                    "level" : ddtt.partner_id.level if ddtt.partner_id.level else False,
                    "year" : ddtt.partner_id.year if ddtt.partner_id.year else False,
                    })


class ContraPayslipDateAccount(models.Model):
    _inherit="hr.payslip"

    description = fields.Html("Description")

    Account_number = fields.Char("Account Number", related="employee_id.Account_number")

    department = fields.Many2one("hr.department", related="employee_id.department_id", store=True)

    net_salary = fields.Float("Net Salary",compute="_value_pc", store=True)

    @api.depends('net_salary')
    def _value_pc(self):
        for record in self:
            for line in record.line_ids:
                if line.category_id.name == 'Net':
                    record.net_salary = line.total

    def change_the_value_payslip(self):
        for ddtt in self:
            ddtt.state = 'draft'

    def change_the_value_verify(self):
        for ddtt in self:
            ddtt.state = 'verify'        




