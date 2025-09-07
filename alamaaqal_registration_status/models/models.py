# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RegistrationStatus(models.Model):
    _name = "registration.status"
    _description = "Registration Status"

    name = fields.Char(string="name")

class ResPartreg(models.Model):
    _inherit = "res.partner"  

    contact_type = fields.Selection([("student","طالب"),("teacher", "مدرس"),("admin","موظف")], string="Contact Type", tracking=True)  

    def assign_registrtion_status(self):
        for ddt in self:
            level = ""
            sale_ord = self.env["sale.order"].search([("partner_id","=",ddt.id)], order="id asc")
            print("sale_ord@@@@@@@@@@@@@@@@",sale_ord)
            for sal in sale_ord:
                if sal.level == level:
                    sal.registration_status = 2
                if sal.level != level:
                    sal.registration_status = 1
                    
                level = sal.level

class SaleOrdReg(models.Model):
    _inherit = "sale.order"

    registration_status = fields.Many2one("registration.status", string="Registration Status")

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        result = super(SaleOrdReg, self).onchange_partner_id()
        # _logger.info("result************11111111111111#####**%s" %result)
        if self.partner_id:
            self.registration_status = self.partner_id.registration_status
            self.status_type = self.partner_id.status_type
        return result


class SubjectSubjectD(models.Model):
    _inherit = 'subject.subject'

    status_type = fields.Selection([('option1', 'ناجح دور اول'),('option2','ناجح دور ثاني'),('option3','ناجح بالعبور'),('option4','راسب بالدرجات'),('option5','راسب بالغياب')], string="Status Type")

    status_in_year = fields.Char("status in year")
    semrating2 = fields.Char("semrating2")
    rating_in_year = fields.Char("rating in year")
    level = fields.Char("Level")
    note = fields.Char("Note")

class DataLevelStatusInh(models.Model):
    _inherit = 'status.change'


    student_type = fields.Many2one("level.level", string="Student Type")  

# class alamaaqal_registration_status(models.Model):
#     _name = 'alamaaqal_registration_status.alamaaqal_registration_status'
#     _description = 'alamaaqal_registration_status.alamaaqal_registration_status'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
