# -*- coding: utf-8 -*-

# from odoo import models, fields, api
from odoo import models, fields, api

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# class techtime_department(models.Model):
#     _name = 'techtime_department.techtime_department'
#     _description = 'techtime_department.techtime_department'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class DepartmentSale(models.Model):
    _name = 'department.department'
    _description = 'department.department'
    _rec_name = 'department'


    department = fields.Char("Department")
    college = fields.Many2one("faculty.faculty", string="college")
    active = fields.Boolean("Active" , default=True)


class FacultySale(models.Model):
    _name = 'faculty.faculty'
    _description = 'faculty.faculty'
    _rec_name = 'college'

    college = fields.Char("college")
    active = fields.Boolean("Active" , default=True) 
      
    
class LevelSale(models.Model):
    _name = 'level.level'
    _description = 'level.level'
    _rec_name = 'Student'

    Student = fields.Char("Student Type")
    active = fields.Boolean("Active" , default=True)

class YearSale(models.Model):
    _name = 'year.year'
    _description = 'year.year'
    _rec_name = 'year'

    year = fields.Char("year")  
    active = fields.Boolean("Active" , default=True)  

class InstallmentDetails(models.Model):
    _name = 'installment.details'
    _description = 'installment.details'
    _rec_name = 'year'

    year = fields.Many2one("year.year", string="Year")   
    college = fields.Many2one("faculty.faculty", string="college")
    Student = fields.Many2one("level.level", string="Student Type")
    department = fields.Many2one("department.department", string="Department")
    Subject = fields.Selection([('morning','Morning'),('afternoon','AfterNoon')], string="Shift") 
    installment = fields.Float("Installment")
    level = fields.Selection([('leve1','Level 1'),('level2','Level 2'),('level3','Level 3'),('level4','Level 4'),('level5','Level 5')], string="Level")
    installment_number = fields.Integer("Installment No.")
    sale_installment_line_ids = fields.One2many('sale.installment', 'college_installment_id', string='Installment Lines', copy=True)
    

    @api.onchange('installment_number', 'installment')
    def _compute_installment_number(self):
        payable_amount = 0
        if self.installment > 0 and self.installment_number > 0:
            payable_amount = self.installment / self.installment_number
            self.sale_installment_line_ids = False
        for i in range(1, self.installment_number + 1):
            sale_installment = self.sale_installment_line_ids.create({
                'number' : i,
                'payment_date' : datetime.today().date() + relativedelta(months=+i - 1),
                'amount_installment' : payable_amount,
                'description': 'Installment Payment',
                'college_installment_id' : self._origin.id,
                })


class StudentFields(models.Model):
    """ Model for case stages. This models the main stages of a document
        management flow. Main CRM objects (leads, opportunities, project
        issues, ...) will now use only stages, instead of state and stages.
        Stages are for example used to display the kanban view of records.
    """
    _inherit = "res.partner"    

    @api.depends('is_company')
    def _compute_company_type(self):
        for partner in self:
            partner.company_type = 'person'


    number_exam = fields.Char("Exam No.")
    university_no = fields.Char("University No.")
    college_number = fields.Char("College Number")
    notes = fields.Text("Notes")
    contact_type = fields.Selection([("student","Student"),("teacher", "Teacher")], string="Contact Type")


    @api.model
    def create(self, vals):
        result = super(StudentFields, self).create(vals)
        result.property_account_receivable_id = 832
        result.property_account_payable_id = 883
        return result
         

    # faculty = fields.Many2one("hr.employee", string="Faculty")
    # trading_account_group = fields.Char("trading account group")
    # symbol_value = fields.Float("Symbol Value")