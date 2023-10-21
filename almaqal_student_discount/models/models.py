# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class almaqal_student_discount(models.Model):
    _name = 'student.grade'
    _description = 'student.grade'

    shift = fields.Selection([('morning','Morning'),('afternoon','AfterNoon')], string="Shift")
    percentage_from = fields.Float("Percentage From")
    percentage_to = fields.Float("Percentage To")
    amount = fields.Char("Amount")

class InheritData(models.Model):
    _inherit = 'faculty.faculty'

    student_discoubt = fields.Many2many("student.grade", string="Student CGPA (Discount)")

class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    student_cgpa = fields.Float("Student CGPA")

class InstallmentDetails(models.Model):
    _inherit = "installment.details"

    student_dicount = fields.Boolean("Student Dicount")
    percentage_from = fields.Float("Percentage From")
    percentage_to = fields.Float("Percentage To")

class ResPrtner(models.Model):
    _inherit = 'sale.order'

    # @api.onchange('partner_id')
    # def _compute_partner_id(self):
    #     print("college################eeeeeeeeeeeeeeee",self.college.student_discoubt) 
    #     for cgpa in self.college.student_discoubt:
    #         if self.partner_id.shift >=  cgpa.shift and self.partner_id.student_cgpa >=  cgpa.percentage_from and self.partner_id.student_cgpa <=  cgpa.percentage_to:
    #             self.installment_amount = cgpa.amount
    #             instamm_ment_details = self.env["installment.details"].search([("student_dicount","=",True),("installment","=",cgpa.amount)])
    #             if instamm_ment_details:
    #                 for i in instamm_ment_details.sale_installment_line_ids:
    #                     sale_installment = self.sale_installment_line_ids.create({
    #                         'number' : i.number,
    #                         'payment_date' : i.payment_date,
    #                         'amount_installment' : i.amount_installment,
    #                         'description': 'Installment Payment',
    #                         'sale_installment_id' : result.id,
    #                         # "invoice_id" : invoice_id.id
    #                         })

    @api.model
    def create(self, vals):
        result = super(ResPrtner, self).create(vals)
        print("result##############",result)    
        print("result.college###########",result.college,result.department,result.student, result.year)
        installmet_dat = result.env["installment.details"].search([('college' , '=', result.college.id),("level","=",result.level),("Subject","=",result.Subject),('department','=',result.department.id),('Student','=',result.student.id),('year','=', result.year.id)],limit=1)
        print("result.id#$$$$$$$$$$$$$$$",installmet_dat)
        instamm_ment_details = self.env["installment.details"].search([("student_dicount","=",True),('college','=',self.college.id),('shift','=',self.partner_id.shift),('year','=',self.year.id),('department','=',self.department.id),('percentage_from','>=',self.partne_id.final_result),('percentage_to','<=',self.partne_id.final_result)])
        print("installmet_dat@@@@@@@@@@@@@@@",installmet_dat)
        if installmet_dat:
            print("sale_installment_line_ids########",installmet_dat.sale_installment_line_ids.ids)
            # for datts in installmet_dat.sale_installment_line_ids:
            # result.sale_installment_line_ids = [(6, 0, installmet_dat.sale_installment_line_ids.ids)]
            result.installment_amount = installmet_dat.installment
            # result.payable_amount = installmet_dat.installment / installmet_dat.installment_number
            result.tenure_month = installmet_dat.installment_number
            result.second_payment_date = datetime.today().date()
            order_line = result.env['sale.order.line'].create({
                'product_id': 1,
                'price_unit': result.installment_amount,
                'product_uom': result.env.ref('uom.product_uom_unit').id,
                'product_uom_qty': 1,
                'order_id': result._origin.id,
                'name': 'sales order line',
            })
        failed_student = self.env["sale.order"].search([("partner_id","=",result.partner_id.id),("college","=",result.partner_id.college.id),("year","!=",result.partner_id.year.id),("level","=",result.partner_id.level)], limit=1)
        print("failed_student@@@@@@@@@@@@@@@@",failed_student)
        _logger.info("failed_student************11111111111111#####**%s" %failed_student)
        if failed_student:
            result.installment_amount = failed_student.installment_amount
            for i in failed_student.sale_installment_line_ids:
                installment = result.sale_installment_line_ids.create({
                'number' : i.number,
                'payment_date' : i.payment_date,
                'amount_installment' : i.amount_installment,
                'description': 'Installment Payment',
                'sale_installment_id' : result.id,
                # "invoice_id" : invoice_id.id
                })  
        if not failed_student and installmet_dat:
            count = 0
            if instamm_ment_details:
                self.installment = instamm_ment_details.installment
                if instamm_ment_details:
                    for i in instamm_ment_details.sale_installment_line_ids:
                        sale_installment = self.sale_installment_line_ids.create({
                            'number' : i.number,
                            'payment_date' : i.payment_date,
                            'amount_installment' : i.amount_installment,
                            'description': 'Installment Payment',
                            'sale_installment_id' : result.id,
                            # "invoice_id" : invoice_id.id
                            })
            else:            
                for i in installmet_dat.sale_installment_line_ids:
                    sale_installment = result.sale_installment_line_ids.create({
                        'number' : i.number,
                        'payment_date' : i.payment_date,
                        'amount_installment' : i.amount_installment,
                        'description': 'Installment Payment',
                        'sale_installment_id' : result.id,
                        # "invoice_id" : invoice_id.id
                        })
                    count = count + 1          

        return result


    @api.onchange('partner_id')
    def _compute_partner_id(self):
        if self.partner_id:
            # if self.partner_id.shift >=  cgpa.shift and self.partner_id.student_cgpa >=  cgpa.percentage_from and self.partner_id.student_cgpa <=  cgpa.percentage_to:
            instamm_ment_details = self.env["installment.details"].search([("student_dicount","=",True),('college','=',self.college.id),('shift','=',self.partner_id.shift),('year','=',self.year.id),('department','=',self.department.id),('percentage_from','>=',self.partne_id.final_result),('percentage_to','<=',self.partne_id.final_result)])
            self.installment = instamm_ment_details.installment
            if instamm_ment_details:
                for i in instamm_ment_details.sale_installment_line_ids:
                    sale_installment = self.sale_installment_line_ids.create({
                        'number' : i.number,
                        'payment_date' : i.payment_date,
                        'amount_installment' : i.amount_installment,
                        'description': 'Installment Payment',
                        'sale_installment_id' : result.id,
                        # "invoice_id" : invoice_id.id
                        })

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
