# -*- coding: utf-8 -*-

from odoo import models, fields, api , _ 
from odoo.exceptions import UserError, ValidationError


class almaqal_templates(models.Model):
    _inherit = "sale.order"

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            year_active  = self.env["year.year"].search([("active", "=", True)])
            if self.year.id not in year_active.mapped("id"):
                raise ValidationError(_('الطالب لم يرحل. هل تريد اكمال عملية التسجيل؟'))
#     _name = 'almaqal_templates.almaqal_templates'
#     _description = 'almaqal_templates.almaqal_templates'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
