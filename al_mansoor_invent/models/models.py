# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class al_mansoor_invent(models.Model):
	_inherit = "stock.picking"

	receipt_number = fields.Char("Receipt Number")
#     _name = 'al_mansoor_invent.al_mansoor_invent'
#     _description = 'al_mansoor_invent.al_mansoor_invent'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
