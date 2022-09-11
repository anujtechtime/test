# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date


class AccountAccountType(models.Model):
    _inherit = "account.account.type"
    
    type = fields.Selection(selection_add=[('view','View')])

class account_payment_account(models.Model):
    _inherit = "account.payment"

    destination_journal_id = fields.Many2one('account.journal', string='Transfer To', domain="[('type', 'in', ('bank', 'cash'))]", readonly=True, states={'draft': [('readonly', False)]})    


class alnasmi_product_fields(models.Model):
    _inherit = 'product.template'

    gold = fields.Boolean(string='Gold', default=False, translate=True)
    gold_gram = fields.Float(string='Gold Weight', default=0.0, translate=True)
    gold_purity = fields.Char(string='Purity', translate=True)
    #gold_purity = fields.Selection([(18,18), (21,21), (22,22), (24,24)], string='Purity', translate=True)
    gw = fields.Char(string='Gold Weight of Product', translate=True)
    gold_price = fields.Float(string='Gold Price', default=0.0, translate=True)
    work_price = fields.Float(string='Work Price', default=0.0, translate=True)
    make = fields.Selection([
    ('UAE', 'اماراتي'),
    ('Kuwait', 'كويتي '),
    ('Turkey', 'تركي '),
    ('Italy', 'ايطالي '),
    ('Iraq', 'عراقي '),
    ('Swiss', 'سويسري '),
    ('Bahrain', 'بحريني'),
    ('Sitash', 'سيتاش'),
    ('Hindi_Lozan', 'هندي لوزان')
    ], string='Make', translate=True)

    diamond = fields.Boolean(string='Diamond', default=False, translate=True)
    diamond_rd_carat = fields.Float(string='RD Carat', translate=True)
    diamond_rd_qty = fields.Float(string='RD QTY', translate=True)
    diamond_bd_carat = fields.Float(string='BD Carat', translate=True)
    diamond_bd_qty = fields.Float(string='BD QTY', translate=True)
    diamond_color = fields.Char(string='Color', translate=True)
    diamond_clarity = fields.Char(string='Clarity', translate=True)
    dw = fields.Char(string='Diamond Weight of Product', translate=True)

    precious_stones = fields.Boolean(string='Precious Stones', default=False, translate=True)
    precious_stones_qty = fields.Float(string='QTY', translate=True)
    precious_stones_type = fields.Char(string='Type', translate=True)
    sw = fields.Char(string='Carat', translate=True)
    pearl_carat = fields.Char(string='Pearl Carat', translate=True)

    ref_barcode = fields.Char(string='Ref. Barcode', translate=True)

    type = fields.Selection([
        ('consu', _('Consumable')),
        ('service', _('Service')),
        ('product', _('Stockable Product'))], string='Product Type', default='product', required=True,
        help='A stockable product is a product for which you manage stock. The "Inventory" app has to be installed.\n'
             'A consumable product, on the other hand, is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.\n'
             'A digital content is a non-material product you sell online. The files attached to the products are the one that are sold on '
             'the e-commerce such as e-books, music, pictures,... The "Digital Product" module has to be installed.')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    wk_loyalty_points = fields.Integer(string='Loyalty Points', help='The loyalty points the user won as part of a Loyalty Program')
    #is_loyalty_enabled = fields.Boolean(string='Loyalty Reward Enabled', help='If enabled then loyalty reward points will be added in POS')
    discount_type = fields.Selection(selection=[('none', 'Standard Discount'),('loyalty', 'Loyalty Points'),('discount_perc', 'Discount Percentage')], default='none')
    discount_percentage = fields.Integer(string="Discount Percentage", default=0.0)
    

class ProductCompaire(models.Model):
    _name = 'product.compair'

    product_id = fields.Many2one('product.product', string="Product")
    name = fields.Char(string="Name", related="product_id.name")
    default_code = fields.Char(string="Internal Reference", related="product_id.default_code")
    barcode = fields.Char(string="Barcode", related="product_id.barcode")
    record_date = fields.Date(string="Record Date",readonly=1)
    erp_quantity = fields.Integer(string='Erp Quantity',default=0, required=True)
    physical_quantity = fields.Integer(string='Physical Quantity', required=True)
    status = fields.Selection([
        ('pass', 'Pass'),
        ('less', 'Less'),
        ('more','More')], string='Status', default='less', required=True)

    @api.onchange('erp_quantity','physical_quantity')
    def onchange_erp_quantity(self):
        self.record_date = date.today()
        if self.erp_quantity > self.physical_quantity:
            self.update({
                'status': 'less'
                })
        elif self.erp_quantity < self.physical_quantity:
            self.update({
                'status': 'more'
                })
        elif self.erp_quantity == 1 and self.physical_quantity == 1:
            self.update({
                'status': 'pass'
                })    
        else:
            self.update({
                'status': 'pass'
                })


    @api.model
    def create(self, vals):
        res =  super(ProductCompaire, self).create(vals)
        res.record_date = date.today()
        if res.erp_quantity > res.physical_quantity:
            res.status = 'less'
        elif res.erp_quantity < res.physical_quantity:
            res.status = 'more'
        elif res.erp_quantity == 1 and res.physical_quantity == 1:
            res.status = 'pass'
        else:
            res.status = 'pass'
        return res 
