# -*- coding: utf-8 -*-

from collections import defaultdict
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd
from pytz import utc
from odoo import models, fields, api, _
from odoo.http import request
from odoo.tools import float_utils

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
                    'age': age
                }
                print("data#############",data)
                employee[0].update(data)
            return employee
        else:
            return False

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
        print("ddt##################",ddt)    
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
        print("dat@@@@@@@@@@@@@@datdatdatdat",dat)
        data = []
        for i in range(0, len(dat)):
            print("dat[i]##############",dat[i])
            data.append({'label': dat[i][0], 'value': dat[i][1]})
        print("get_dept_employee###################",data)    
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

    #     print("days#################",days)
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
            print("res################",res)
            vals = {
                'l_month': month.Student,
                'leave': res
            }
            value = value + res
            graph_result.append(vals)
        print("graph_resultgggggffffffffffffffffffff",graph_result)    
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
            print("last_month###################",last_month)
            text = format(last_month, '%B %Y')
            month_list.append(text)
            print("month_list@@@@@@@@@@@@@@",month_list)
            
        college_info = self.env['faculty.faculty'].sudo().search([])
          
        for month in college_info:
            res = 0
            res = self.env["res.partner"].sudo().search_count([('college','=',month.id)])
            print("res################",res)
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

        print("graph_resultkkkkkkkkkkkkkkkkkkkkkkkkkk",graph_result)
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

        print("graph_resultkkkkkkkkkkkkkkkkkkkkkkkkkk",graph_result)
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
        # print("month_attrition#################",month_attrition)

        # month_attrition################# [{'month': 'May', 'attrition_rate': 0.0}, {'month': 'Apr', 'attrition_rate': 0.0}, {'month': 'Mar', 'attrition_rate': 0.0}, {'month': 'Feb', 'attrition_rate': 0.0}, {'month': 'Jan', 'attrition_rate': 0.0}, {'month': 'Dec', 'attrition_rate': 0.0}, {'month': 'Nov', 'attrition_rate': 0.0}, {'month': 'Oct', 'attrition_rate': 0.0}, {'month': 'Sep', 'attrition_rate': 0.0}, {'month': 'Aug', 'attrition_rate': 0.0}, {'month': 'Jul', 'attrition_rate': 0.0}, {'month': 'Jun', 'attrition_rate': 0.0}]

        return month_attrition