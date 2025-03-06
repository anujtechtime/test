# -*- coding: utf-8 -*-

from odoo import models, fields, api , _

import logging

_logger = logging.getLogger(__name__)

class ResPart(models.Model):
    _inherit = "res.partner"

    Status = fields.Selection(
        selection_add=[("hosting_university", " استضافة من الجامعة")],
    )
    
    graduation_source = fields.Many2one("graduation.source", string="جهة التخرج ")
    nationalty_source = fields.Many2one("nationality.source", string="الجنسية ")
    second_nationality_source = fields.Many2one("nationality.source", string="الجنسيه الثانويه ")
    remark_data_change_2 = fields.Many2many("status.change",store = True)

    remark_data_change_level = fields.Many2many("persistent.model",store = True)

    data_one = fields.Many2one("new.work", string="نافذة القبول")
    academic_branch = fields.Char("Academi Branch")
    rfid = fields.Char("RFID")
    transferred_college = fields.Boolean("نقل من الجامعه ")
    d_date = fields.Date("#Date", track_visibility=True)
 
    n_notes = fields.Text("#Notes", track_visibility=True)
    s_sequence = fields.Char("#Sequence", track_visibility=True)

    batch_namee = fields.Many2one("batch.name", string="اسم الدفعه")
    attempt = fields.Many2one("attempt.attempt", string="الدور")
    year_of_collage_graduation = fields.Many2one("collage.graduation", string="سنه التخرج ")

    student_Lack_of_information  = fields.Boolean("نقص في معلومات الطلبه")
    Mother_Name_in_AR = fields.Char("Mother Name in AR")
    Mother_Name_in_EN = fields.Char("Mother Name in EN")
    ID_Unified_Number =  fields.Char("رقم الهويه الموحده")
    ID_Unified_Number_date = fields.Date("تاريخ اصدار الهوي ه الموحده")

    name_of_school_graduated_from_1 = fields.Many2one("name.school",string="اسم المدرسة", tracking=True)
    State_of_school_graduated_from_1 = fields.Many2one("state.school", string="State of school graduated from", tracking=True)

    

    

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
                        change_logs = chg.env['persistent.model'].sudo().create({
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
                    chg.write({'remark_data_change_level': [(4, change_logs.id)]})

    def action_done_show_wizard_level_status(self):
        return {'type': 'ir.actions.act_window',
        'name': _('Change the Status'),
        'res_model': 'status.change',
        'target': 'new',
        'view_id': self.env.ref('almaaqal_fields.view_any_name_form_status_change').id,
        'view_mode': 'form',
        'context': {"active_id" : self._context.get("active_ids")}
        }

    def action_done_show_wizard_persistent_model(self):
        return {'type': 'ir.actions.act_window',
        'name': _('Change the Level Value'),
        'res_model': 'persistent.model',
        'target': 'new',
        'view_id': self.env.ref('almaaqal_fields.view_any_name_form_persistent_model').id,
        'view_mode': 'form',
        'context': {"active_id" : self._context.get("active_ids")}
        }    


class BatchModel(models.Model):
    _name = 'batch.name'
    _description = 'اسم الدفعه'

    name = fields.Char("اسم الدفعه")

class AttemptModel(models.Model):
    _name = 'attempt.attempt'
    _description = 'الدور'

    name = fields.Char("الدور")

class CollGradtModel(models.Model):
    _name = 'collage.graduation'
    _description = 'سنه التخرج'

    name = fields.Char("سنه التخرج")        


class NameSchool(models.Model):
    _name = 'name.school'
    _description = 'المدرسه التي تخرج منها '

    name = fields.Char("المدرسه التي تخرج منها ")

class StateSchool(models.Model):
    _name = 'state.school'
    _description = 'المحافظه'

    name = fields.Char("المحافظه")
    


class PersistentModel(models.Model):
    _name = 'persistent.model'
    _description = 'Persistent Model'
    _inherit = 'level.value'

    res_part = fields.Many2one("res.partner")   
    notes_data = fields.Text("Notes", track_visibility=True)
    data_date_value = fields.Date("Date", track_visibility=True)
    sequence_num = fields.Char("Sequence", track_visibility=True)
    attachment = fields.Many2many("ir.attachment",  string="Attachment")

    Status = fields.Selection([('currecnt_student','Current student'),('succeeded','Succeeded'),('failed','Falied'),('transferred_from_us','Transferred From Us'),('graduated','Graduated')], string="Status")
    contact_type = fields.Selection([("student","طالب"),("teacher", "مدرس")], string="Contact Type", tracking=True)

    def action_confirm_change(self):
        for ddts in self:
            for idds in ddts._context.get("active_id"):
                levels_sale_order = self.env["res.partner"].browse(int(idds))
                # print("levels_sale_order@@@@@@@@@@@@@@@@@@@@@@@@",levels_sale_order)
                levels_sale_order.remark_data_change_level  = [(4, ddts.id)]
                ddts.res_part = levels_sale_order.id
                if ddts.level:
                    levels_sale_order.level = ddts.level
                    # levels_sale_order.partner_id.level = self.level

                if ddts.year:    
                    levels_sale_order.year = ddts.year
                    # levels_sale_order.partner_id.year = self.year

                if ddts.Status:    
                    levels_sale_order.Status = ddts.Status
                    # levels_sale_order.partner_id.Status = self.Statuos
                    
                if ddts.contact_type:
                    levels_sale_order.contact_type = ddts.contact_type
                if ddts.notes_data:
                    levels_sale_order.notes_data = ddts.notes_data
                if ddts.data_date_value:
                    levels_sale_order.data_date_value = ddts.data_date_value
                if ddts.sequence_num:
                    levels_sale_order.sequence_num = ddts.sequence_num

                if ddts.attachment:
                    levels_sale_order.attachment =  [(6, 0, ddts.attachment.mapped("id"))]
                    # for pdf in self.attachment:
                    #     attachments.append(pdf.id)

                    levels_sale_order.message_post(attachment_ids=self.attachment.mapped("id")) 


    

class DataLevelStatus(models.Model):
    _name = 'status.change'


    Status = fields.Selection([('status4', 'مؤجل'),('status1','ترقين قيد'),('status2','طالب غير مباشر'),('status3','انسحاب'),('currecnt_student','طالب حالي '),('succeeded','ناجح '),('failed','راسب '),('transferred_from_us','نقل من جامعتنا '),('graduated','متخرج ')], string="حالة الطالب ")
    transferred_to_us = fields.Boolean("نقل الئ الجامعة ") 
    transfer_shift = fields.Boolean("Transferred Shift ")
    chckbox_data = fields.Boolean("نقل من كلية الى أخرى")

    chckbox_data_2 = fields.Boolean("نقل من جامعة")

    boolean_one = fields.Boolean(string="أبناء الهيئة التدريسية", tracking=True)
    boolean_two = fields.Boolean(string="أبناء أصحاب الشهادات العليا في وزارات أخرى", tracking=True)
    boolean_three = fields.Boolean(string="الوافدين", tracking=True)
    boolean_four = fields.Boolean(string="السجناء السياسيين", tracking=True)

    res_part_2 = fields.Many2one("res.partner")   
    notes_data = fields.Text("الملاحظات ", track_visibility=True)
    data_date_value = fields.Date("التاريخ", track_visibility=True)
    sequence_num = fields.Char("التسلسل ", track_visibility=True)
    attachment = fields.Many2many("ir.attachment",  string="المرفقات ")

    batch_namee = fields.Many2one("batch.name", string="اسم الدفعه")
    attempt = fields.Many2one("attempt.attempt", string="الدور")
    year_of_collage_graduation = fields.Many2one("collage.graduation", string="سنه التخرج ")


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


                if ddts.data_date_value:
                    levels_sale_order.d_date = ddts.data_date_value
                if ddts.notes_data:
                    levels_sale_order.n_notes = ddts.notes_data
                if ddts.sequence_num:
                    levels_sale_order.s_sequence = ddts.sequence_num
                # levels_sale_order.a_attachment = ddts.attachment

                if ddts.attachment:
                    levels_sale_order.attachment =  [(6, 0, ddts.attachment.mapped("id"))]
                    # for pdf in self.attachment:
                    #     attachments.append(pdf.id)

                    levels_sale_order.message_post(attachment_ids=ddts.attachment.mapped("id")) 
                if ddts.Status:
                    levels_sale_order.Status = ddts.Status


                if ddts.batch_namee:
                    levels_sale_order.batch_namee = ddts.batch_namee.id
                if ddts.attempt:
                    levels_sale_order.attempt = ddts.attempt.id
                if ddts.year_of_collage_graduation:
                    levels_sale_order.year_of_collage_graduation = ddts.year_of_collage_graduation.id

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
         

class TechtimeNewWork(models.Model):
    _name = 'graduation.source'
    _description = 'نافذة القبول'

    name = fields.Char("نافذة القبول")      

class TechtimeNationality(models.Model):
    _name = 'nationality.source'
    _description = 'الجنسية '

    name = fields.Char("الجنسية ")      


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
