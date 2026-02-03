# -*- coding: utf-8 -*-

from odoo import models, fields, api , _


# class almaaqal_wizard_contact(models.Model):
#     _name = 'almaaqal_wizard_contact.almaaqal_wizard_contact'
#     _description = 'almaaqal_wizard_contact.almaaqal_wizard_contact'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class WizardDocs(models.TransientModel):
    _name = 'wizard.docs'
   
    date_map = fields.Date("Date")

    docs_option = fields.Selection([
        ('ppd1', ' الاستاذ الدكتور بدر نعمه عكاش البدران رئيس جامعة'),
        ('ppd2',' أ.م.د محمد جاسم الاسديمساعد رئيس الجامعة للشؤون العلمية')
    ], string="اختر اسم المخول")
    Target = fields.Text("Target")
    docs_name = fields.Selection([
        ('pdf1', 'طلب جلب شهادة'),
        ('pdf2', 'تأييد')
    ], string='طلبات', default='pdf1')

    
    
    def action_confirm_change_status(self):
        print("res@@@@@@@@@@@@@@@@@@@@@@@@@@26666",self._context.get("active_id"))
        for idds in self._context.get("active_id"):
            if self.docs_name == 'pdf2':
                report = self.env['ir.actions.report'].browse(1270)
            if self.docs_name == 'pdf1':
                report = self.env['ir.actions.report'].browse(1269)


            if self.docs_option == 'ppd1':
                self_data.docs_option = ' الاستاذ الدكتور بدر نعمه عكاش البدران رئيس جامعة'
            if self.docs_option == 'ppd2':
                self_data.docs_option = ' أ.م.د محمد جاسم الاسديمساعد رئيس الجامعة للشؤون العلمية'
            
            self_data = self.env["res.partner"].search([("id","=",idds)])
            depp = ""
            shift_name = ""
            lev = self_data.level
            shift = self_data.shift

            if lev == 'leve1':
                depp = 'المرحلة الاولى'
            if lev == 'level2':
                depp = 'المرحلة الثانية'
            if lev == 'level3':
                depp = 'المرحلة الثالثة'
            if lev == 'level4':
                depp = 'المرحلة الرابعة'
            if lev == 'level5':
                depp = 'المرحلة الخامسة'


            if shift == 'morning':
                shift_name = 'صباحي'
            if shift == 'afternoon':    
                shift_name = 'مسائي'
                
            self_data.date_map = self.date_map
            self_data.Target = self.Target
            self_data.level_name_work = depp
            self_data.shift_name_work = shift_name
            # self_data.docs_option = self.docs_option
            
            return report.report_action(self_data)

            # print("idds@@@@@@@@@@@@@@@@@",idds)
            # levels_sale_order = self.env["sale.order"].browse(int(idds))
            # levels_sale_order.Status = self.Status
            # levels_sale_order.partner_id.Status = self.Status

class WizardResPart(models.Model):
    _inherit = "res.partner"

    date_map = fields.Date("Date")
    Target = fields.Text("Target")
    level_name_work = fields.Char("Level work")
    shift_name_work = fields.Char("Level work")
    docs_option = fields.Char("docs_option")

    def action_done_download_docs(self):
        print("self._context##################",self._context.get("active_ids"))
        return {'type': 'ir.actions.act_window',
        'name': _('Download the Report'),
        'res_model': 'wizard.docs',
        'target': 'new',
        'view_id': self.env.ref('almaaqal_wizard_contact.view_any_name_wizard_download_val').id,
        'view_mode': 'form',
        'context': {"active_id" : self._context.get("active_ids")}
        }
            
            