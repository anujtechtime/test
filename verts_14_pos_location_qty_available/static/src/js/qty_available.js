odoo.define('verts_14_pos_location_qty_available.qty_available', function (require) {
    "use strict";

    const pos_model = require('point_of_sale.models');
    const ProductsWidget = require('point_of_sale.ProductsWidget');
    const Registries = require('point_of_sale.Registries');
    pos_model.load_fields("product.product", ["location_wise_qty"]);

    const PosQuantityProductsWidget = ProductsWidget =>
        class extends ProductsWidget {
            constructor() {
                super(...arguments);
            }
            async willStart () {
                var self = this;
                let picking_type_id = self.env.pos.config.picking_type_id[0];
                await this.rpc({
                    model: 'product.product',
                    method: 'get_location_qty',
                    args: [picking_type_id],
                }).then(function(return_value) {
                    var returned_values = return_value;
                    $.each(returned_values, function(placeholder, product_location_qty ){
                        var product_id = self.env.pos.db.get_product_by_id(product_location_qty.id);
                        if (product_id) {
                            product_id.location_wise_qty = product_location_qty.location_wise_qty;
                        }
                    });
                });
            }
            get productsToDisplay() {
                let self = this;
                let picking_type_id = self.env.pos.config.picking_type_id[0];
                this.rpc({
                    model: 'product.product',
                    method: 'get_location_qty',
                    args: [picking_type_id],
                }).then(function(return_value) {
                    let returned_values = return_value;
                    $.each(returned_values, function( placeholder, product_details ){
                        var product_id = self.env.pos.db.get_product_by_id(product_details.id);
                        if (product_id) {
                            product_id.location_wise_qty = product_details.location_wise_qty;
                        }
                    });
                });
                let products = super.productsToDisplay;
                return products;
            }
    }
    Registries.Component.extend(ProductsWidget, PosQuantityProductsWidget);
});
