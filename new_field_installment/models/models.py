# -*- coding: utf-8 -*-

from odoo import models, fields, api


import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

def pre_init_hook(cr):
    """
    Add the department column directly via SQL before Odoo's ORM tries to alter the table.
    This bypasses the foreign key constraint conflict.
    """
    # Check if column already exists
    cr.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='sale_installment' AND column_name='department'
    """)
    
    if not cr.fetchone():
        _logger.info("Adding department column to sale_installment table")
        
        # Add the column as INTEGER (since Many2one stores an integer ID)
        cr.execute("""
            ALTER TABLE sale_installment 
            ADD COLUMN department INTEGER
        """)
        
        # Populate the column with values from the related invoice
        _logger.info("Populating department column with existing data")
        cr.execute("""
            UPDATE sale_installment si
            SET department = ai.department
            FROM account_move ai
            WHERE si.invoice_id = ai.id AND ai.department IS NOT NULL
        """)
        
        _logger.info("department column added and populated successfully")
        

class MoveDiv(models.Model):
    _inherit = "account.move"

    student_status_in_department = fields.Char(" الطالب في القسم")
    Status = fields.Selection([('status4', 'مؤجل'),('status1','ترقين قيد'),('status2','طالب غير مباشر'),('status3','انسحاب'),('currecnt_student','Current student'),('succeeded','Succeeded'),('failed','Falied'),('transferred_from_us','Transferred From Us'),('graduated','Graduated')], string="Status", store=True, related="partner_id.Status")
    year_of_acceptance_1 = fields.Many2one("techtime_mcc_data.techtime_mcc_data", string="Year of acceptance", store=True, related="partner_id.year_of_acceptance_1")


# class new_field_installment(models.Model):
#     _name = 'new_field_installment.new_field_installment'
#     _description = 'new_field_installment.new_field_installment'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class SaleMembershipInt(models.Model):
    _inherit = 'sale.installment'

    department = fields.Many2one(
        'department.department',
        related='invoice_id.department',
        store=True,
        readonly=True,
    )

