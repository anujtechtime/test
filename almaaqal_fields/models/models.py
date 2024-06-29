# -*- coding: utf-8 -*-

from odoo import models, fields, api , _

import logging

_logger = logging.getLogger(__name__)

class ResPart(models.Model):
    _inherit = "res.partner"

    graduation_source = fields.Many2one("graduation.source", string="Graduation Source")
    nationalty_source = fields.Many2one("nationality.source", string="Nationality")
    second_nationality_source = fields.Many2one("nationality.source", string="Second Nationality")
    remark_data_change_2 = fields.Many2many("status.change",store = True)

    def action_done_show_change_log_update(self):
        # self.ensure_one()  # Ensure the method is called on a single record
        for chg in self:
            messages = chg.env['mail.message'].search([
                ('model', '=', 'res.partner'),
                ('res_id', '=', chg.id)
            ])

            attachment_ids = chg.env['ir.attachment'].search([
                ('res_model', '=', 'mail.message'),
                ('res_id', 'in', messages.ids)
            ])
            change_logs = ""
            lev = ""
            print("self.env['level.value']@@@@@@@@@@@@@",chg)
            for message in messages:
                if len(message.tracking_value_ids) < 2:
                    if message.tracking_value_ids.field == "sequence_num":
                        change_logs = chg.env['level.value'].sudo().create({
                            "sequence_num" : message.tracking_value_ids.new_value_char
                            })
                        print("change_logs@@@@@@@@@@@@",change_logs)
                    if change_logs:    
                        if message.tracking_value_ids.field == "data_date_value":
                            change_logs.update({
                                "data_date_value" : message.tracking_value_ids.new_value_datetime
                                })

                        if message.tracking_value_ids.field == "notes_data":
                            change_logs.update({
                                "notes_data" : message.tracking_value_ids.new_value_text
                                })    

                        # if message.tracking_value_ids.field == "year":
                        #     change_logs.update({
                        #         "year" : message.tracking_value_ids.new_value_integer
                        #         })        
                        if message.tracking_value_ids.field == "level":
                            if message.tracking_value_ids.new_value_char == 'المرحلة الاولى':
                                lev = 'leve1'
                            if message.tracking_value_ids.new_value_char == 'المرحلة الثانية':
                                lev = 'level2'
                            if message.tracking_value_ids.new_value_char == 'المرحلة الثالثة':
                                lev = 'level3'
                            if message.tracking_value_ids.new_value_char == 'المرحلة الرابعة':
                                lev = 'level4'
                            if message.tracking_value_ids.new_value_char == 'المرحلة الخامسة':
                                lev =='level5'
                            change_logs.update({
                                "level" : lev
                                })   
                        if attachment_ids:
                            change_logs.update({
                                "attachment" : [(4, attachment_ids.id)]
                                })                     
                            
                if change_logs:
                    chg.write({'remark_data_change': [(4, change_logs.id)]})

    def action_done_show_wizard_level_status(self):
        return {'type': 'ir.actions.act_window',
        'name': _('Change the Status'),
        'res_model': 'status.change',
        'target': 'new',
        'view_id': self.env.ref('almaaqal_fields.view_any_name_form_status_change').id,
        'view_mode': 'form',
        'context': {"active_id" : self._context.get("active_ids")}
        }


class DataLevelStatus(models.TransientModel):
    _name = 'status.change'


    Status = fields.Selection([('status4', 'مؤجل'),('status1','ترقين قيد'),('status2','طالب غير مباشر'),('status3','انسحاب'),('currecnt_student','Current student'),('succeeded','Succeeded'),('failed','Falied'),('transferred_from_us','Transferred From Us'),('graduated','Graduated')], string="Status")
    transferred_to_us = fields.Boolean("Transferred To Us ") 
    transfer_shift = fields.Boolean("Transferred Shift ")
    chckbox_data = fields.Boolean("نقل من كلية الى أخرى")

    chckbox_data_2 = fields.Boolean("نقل من جامعة")

    boolean_one = fields.Boolean(string="أبناء الهيئة التدريسية", tracking=True)
    boolean_two = fields.Boolean(string="أبناء أصحاب الشهادات العليا في وزارات أخرى", tracking=True)
    boolean_three = fields.Boolean(string="الوافدين", tracking=True)
    boolean_four = fields.Boolean(string="السجناء السياسيين", tracking=True)

    res_part_2 = fields.Many2one("res.partner")   
    notes_data = fields.Text("Notes", track_visibility=True)
    data_date_value = fields.Date("Date", track_visibility=True)
    sequence_num = fields.Char("Sequence", track_visibility=True)
    attachment = fields.Many2many("ir.attachment",  string="Attachment")

    def action_confirm_change_level(self):
        # print("res@@@@@@@@@@@@@@@@@@@@@@@@@@26666",self._context.get("active_id"))
        for ddts in self:
            for idds in ddts._context.get("active_id"):
                print("idds@@@@@@@@@@@@@@@@@",idds)
                levels_sale_order = self.env["res.partner"].browse(int(idds))
                print("levels_sale_order@@@@@@@@@@@@@@",levels_sale_order)
                ddts.res_part_2 = levels_sale_order.id
                _logger.info("ddts************11111111111111#####**%s" %ddts)


                levels_sale_order.remark_data_change_2  = [(4, ddts.id)]


                if ddts.Status:
                    levels_sale_order.Status = ddts.Status
                if ddts.transferred_to_us:    
                    levels_sale_order.transferred_to_us = ddts.transferred_to_us

                if ddts.transfer_shift:
                    levels_sale_order.transfer_shift = ddts.transfer_shift
                if ddts.chckbox_data:
                    levels_sale_order.chckbox_data = ddts.chckbox_data
                if ddts.chckbox_data_2:
                    levels_sale_order.chckbox_data_2 = ddts.chckbox_data_2
                if ddts.boolean_one:
                    levels_sale_order.boolean_one = ddts.boolean_one
                if ddts.boolean_two:
                    levels_sale_order.boolean_two = ddts.boolean_two
                if ddts.boolean_three:
                    levels_sale_order.boolean_three = ddts.boolean_three
                if ddts.boolean_four:
                    levels_sale_order.boolean_four = ddts.boolean_four
                print("levels_sale_order.remark_data_change_2@@@@@@@@@@",levels_sale_order.remark_data_change_2)
         

class TechtimeNewWork(models.Model):
    _name = 'graduation.source'
    _description = 'graduation.source'

    name = fields.Char("نافذة القبول")      

class TechtimeNationality(models.Model):
    _name = 'nationality.source'
    _description = 'nationality.source'

    name = fields.Char("Name")      


# class almaaqal_fields(models.Model):
#     _name = 'almaaqal_fields.almaaqal_fields'
#     _description = 'almaaqal_fields.almaaqal_fields'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
