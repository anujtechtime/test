# -*- coding: utf-8 -*-

from odoo import models, fields, api

class almaaqal_record_access(models.Model):

    _inherit = "faculty.faculty"

    res_user = fields.Many2many("res.users", string="Users")

class almaaqalRecordaccesAMs(models.Model):

    _inherit = "department.department"

    res_user = fields.Many2many("res.users", string="Users")    


# class almaaqal_record_access(models.Model):
#     _name = 'almaaqal_record_access.almaaqal_record_access'
#     _description = 'almaaqal_record_access.almaaqal_record_access'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
