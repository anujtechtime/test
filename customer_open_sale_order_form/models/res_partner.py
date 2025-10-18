from odoo import models, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_open_new_sale_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('New Sale Order'),
            'res_model': 'sale.order',
            'view_mode': 'form',
            'target': 'current',
            'context': {'default_partner_id': self.id, 'default_year': self.year.id, 'default_college': self.college.id, 'default_department': self.department.id, 'default_Student': self.student_type.id, 'default_shift': self.shift, 'default_level': self.level},
        }
