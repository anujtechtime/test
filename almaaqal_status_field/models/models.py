# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class almaaqal_status_field(models.Model):
    _name = 'status.type'
    _description = 'status.type'

    name = fields.Char("Name")

class almaaqalStatusResm(models.Model):
    _inherit = 'res.partner'
    _description = 'status.type'

    status_type = fields.Many2one("status.type",string="Status Type")    


class almaaqalStatusCHanng(models.Model):
    _inherit = 'status.change'

    status_type = fields.Many2one("status.type",string="Status Type")

    def action_confirm_change_level(self):
        result = super(almaaqalStatusCHanng, self).action_confirm_change_level()
        for ddts in self:
            for idds in ddts._context.get("active_id"):
                levels_sale_order = self.env["res.partner"].browse(int(idds))
                levels_sale_order.status_type = ddts.status_type.id

        return result
    
class SaleStatusType(models.Model):
    _inherit = 'sale.order'

    status_type = fields.Many2one("status.type",string="Status Type")    

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
