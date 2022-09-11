# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, datetime, timedelta
from odoo import fields, models, _
# class techtime_bbronze(models.Model):
#     _name = 'techtime_bbronze.techtime_bbronze'
#     _description = 'techtime_bbronze.techtime_bbronze'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class ProductPayout(models.Model):
    """ Model for case stages. This models the main stages of a document
        management flow. Main CRM objects (leads, opportunities, project
        issues, ...) will now use only stages, instead of state and stages.
        Stages are for example used to display the kanban view of records.
    """
    _inherit = "hr.contract"

    partner_slect = fields.Many2one('res.partner',string="الكفيل")

    # @api.onchange('partner_slect')
    # def _onchange_partner_slect(self):
    #     self.partner_slect.contract_id = self._origin.id


class ProjectProject(models.Model):
    """ Model for case stages. This models the main stages of a document
        management flow. Main CRM objects (leads, opportunities, project
        issues, ...) will now use only stages, instead of state and stages.
        Stages are for example used to display the kanban view of records.
    """
    _inherit = "project.project"


    task_1 = fields.Boolean("Task 1")  


class HrPayoutData(models.Model):
    """ Model for case stages. This models the main stages of a document
        management flow. Main CRM objects (leads, opportunities, project
        issues, ...) will now use only stages, instead of state and stages.
        Stages are for example used to display the kanban view of records.
    """
    _inherit = "hr.employee"

    contact = fields.Many2one("res.partner" ,string="الكفيل")
    arrival_date = fields.Date(string="تاريخ الوصول")

    task = fields.Many2many("project.task", string="Task")

    weight = fields.Char("Weight")
    height = fields.Char("Height")
    skin = fields.Char("Skin Color")
    age = fields.Integer("العمر")
    agent = fields.Char("الايجنت")
    religion = fields.Char("Religion")
    place_of_birth = fields.Char("Place Of Birth")
    no_of_children = fields.Integer("Number Of Children")
    previous_work_experiance = fields.Many2many("previous.work", "working_data_rel",string="Previous Work Experiance")
    language = fields.Many2many("res.language", string="Language")
    baby_sitting = fields.Boolean("Baby Sitting")
    cooking = fields.Boolean("Cooking")
    children_care = fields.Boolean("Children Care")
    tutoring = fields.Boolean("Tutoring")
    disabled_care = fields.Boolean("Disabled Care")
    baby_care = fields.Boolean("Baby Care")
    cleaning = fields.Boolean("Cleaning")
    clothes_washing = fields.Boolean("Clothes Washing")
    dish_washing = fields.Boolean("Dish Washing")
    ironing = fields.Boolean("Ironing")
    pprt = fields.Many2one("project.task")
    elderly_care = fields.Boolean("Elderly Care")


    task_count = fields.Integer(compute='_compute_task_count', string='Task Count')


    def display_task_contract(self):
        tree_view = self.env.ref('project.view_task_tree2')
        form_view = self.env.ref('project.view_task_form2')
        return {
            'name': _('Task for %s') % (self.name),
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'views': [(tree_view.id, 'tree'), (form_view.id, 'form')],
            'target': 'current',
            'domain': [('id', 'in', self.task.mapped("id"))],
        }

    def _compute_task_count(self):
        length_task = len(self.task.mapped("id"))
        self.task_count = length_task


    # @api.onchange('contact')
    # def _onchange_contact(self):
    #     self.contact.employee_id = self._origin.id



class PreviousWorkExperiance(models.Model):

    _name = 'previous.work'
    _description = 'Previous Work'

    period_of_work = fields.Char("Period Of Work")
    position = fields.Char("Position")
    country_city = fields.Many2one("res.country", string="Country")


class ResLanguage(models.Model):

    _name = 'res.language'

    name = fields.Char("Language")




class ProjProject(models.Model):

    _inherit = "project.task"

    contract_id = fields.Many2one("hr.contract", string="Contract")
    task_1 = fields.Boolean("Task", related='project_id.task_1')
    contact = fields.Many2one("res.partner" ,string="الكفيل")

    coming_date  = fields.Char("تاريخ طلب الاستقدام")
    work_permission = fields.Char("برق اذن العمل")
    entry_order_date = fields.Char("تاريخ طلب سمة الدخول")
    payment = fields.Char("دفع الرسوم")
    confirmation = fields.Char("صدور الموافقة")
    entry_date = fields.Char("تاريخ استلام سمة الدخول")
    employee_table = fields.Many2many("employee.data", "project", string="Employee")

    upload_to_staying_department  = fields.Char("Upload to Staying department")
    change_warranty = fields.Char("Change warranty")
    legal_authority = fields.Char("قانونية")
    intelligence = fields.Char("Intelligence")

    safety_issue_date = fields.Char("Safety Issue Date")
    work_order = fields.Char("Work Order")
    licence_fee = fields.Char("Licence Fee")
    receive_work_permit = fields.Char("Receive Work Permit")
    issue_of_safety_confirmation = fields.Char("Issue Of Safety Confirmation")
    receive_the_badge = fields.Char("Receive The Badge")


    @api.onchange('coming_date')
    def _onchange_coming_date(self):
        self.stage_id = 17

    @api.onchange('work_permission')
    def _onchange_work_permission(self):
        self.stage_id = 18

    @api.onchange('entry_order_date')
    def _onchange_entry_order_date(self):
        self.stage_id = 22

    @api.onchange('payment')
    def _onchange_payment(self):
        self.stage_id = 19 

    @api.onchange('confirmation')
    def _onchange_confirmation(self):
        self.stage_id = 20

    @api.onchange('entry_date')
    def _onchange_entry_date(self):
        self.stage_id = 21      

    
    



    def write(self, vals):
        res =  super(ProjProject, self).write(vals)
        print("result###################",self.employee_table)
        for ids in self.employee_table:
            if ids.employee_id:
                ids.employee_id.task = [(4, self.id)]
        if self.contact:
            self.contact.task = [(4, self.id)]           
        return res


class ResPartner(models.Model):

    _inherit = "res.partner"

    task = fields.Many2many("project.task", string="Task")
    # contract_id = fields.Many2one("hr.contract", string="Contract")
    # employee_id = fields.Many2one("hr.employee")
    contracts_count = fields.Integer(compute='_compute_contracts_count', string='Contract Count')
    
    # @api.depends('is_company')
    # def _compute_company_type(self):
    #     for partner in self:
    #         print("self")
    #         # partner.company_type = 'company' if partner.is_company else 'person'

    task_count = fields.Integer(compute='_compute_task_count_partner', string='Task Count')


    def display_task_contract(self):
        tree_view = self.env.ref('project.view_task_tree2')
        form_view = self.env.ref('project.view_task_form2')
        return {
            'name': _('Task for %s') % (self.name),
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'views': [(tree_view.id, 'tree'), (form_view.id, 'form')],
            'target': 'current',
            'domain': [('id', 'in', self.task.mapped("id"))],
        }

    def _compute_task_count_partner(self):
        length_task = len(self.task.mapped("id"))
        self.task_count = length_task

    def _compute_contracts_count(self):
        # read_group as sudo, since contract count is displayed on form view
        contract_data = self.env['hr.contract'].sudo().read_group([('partner_slect', 'in', self.ids)], ['partner_slect'], ['partner_slect'])
        print("partner_slect@@@@@@@@@@@@@@@@",contract_data)
        result = dict((data['partner_slect'][0], data['partner_slect_count']) for data in contract_data)
        for employee in self:
            employee.contracts_count = result.get(employee.id, 0)


    def display_contract(self):
        tree_view = self.env.ref('hr_contract.hr_contract_view_tree')
        form_view = self.env.ref('hr_contract.hr_contract_view_form')
        return {
            'name': _('Contract for %s') % (self.name),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.contract',
            'views': [(tree_view.id, 'tree'), (form_view.id, 'form')],
            'target': 'current',
            'domain': [('partner_slect', 'in', self.ids)],
        }

class EmployeeNation(models.Model):

    _name = 'employee.data'


    project = fields.Many2one("project.task",string="project")
    employee_id = fields.Many2one("hr.employee", string="Employee")
    country_id = fields.Many2one("res.country", string="Country")
    passport_id = fields.Char("Passport")

    @api.onchange('employee_id')
    def _onchange_phone_validation_check(self):
        self.country_id = self.employee_id.country_id.id
        self.passport_id = self.employee_id.passport_id
