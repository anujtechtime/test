from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    location_wise_qty = fields.Float(string='Quantity')

    @api.model
    def get_location_qty(self, picking_type_id):
        product_list = []
        products = self.env['product.product'].search([
            ('available_in_pos', '=', True)
        ])
        picking_type = self.env['stock.picking.type'].search([
            ('id', '=', picking_type_id)
        ])
        for product_id in products:
            if picking_type:
                if picking_type.default_location_src_id:
                    stock_quants = self.env['stock.quant'].search([
                        ('location_id', '=', picking_type.default_location_src_id.id),
                        ('product_id', '=', product_id.id)
                    ])
                    qunatity = 0
                    for quant in stock_quants:
                        qunatity += quant.quantity

                    product_list.append({
                        'id': product_id.id,
                        'name': product_id.name,
                        'location_wise_qty': qunatity,
                    })
        return product_list
