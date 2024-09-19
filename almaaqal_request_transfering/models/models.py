# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class almaaqal_request_transfering(models.Model):
#     _name = 'almaaqal_request_transfering.almaaqal_request_transfering'
#     _description = 'almaaqal_request_transfering.almaaqal_request_transfering'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
