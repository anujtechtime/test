# -*- coding: utf-8 -*-

from odoo import models, fields, api , _

class ResPart(models.Model):
    _inherit = "res.partner"

    graduation_source = fields.Many2one("graduation.source", string="Graduation Source")
    nationalty_source = fields.Many2one("nationality.source", string="Nationality")
    second_nationality_source = fields.Many2one("nationality.source", string="Second Nationality")
    remark_data_change_2 = fields.One2many("status.change","res_part_2",store = True)


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
        print("res@@@@@@@@@@@@@@@@@@@@@@@@@@26666",self._context.get("active_id"))
        for idds in self._context.get("active_id"):
            print("idds@@@@@@@@@@@@@@@@@",idds)
            levels_sale_order = self.env["res.partner"].browse(int(idds))
            print("levels_sale_order@@@@@@@@@@@@@@",levels_sale_order)
            self.res_part_2 = levels_sale_order.id
            levels_sale_order.remark_data_change_2  = [(4, self.id)]



            levels_sale_order.Status = self.Status
            levels_sale_order.transferred_to_us = self.transferred_to_us
            levels_sale_order.transfer_shift = self.transfer_shift
            levels_sale_order.chckbox_data = self.chckbox_data
            levels_sale_order.chckbox_data_2 = self.chckbox_data_2
            levels_sale_order.boolean_one = self.boolean_one
            levels_sale_order.boolean_two = self.boolean_two
            levels_sale_order.boolean_three = self.boolean_three
            levels_sale_order.boolean_four = self.boolean_four
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
