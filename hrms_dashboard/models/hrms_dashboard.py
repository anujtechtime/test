# -*- coding: utf-8 -*-

from collections import defaultdict
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd
from pytz import utc
from odoo import models, fields, api, _
from odoo.http import request
from odoo.tools import float_utils

import logging

_logger = logging.getLogger(__name__)

ROUNDING_FACTOR = 16

class Employee(models.Model):
    _inherit = 'hr.employee'

    birthday = fields.Date('Date of Birth', groups="base.group_user", help="Birthday")

    @api.model
    def check_user_group(self):
        uid = request.session.uid
        user = self.env['res.users'].sudo().search([('id', '=', uid)], limit=1)
        if user.has_group('hr.group_hr_manager'):
            return True
        else:
            return False

    @api.model
    def get_user_employee_details(self):
        uid = request.session.uid
        employee = self.env['res.users'].sudo().search_read([('id', '=', uid)], limit=1)
        today = datetime.strftime(datetime.today(), '%Y-%m-%d')
        
        first_day = date.today().replace(day=1)
        last_day = (date.today() + relativedelta(months=1, day=1)) - timedelta(1)
        

        year  =  self.env['year.year'].sudo().search([]).mapped("year") 
        
        year_of_acceptance  =  self.env['techtime_mcc_data.techtime_mcc_data'].sudo().search([]).mapped("name")

        department  =  self.env['department.department'].sudo().search([]).mapped("department")
        
        timesheet_count = self.env['res.partner'].sudo().search_count(
            [('transferred_to_us', '!=', False)])

        payslip_count = self.env['res.partner'].sudo().search_count(
            [('transfer_shift', '!=', False)])

        contracts_count = self.env['res.partner'].sudo().search_count(
            [('chckbox_data', '!=', False)])


        broad_factor = self.env['res.partner'].sudo().search_count(
            [('boolean_one', '!=', False)]) 


        leaves_to_approve  =  self.env['res.partner'].sudo().search_count(
            [('boolean_two', '!=', False)]) 

        leaves_today  =  self.env['res.partner'].sudo().search_count(
            [('boolean_three', '!=', False)]) 

        leaves_this_month  =  self.env['res.partner'].sudo().search_count(
            [('boolean_four', '!=', False)])         


        if employee:
            # broad_factor = result[0]['broad_factor']
            if employee[0]['birthday']:
                diff = relativedelta(datetime.today(), employee[0]['birthday'])
                age = diff.years
            else:
                age = False
            if employee[0]['create_date']:
                diff = relativedelta(datetime.today(), employee[0]['create_date'])
                years = diff.years
                months = diff.months
                days = diff.days
                experience = '{} years {} months {} days'.format(years, months, days)
            else:
                experience = False
            if employee:
                data = {
                    'broad_factor': broad_factor if broad_factor else 0,
                    'leaves_to_approve': leaves_to_approve,
                    'leaves_today': leaves_today,
                    'leaves_this_month': leaves_this_month,
                    'contracts_count': contracts_count,
                    'emp_timesheets': timesheet_count,
                    'payslip_count': payslip_count,
                    'experience': experience,
                    'age': age,
                    'year' :  year,
                    'year_of_acceptance' : year_of_acceptance,
                    'department' : department,
                }
                employee[0].update(data)
            return employee
        else:
            return False

    # @api.model
    # def get_dashboard_data(self, filters=None):

    #     domain = []

    #     if filters.get('academic_year_id'):
    #         domain.append(
    #             ('academic_year_id', '=', int(filters['academic_year_id']))
    #         )

    #     if filters.get('acceptance_year_id'):
    #         domain.append(
    #             ('acceptance_year_id', '=', int(filters['acceptance_year_id']))
    #         )

    #     students = self.env['your.student.model'].search(domain)

    #     return {
    #         'total_students': len(students),
    #         'year_chart': self._get_year_chart(domain),
    #         'college_chart': self._get_college_chart(domain),
    #         'status_chart': self._get_status_chart(domain),
    #     }

    @api.model
    def get_upcoming(self):
        cr = self._cr
        uid = request.session.uid
        employee = self.env['hr.employee'].search([('user_id', '=', uid)], limit=1)

        cr.execute("""select *, 
        (to_char(dob,'ddd')::int-to_char(now(),'ddd')::int+total_days)%total_days as dif
        from (select he.id, he.name, to_char(he.birthday, 'Month dd') as birthday,
        hj.name as job_id , he.birthday as dob,
        (to_char((to_char(now(),'yyyy')||'-12-31')::date,'ddd')::int) as total_days
        FROM hr_employee he
        join hr_job hj
        on hj.id = he.job_id
        ) birth
        where (to_char(dob,'ddd')::int-to_char(now(),'DDD')::int+total_days)%total_days between 0 and 15
        order by dif;""")
        birthday = cr.fetchall()
        ddt = {
            'birthday': birthday,
        }
        return {
            'birthday': birthday,
        }

    @api.model
    def get_dept_employee(self):
        cr = self._cr
        cr.execute("""select techtime_mcc_data_techtime_mcc_data.name,count(*) 
from res_partner join techtime_mcc_data_techtime_mcc_data on techtime_mcc_data_techtime_mcc_data.id=res_partner.year_of_acceptance_1 
group by res_partner.year_of_acceptance_1 , techtime_mcc_data_techtime_mcc_data.name""")
        dat = cr.fetchall()
        data = []
        for i in range(0, len(dat)):
            data.append({'label': dat[i][0], 'value': dat[i][1]})
        return data

    @api.model
    def get_dept_employee_shift(self):
        shift = ['morning','afternoon']
        data = []
        for i in shift:
            shift_contact = self.env['res.partner'].sudo().search_count([("shift",'=',i)])
            if i == 'afternoon':
                i = 'مسائي'
            if i == 'morning':
                i = 'صباحي'    

            data.append({'label': i, 'value': shift_contact})
        return data

    @api.model
    def get_dept_employee_shift_gender(self):
        shift = ['male','female']
        data = []
        for i in shift:
            shift_contact = self.env['res.partner'].sudo().search_count([("gender",'=',i)])
            if i == 'male':
                i = 'ذكر'
            if i == 'female':
                i = 'انثى'    

            data.append({'label': i, 'value': shift_contact})
        return data    

        


    @api.model
    def get_department_leave(self):
        month_list = []
        graph_result = []

        graph_result_pie = []
        level_data = ["leve1","level2", "level3", "level4"]
        level_name = ""
        department_list = ""
        for level in level_data:
            level_data = self.env["res.partner"].sudo().search_count([("level",'=',level)])
            if level == "leve1":
                level_name = "المرحلة الاولى"
            if level == "level2":
                level_name = "المرحلة الثانية"
            if level == "level3": 
                level_name = "المرحلة الثالثة"
            if level == "level4":
                level_name = "المرحلة الرابعة"
            if level == "level5":
                level_name = "المرحلة الخامسة"
            vals_d = {
                'leave' : level_data,
                'type': level_name,
            }
            vals_pie = {
                0 : level_name,
                1: level_data,
            }
            graph_result.append(vals_pie)
            graph_result_pie.append(vals_d) 
            department_list = level_data
        # {'l_month': 'Dec 2022', 'leave': {'Administration': 0, 'Sales': 0, 'Management': 0, 'Research & Development': 0, 'Professional Services': 0}}, {'l_month': 'Jan 2023', 'leave': {'Administration': 0, 'Sales': 0, 'Management': 0, 'Research & Development': 0, 'Professional Services': 0}}, {'l_month': 'Feb 2023', 'leave': {'Administration': 0, 'Sales': 0, 'Management': 0, 'Research & Development': 0, 'Professional Services': 0}}, {'l_month': 'Mar 2023', 'leave': {'Administration': 0, 'Sales': 0, 'Management': 0, 'Research & Development': 0, 'Professional Services': 0}}, {'l_month': 'Apr 2023', 'leave': {'Administration': 0, 'Sales': 0, 'Management': 0, 'Research & Development': 0, 'Professional Services': 0}}, {'l_month': 'May 2023', 'leave': {'Administration': 0, 'Sales': 0, 'Management': 2.0, 'Research & Development': 3.0, 'Professional Services': 0}}]
        # gggggggggggggggggggggg ['Administration', 'Sales', 'Management', 'Research & Development', 'Professional Services']                      
        return graph_result, department_list, graph_result_pie

    # def get_work_days_dashboard(self, from_datetime, to_datetime, compute_leaves=False, calendar=None, domain=None):
    #     resource = self.resource_id
    #     calendar = calendar or self.resource_calendar_id

    #     if not from_datetime.tzinfo:
    #         from_datetime = from_datetime.replace(tzinfo=utc)
    #     if not to_datetime.tzinfo:
    #         to_datetime = to_datetime.replace(tzinfo=utc)
    #     from_full = from_datetime - timedelta(days=1)
    #     to_full = to_datetime + timedelta(days=1)
    #     intervals = calendar._attendance_intervals(from_full, to_full, resource)
    #     day_total = defaultdict(float)
    #     for start, stop, meta in intervals:
    #         day_total[start.date()] += (stop - start).total_seconds() / 3600
    #     if compute_leaves:
    #         intervals = calendar._work_intervals(from_datetime, to_datetime, resource, domain)
    #     else:
    #         intervals = calendar._attendance_intervals(from_datetime, to_datetime, resource)
    #     day_hours = defaultdict(float)
    #     for start, stop, meta in intervals:
    #         day_hours[start.date()] += (stop - start).total_seconds() / 3600
    #     days = sum(
    #         float_utils.round(ROUNDING_FACTOR * day_hours[day] / day_total[day]) / ROUNDING_FACTOR
    #         for day in day_hours
    #     )

    #     return days

    @api.model
    def employee_leave_trend(self):
        leave_lines = []
        month_list = []
        graph_result = []
        value = 0


        college_info = self.env['level.level'].sudo().search([])
          
        for month in college_info:
            res = 0
            res = self.env["res.partner"].sudo().search_count([('student_type','=',month.id)])
            vals = {
                'l_month': month.Student,
                'leave': res
            }
            value = value + res
            graph_result.append(vals)
        # graph_resultgggggffffffffffffffffffff [{'l_month': 'Dec 2022', 'leave': 0}, {'l_month': 'Jan 2023', 'leave': 0}, {'l_month': 'Feb 2023', 'leave': 0}, {'l_month': 'Mar 2023', 'leave': 0}, {'l_month': 'Apr 2023', 'leave': 0}, {'l_month': 'May 2023', 'leave': 0}]
        return graph_result

    @api.model
    def join_resign_trends(self):
        cr = self._cr
        month_list = []
        join_trend = []
        resign_trend = []
        value = 0
        value_shift = 0
        value_s = 0
        for i in range(11, -1, -1):
            last_month = datetime.now() - relativedelta(months=i)
            text = format(last_month, '%B %Y')
            month_list.append(text)
            
        college_info = self.env['faculty.faculty'].sudo().search([])
          
        for month in college_info:
            res = 0
            res = self.env["res.partner"].sudo().search_count([('college','=',month.id)])
            vals = {
                'l_month': month.college,
                'count': res
            }
            value = value + res
            join_trend.append(vals)
        graph_result = [{
            'name': 'College (%s)' % value,
            'values': join_trend
        }]

        # graph_resultkkkkkkkkkkkkkkkkkkkkkkkkkk [{'name': 'Transfered To Us', 'values': [{'l_month': 'Jun', 'count': 0}, {'l_month': 'Jul', 'count': 0}, {'l_month': 'Aug', 'count': 0}, {'l_month': 'Sep', 'count': 0}, {'l_month': 'Oct', 'count': 0}, {'l_month': 'Nov', 'count': 0}, {'l_month': 'Dec', 'count': 0}, {'l_month': 'Jan', 'count': 0}, {'l_month': 'Feb', 'count': 0}, {'l_month': 'Mar', 'count': 0}, {'l_month': 'Apr', 'count': 0}, {'l_month': 'May', 'count': 0}]}, {'name': 'Resign', 'values': [{'l_month': 'Jun', 'count': 0}, {'l_month': 'Jul', 'count': 0}, {'l_month': 'Aug', 'count': 0}, {'l_month': 'Sep', 'count': 0}, {'l_month': 'Oct', 'count': 0}, {'l_month': 'Nov', 'count': 0}, {'l_month': 'Dec', 'count': 0}, {'l_month': 'Jan', 'count': 0}, {'l_month': 'Feb', 'count': 0}, {'l_month': 'Mar', 'count': 0}, {'l_month': 'Apr', 'count': 0}, {'l_month': 'May', 'count': 0}]}]

        return graph_result


    @api.model
    def join_resign_trends_dep(self):
        cr = self._cr
        month_list = []
        join_trend = []
        resign_trend = []
        value = 0
        value_shift = 0
        value_s = 0

        department_info = self.env['department.department'].sudo().search([]) 
        for month in department_info:
            res_id = 0
            res_id = self.env["res.partner"].sudo().search_count([('department','=',month.id)])
            vals = {
                'l_month': month.department,
                'count': res_id
            }
            value_s = value_s + res_id
            resign_trend.append(vals)

        graph_result = [{
            'name': 'Department (%s)' % value_s,
            'values': resign_trend
        }]

        # graph_resultkkkkkkkkkkkkkkkkkkkkkkkkkk [{'name': 'Transfered To Us', 'values': [{'l_month': 'Jun', 'count': 0}, {'l_month': 'Jul', 'count': 0}, {'l_month': 'Aug', 'count': 0}, {'l_month': 'Sep', 'count': 0}, {'l_month': 'Oct', 'count': 0}, {'l_month': 'Nov', 'count': 0}, {'l_month': 'Dec', 'count': 0}, {'l_month': 'Jan', 'count': 0}, {'l_month': 'Feb', 'count': 0}, {'l_month': 'Mar', 'count': 0}, {'l_month': 'Apr', 'count': 0}, {'l_month': 'May', 'count': 0}]}, {'name': 'Resign', 'values': [{'l_month': 'Jun', 'count': 0}, {'l_month': 'Jul', 'count': 0}, {'l_month': 'Aug', 'count': 0}, {'l_month': 'Sep', 'count': 0}, {'l_month': 'Oct', 'count': 0}, {'l_month': 'Nov', 'count': 0}, {'l_month': 'Dec', 'count': 0}, {'l_month': 'Jan', 'count': 0}, {'l_month': 'Feb', 'count': 0}, {'l_month': 'Mar', 'count': 0}, {'l_month': 'Apr', 'count': 0}, {'l_month': 'May', 'count': 0}]}]

        return graph_result    

    @api.model
    def get_attrition_rate(self):
        month_attrition = []
        
        status = ['status4','status1','status2','status3','currecnt_student','succeeded','failed','transferred_from_us','graduated']
        for stat in status:
            res_part = 0
            res_part = self.env["res.partner"].sudo().search([("Status",'=',stat)])
            length_status = len(res_part.mapped("id"))
            if stat == 'status4':
                stat = 'مؤجل'
            if stat == 'status1':
                stat = 'ترقين قيد'
            if stat == 'status2':
                stat = 'طالب غير مباشر'
            if stat == 'status3':
                stat = 'انسحاب'
            if stat == 'currecnt_student':
                stat = 'Current std'
            if stat == 'succeeded':
                stat = 'Succeeded'
            if stat == 'failed':
                stat = 'Falied'
            if stat == 'transferred_from_us':
                stat = 'Transferred'
            if stat == 'graduated':
                stat = 'Graduated'
            vals = {
                # 'month': month_emp[1].split(' ')[:1][0].strip()[:3] + ' ' + month_emp[1].split(' ')[-1:][0],
                'month': stat,
                'attrition_rate': length_status
            }
            month_attrition.append(vals)

        # month_attrition################# [{'month': 'May', 'attrition_rate': 0.0}, {'month': 'Apr', 'attrition_rate': 0.0}, {'month': 'Mar', 'attrition_rate': 0.0}, {'month': 'Feb', 'attrition_rate': 0.0}, {'month': 'Jan', 'attrition_rate': 0.0}, {'month': 'Dec', 'attrition_rate': 0.0}, {'month': 'Nov', 'attrition_rate': 0.0}, {'month': 'Oct', 'attrition_rate': 0.0}, {'month': 'Sep', 'attrition_rate': 0.0}, {'month': 'Aug', 'attrition_rate': 0.0}, {'month': 'Jul', 'attrition_rate': 0.0}, {'month': 'Jun', 'attrition_rate': 0.0}]

        return month_attrition
    

class SaleInstallment(models.Model):
    _inherit = 'sale.installment'

    department = fields.Many2one(
        'department.department',
        related='sale_installment_id.department',
        store=True,
        readonly=True,
    )

    student = fields.Many2one(
        'level.level',
        related='sale_installment_id.student',
        store=True,
        readonly=True,
    )

class ResPartner(models.Model):
    _inherit = 'sale.order'


    acceptance_year_id = fields.Many2one("techtime_mcc_data.techtime_mcc_data", string="Year of acceptance", related="partner_id.year_of_acceptance_1")

    @api.model
    def get_student_payment_dashboard(self, filters=None):
        filters = filters or {}

        Installment = self.env['sale.installment']
        Department = self.env['department.department']
        StudentType = self.env['level.level']

        sale_domain = []
        installment_domain = []

        if filters.get('acceptance_year_id'):
            sale_domain.append(
                ('year_of_acceptance_1.name', '=', filters['acceptance_year_id'])
            )

            installment_domain.append(
                ('sale_installment_id.year_of_acceptance_1.name', '=', filters['acceptance_year_id'])
            )

        result = {
            'kpi': {},
            'second_installment_percentage': [],
            'first_installment_department': [],
            'first_installment_student_type': [],
        }

        # ==========================================================
        # KPI
        # ==========================================================
        kpi_groups = Installment.read_group(
            installment_domain + [
                ('payment_status', '=', 'paid'),
                ('number', 'in', [1, 2, 3]),
            ],
            ['number'],
            ['number'],
            lazy=False,
        )

        kpi = {}
        for rec in kpi_groups:
            kpi[rec['number']] = rec['__count']

        result['kpi'] = {
            'first_paid': kpi.get(1, 0),
            'second_paid': kpi.get(2, 0),
            'third_paid': kpi.get(3, 0),
        }

        # ==========================================================
        # Total Students Department Wise
        # ==========================================================
        total_groups = self.read_group(
            sale_domain,
            ['department'],
            ['department'],
            lazy=False,
        )

        total_map = {}
        for rec in total_groups:
            if rec.get('department'):
                total_map[rec['department'][0]] = rec['__count']

        # ==========================================================
        # Second Installment Paid Department Wise
        # ==========================================================
        second_groups = Installment.read_group(
            installment_domain + [
                ('payment_status', '=', 'paid'),
                ('number', '=', 2),
            ],
            ['department'],
            ['department'],
            lazy=False,
        )

        second_map = {} 
        for rec in second_groups:
            if rec.get('sale_installment_id.department'):
                second_map[
                    rec['sale_installment_id.department'][0]
                ] = rec['__count']

        # ==========================================================
        # First Installment Paid Department Wise
        # ==========================================================
        first_groups = Installment.read_group(
            installment_domain + [
                ('payment_status', '=', 'paid'),
                ('number', '=', 1),
            ],
            ['department'],
            ['department'],
            lazy=False,
        )

        first_map = {}
        for rec in first_groups:
            if rec.get('sale_installment_id.department'):
                first_map[
                    rec['sale_installment_id.department'][0]
                ] = rec['__count']

        # ==========================================================
        # First Installment Paid Student Type Wise
        # ==========================================================
        student_groups = Installment.read_group(
            installment_domain + [
                ('payment_status', '=', 'paid'),
                ('number', '=', 1),
            ],
            ['student'],
            ['student'],
            lazy=False,
        )

        student_map = {}
        for rec in student_groups:
            if rec.get('sale_installment_id.student'):
                student_map[
                    rec['sale_installment_id.student'][0]
                ] = rec['__count']

        # ==========================================================
        # Department Graphs
        # ==========================================================
        departments = Department.search([])

        for dept in departments:
            total = total_map.get(dept.id, 0)
            second_paid = second_map.get(dept.id, 0)
            first_paid = first_map.get(dept.id, 0)

            percentage = round(
                (second_paid * 100.0) / total, 2
            ) if total else 0

            result['second_installment_percentage'].append({
                'department': dept.department,
                'percentage': percentage,
            })

            result['first_installment_department'].append({
                'department': dept.department,
                'count': first_paid,
            })

        # ==========================================================
        # Student Type Graph
        # ==========================================================
        students = StudentType.search([])

        for student in students:
            result['first_installment_student_type'].append({
                'student_type': student.Student,
                'count': student_map.get(student.id, 0),
            })

        return result
    

    # first_paid = self.env['sale.installment'].search_count([
    #     ('sequence', '=', 1),
    #     ('payment_status', '=', 'paid')
    # ])

    # second_paid = self.env['sale.installment'].search_count([
    #     ('sequence', '=', 2),
    #     ('payment_status', '=', 'paid')
    # ])
        
    # third_paid = self.env['sale.installment'].search_count([
    #     ('sequence', '=', 3),
    #     ('payment_status', '=', 'paid')
    # ])


    # departments = self.env['department.department'].search([])

    # result = []


    # # first graphn with 2nd payment installment percentage calculation

    # for dept in departments:

    #     total = self.env['sale.order'].search_count([
    #         ('department', '=', dept.id)
    #     ])

    #     paid = self.env['sale.installment'].search_count([
    #         ('sequence', '=', 2),
    #         ('payment_status', '=', 'paid'),
    #         ('sale_installment_id.department', '=', dept.id)
    #     ])

    #     percentage = (paid / total * 100) if total else 0

    #     result.append({
    #         'department': dept.name,
    #         'percentage': round(percentage, 2),
    #     })

    # # first graphn with 2nd payment installment percentage calculation
    # for dept in departments:

    # count = self.env['sale.installment'].search_count([
    #     ('sequence', '=', 1),
    #     ('payment_status', '=', 'paid'),
    #     ('sale_id.department_id', '=', dept.id)
    # ])    


    # supports = self.env['student.support'].search([])

    # for support in supports:

    #     count = self.env['sale.installment'].search_count([
    #         ('sequence', '=', 1),
    #         ('payment_status', '=', 'paid'),
    #         ('sale_id.partner_id.student_support_id', '=', support.id)
    #     ])











    # @api.model
    # def get_dashboard_data(self, filters=None):

    #     domain = []

    #     if filters.get('year'):
    #         domain.append(
    #             ('year.year', '=', int(filters['academic_year_id']))
    #         )

    #     if filters.get('year_of_acceptance_1'):
    #         domain.append(
    #             ('year_of_acceptance_1.name', '=', int(filters['acceptance_year_id']))
    #         )

    #     students = self.env['sale.order'].search(domain)

    #     department_count = self.env['sale.order'].search(domain)

    #     students = self.env['sale.order'].search(domain)

    #     print("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn",len(students))

    #     return {
    #         'total_students': len(students),
    #         'department_count': self.get_dept_employee(),
    #         'shift_count': self.get_dept_employee_shift(),
    #     }


    @api.model
    def get_grant_discount_graph(self, filters=None):
        result = []

        grants = self.env['level.level'].search([])

        for grant in grants:
            count = self.env['sale.order'].search_count([
                ('student', '=', grant.id),('year_of_acceptance_1.name', '=', filters['acceptance_year_id'])
            ])

            result.append({
                'label': grant.Student,
                'value': count,
            })

        return result


    @api.model
    def get_dashboard_data(self, filters=None):
        filters = filters or {}

        domain = []

        if filters.get('academic_year_id'):
            domain.append(
                ('year.year', '=', filters['academic_year_id'])
            )

        if filters.get('acceptance_year_id'):
            domain.append(
                ('year_of_acceptance_1.name', '=', filters['acceptance_year_id'])
            )

        # Department Filter
        if filters.get('department_id'):
            domain.append(
                ('department', '=', filters['department_id'])
            )

        _logger.info("Filters: %s", filters)
        _logger.info("Domain: %s", domain)

        orders = self.env['sale.order']

        department_data = []

        departments = orders.read_group(
            domain,
            ['department'],
            ['department']
        )

        for dept in departments:

            if not dept.get('department'):
                continue

            dept_id = dept['department'][0]
            dept_name = dept['department'][1]

            dept_domain = domain + [
                ('department', '=', dept_id)
            ]

            shift_data = []

            for shift in ['morning', 'evening']:

                shift_domain = dept_domain + [
                    ('Subject', '=', shift)
                ]

                shift_count = orders.search_count(shift_domain)

                student_groups = orders.read_group(
                    shift_domain,
                    ['student'],
                    ['student']
                )

                student_types = []

                for st in student_groups:
                    student_types.append({
                        'student_type': st['student'][1] if st.get('student') else '',
                        'count': st.get('student_count', 0),
                    })

                shift_data.append({
                    'shift': shift,
                    'count': shift_count,
                    'student_types': student_types,
                })

            department_data.append({
                'id': dept_id,
                'department': dept_name,
                'count': orders.search_count(dept_domain),
                'shifts': shift_data,
            })

        return {
            'total_students': orders.search_count(domain),
            'department_data': department_data,
        }
    


