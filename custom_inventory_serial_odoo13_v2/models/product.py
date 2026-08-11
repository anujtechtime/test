# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_test_code = fields.Char(
        string='Product Test Code',
        copy=False,
        help='Unique product code used as the product portion of the generated serial.'
    )
