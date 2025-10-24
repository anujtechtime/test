
# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartnerStage(models.Model):
    _name = 'res.partner.stage'
    _description = 'Customer Level'

    name = fields.Char(string='المستوى', required=True, translate=True)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    stage_id = fields.Many2one(
        'res.partner.stage',
        string='المستوى',
        help='Customer level',
    )


class RespersistentModel(models.Model):
    _inherit = 'persistent.model'

    stage_id = fields.Many2one(
        'res.partner.stage',
        string='المستوى',
        help='Customer level',
    )

    def action_confirm_change(self):
        res = super(RespersistentModel, self).action_confirm_change()
        print("self########33333444444444444444",self.res_part)
        if self.stage_id:
            self.res_part.stage_id = self.stage_id.id
        return res

