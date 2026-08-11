# -*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    prefix_code = fields.Char(
        string='Product Prefix Code',
        copy=False,
        index=True,
        help='Prefix used when generating serial/lot numbers for this product.',
    )
