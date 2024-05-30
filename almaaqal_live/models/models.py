# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class RespartnerLive(models.Model):
    _inherit = "res.partner"

    # attachment_ids_three = fields.One2many('ir.attachment', 'res_id', string='Attachments')
    attachment_live = fields.Binary('Attachment')
    attachment_name_live = fields.Char('Attachment Name')

    boolean_six = fields.Boolean("كتاب التصويب")

    attachment_six = fields.Binary('Attachment')
    attachment_name_six = fields.Char('Attachment Name')

    transferred_college = fields.Boolean("Transferred College")
    




# class almaaqal_live(models.Model):
#     _name = 'almaaqal_live.almaaqal_live'
#     _description = 'almaaqal_live.almaaqal_live'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
