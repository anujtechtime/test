# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class almaaqalStatusDone(models.Model):
    _inherit = 'res.partner'
    _description = 'status.type'

    registration_status = fields.Many2one("registration.status")


class almaaqalStatusTypem(models.Model):
    _inherit = 'sale.order'
    _description = 'status.type'

    status_type = fields.Many2one("status.type",string="Status Type")  

class PersistentModelinher(models.Model):
    _inherit = ['persistent.model', 'level.value']

    registration_status = fields.Many2one("registration.status")   
    status_type = fields.Many2one("status.type",string="Status Type")  

    def action_confirm_change(self):
        res = super(PersistentModelinher, self).action_confirm_change()
        print("self########33333444444444444444",self.res_part)
        if self.registration_status:
            self.res_part.registration_status = self.registration_status
        if self.status_type:
            self.res_part.status_type = self.status_type    
        return res
    
        # for ddts in self:
        #     for idds in ddts._context.get("active_id"):
        #         levels_sale_order = self.env["res.partner"].browse(int(idds))
        #         # print("levels_sale_order@@@@@@@@@@@@@@@@@@@@@@@@",levels_sale_order)
        #         levels_sale_order.remark_data_change_level  = [(4, ddts.id)]
        #         ddts.res_part = levels_sale_order.id
        #         if ddts.level:
        #             levels_sale_order.level = ddts.level
        #             # levels_sale_order.partner_id.level = self.level

        #         if ddts.year:    
        #             levels_sale_order.year = ddts.year
        #             # levels_sale_order.partner_id.year = self.year

        #         if ddts.Status:    
        #             levels_sale_order.Status = ddts.Status
        #             # levels_sale_order.partner_id.Status = self.Status
                    
        #         if ddts.contact_type:
        #             levels_sale_order.contact_type = ddts.contact_type
        #         if ddts.notes_data:
        #             levels_sale_order.notes_data = ddts.notes_data
        #         if ddts.data_date_value:
        #             levels_sale_order.data_date_value = ddts.data_date_value
        #         if ddts.sequence_num:
        #             levels_sale_order.sequence_num = ddts.sequence_num

        #         if ddts.attachment:
        #             levels_sale_order.attachment =  [(6, 0, ddts.attachment.mapped("id"))]
        #             # for pdf in self.attachment:
        #             #     attachments.append(pdf.id)

        #             levels_sale_order.message_post(attachment_ids=self.attachment.mapped("id")) 



# class almaaqal_edit(models.Model):
#     _name = 'almaaqal_edit.almaaqal_edit'
#     _description = 'almaaqal_edit.almaaqal_edit'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
