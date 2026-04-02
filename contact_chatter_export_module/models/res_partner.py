
from odoo import models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_export_chatter(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Export Chatter',
            'res_model': 'partner.chatter.export.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_partner_id': self.id}
        }
