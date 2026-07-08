# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MoveDiv(models.Model):
    _inherit = "account.move"

    student_status_in_department = fields.Char(" الطالب في القسم")
    Status = fields.Selection([('status4', 'مؤجل'),('status1','ترقين قيد'),('status2','طالب غير مباشر'),('status3','انسحاب'),('currecnt_student','Current student'),('succeeded','Succeeded'),('failed','Falied'),('transferred_from_us','Transferred From Us'),('graduated','Graduated')], string="Status", store=True, related="partner_id.Status")
    year_of_acceptance_1 = fields.Many2one("techtime_mcc_data.techtime_mcc_data", string="Year of acceptance", store=True, related="partner_id.year_of_acceptance_1")

from odoo import api, fields, models

class SaleInstallment(models.Model):
    _inherit = 'sale.installment'

    # Option 1: Directly related to the existing field
    installment_details_year = fields.Many2one(
        comodel_name='year.year',
        related='college_installment_id.year',
        string='Year',
        store=True,
        readonly=True,
    )
    
    installment_details_college = fields.Many2one(
        comodel_name='faculty.faculty',
        related='college_installment_id.college',
        string='College',
        store=True,
        readonly=True,
    )
    
    installment_details_student = fields.Many2one(
        comodel_name='level.level',
        related='college_installment_id.Student',
        string='Student Type',
        store=True,
        readonly=True,
    )
    
    installment_details_department = fields.Many2one(
        comodel_name='department.department',
        related='college_installment_id.department',
        string='Department',
        store=True,
        readonly=True,
    )
    
    installment_details_shift = fields.Selection(
        selection=[('morning','Morning'),('afternoon','AfterNoon')],
        related='college_installment_id.Subject',
        string='Shift',
        store=True,
        readonly=True,
    )
    
    installment_details_level = fields.Selection(
        selection=[('leve1','Level 1'),('level2','Level 2'),('level3','Level 3'),('level4','Level 4'),('level5','Level 5')],
        related='college_installment_id.level',
        string='Level',
        store=True,
        readonly=True,
    )
    
    # Option 2: If you want a direct Many2one to installment.details (if not already present)
    # This might already exist as 'college_installment_id'
    # If not, add it:
    # college_installment_id = fields.Many2one(
    #     'installment.details',
    #     string='Installment Details',
    #     ondelete='restrict',
    # )

# class new_field_installment(models.Model):
#     _name = 'new_field_installment.new_field_installment'
#     _description = 'new_field_installment.new_field_installment'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


# class SaleMembershipInt(models.Model):
#     _inherit = 'sale.installment'

#     department = fields.Many2one(
#         'department.department',
#         related='invoice_id.department',
#         store=True,
#         readonly=True,
#     )

