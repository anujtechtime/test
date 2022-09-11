odoo.define('point_of_sale.AlnashmiPos', function (require) {
"use strict";

var models = require('point_of_sale.models');
var screen_widget = require('point_of_sale.screens');
var _super_posmodel = models.PosModel.prototype;
var core = require('web.core');
var QWeb = core.qweb;

models.PosModel = models.PosModel.extend({
    initialize: function (session, attributes) {
        // New code
        var product_model = _.find(this.models, function(model){
            return model.model === 'product.product';
        });

        product_model.fields.push('gold');
        product_model.fields.push('gold_gram');
        product_model.fields.push('gold_purity');
        product_model.fields.push('gw');

        product_model.fields.push('diamond');
        product_model.fields.push('diamond_rd_carat');
        product_model.fields.push('diamond_rd_qty');
        product_model.fields.push('diamond_bd_carat');
        product_model.fields.push('diamond_bd_qty');        
        product_model.fields.push('diamond_color');
        product_model.fields.push('diamond_clarity');
        product_model.fields.push('dw');

        product_model.fields.push('precious_stones');
        product_model.fields.push('precious_stones_qty');
        product_model.fields.push('precious_stones_type');
        product_model.fields.push('sw');
        product_model.fields.push('pearl_carat');

        // Inheritance
        return _super_posmodel.initialize.call(this, session, attributes);
    }
});


screen_widget.ReceiptScreenWidget.include({
    get_image_url: function(product_id){
        return window.location.origin + '/web/image?model=product.product&field=image_medium&id='+product_id;
    },   
    get_barcode_url: function(type, barcode_val, width, height){
        return '/report/barcode/?type='+type+'&value='+barcode_val+'&width='+width+'&height='+height;
    },
    render_receipt: function() {
        var order = this.pos.get_order();
        var orderlines = order.get_orderlines();
        var product_id = orderlines[0].get_product().id;
        var barcode_val = orderlines[0].get_product().barcode;

        var product_image_url = this.get_image_url(product_id);
        
        var barcode_image_url = '';
        if(barcode_val != ""){
            barcode_image_url = this.get_barcode_url('QR', barcode_val, 100, 100);    
        }

        var payment_lines = order.get_paymentlines();

        for(var k in payment_lines)
        {
            payment_lines[k].name = payment_lines[k].name.replace("Cash IQD (IQD)", "Payment");
            payment_lines[k].name = payment_lines[k].name.replace("Cash USD (USD)", "Payment");
            payment_lines[k].name = payment_lines[k].name.replace("Debt (USD)", "Debt");
            payment_lines[k].name = payment_lines[k].name.replace("Debt (IQD)", "Debt");
        }

        this.$('.pos-receipt-container').html(QWeb.render('PosTicket',{
                widget:this,
                order: order,
                product_image_url: product_image_url,
                barcode_image_url: barcode_image_url,                
                receipt: order.export_for_printing(),
                orderlines: orderlines,
                paymentlines: payment_lines,
            }));
    }           
});

});