
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
