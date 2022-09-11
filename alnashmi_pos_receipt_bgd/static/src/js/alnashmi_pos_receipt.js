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
            console.log("model.model@@@@@@@@@@@@@@@@@@",model)
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

        var res_partner_model = _.find(this.models, function(model){
            return model.model === 'res.partner';
        });

        res_partner_model.fields.push('h_birthday');
        res_partner_model.fields.push('w_birthday');
        
        // Inheritance
        return _super_posmodel.initialize.call(this, session, attributes);
    }
});



screen_widget.ReceiptScreenWidget.include({
    get_image_url: function(product_id){
        return window.location.origin + '/web/image?model=product.product&field=image_128&id='+product_id;
    },   
    get_barcode_url: function(type, barcode_val, width, height){
        return '/report/barcode/?type='+type+'&value='+barcode_val+'&width='+width+'&height='+height;
    },
    render_receipt: function() {
        var order = this.pos.get_order();
        var orderlines = order.get_orderlines();
        for (var o in orderlines)
        {

function convertNumberToWords(amount) {
    var words = new Array();
    words[0] = '';
    words[1] = 'One';
    words[2] = 'Two';
    words[3] = 'Three';
    words[4] = 'Four';
    words[5] = 'Five';
    words[6] = 'Six';
    words[7] = 'Seven';
    words[8] = 'Eight';
    words[9] = 'Nine';
    words[10] = 'Ten';
    words[11] = 'Eleven';
    words[12] = 'Twelve';
    words[13] = 'Thirteen';
    words[14] = 'Fourteen';
    words[15] = 'Fifteen';
    words[16] = 'Sixteen';
    words[17] = 'Seventeen';
    words[18] = 'Eighteen';
    words[19] = 'Nineteen';
    words[20] = 'Twenty';
    words[30] = 'Thirty';
    words[40] = 'Forty';
    words[50] = 'Fifty';
    words[60] = 'Sixty';
    words[70] = 'Seventy';
    words[80] = 'Eighty';
    words[90] = 'Ninety';
    amount = amount.toString();
    var atemp = amount.split(".");
    var number = atemp[0].split(",").join("");
    var n_length = number.length;
    var words_string = "";
    if (n_length <= 9) {
        var n_array = new Array(0, 0, 0, 0, 0, 0, 0, 0, 0);
        var received_n_array = new Array();
        for (var i = 0; i < n_length; i++) {
            received_n_array[i] = number.substr(i, 1);
        }
        for (var i = 9 - n_length, j = 0; i < 9; i++, j++) {
            n_array[i] = received_n_array[j];
        }
        for (var i = 0, j = 1; i < 9; i++, j++) {
            if (i == 0 || i == 2 || i == 4 || i == 7) {
                if (n_array[i] == 1) {
                    n_array[j] = 10 + parseInt(n_array[j]);
                    n_array[i] = 0;
                }
            }
        }
        var value = "";
        for (var i = 0; i < 9; i++) {
            if (i == 0 || i == 2 || i == 4 || i == 7) {
                value = n_array[i] * 10;
            } else {
                value = n_array[i];
            }
            if (value != 0) {
                words_string += words[value] + " ";
            }
            if ((i == 1 && value != 0) || (i == 0 && value != 0 && n_array[i + 1] == 0)) {
                words_string += "Crores ";
            }
            if ((i == 3 && value != 0) || (i == 2 && value != 0 && n_array[i + 1] == 0)) {
                words_string += "Lakhs ";
            }
            if ((i == 5 && value != 0) || (i == 4 && value != 0 && n_array[i + 1] == 0)) {
                words_string += "Thousand ";
            }
            if (i == 6 && value != 0 && (n_array[i + 1] != 0 && n_array[i + 2] != 0)) {
                words_string += "Hundred and ";
            } else if (i == 6 && value != 0) {
                words_string += "Hundred ";
            }
        }
        words_string = words_string.split("  ").join(" ");
    }
    return words_string;
}



        var words = convertNumberToWords(orderlines[o].get_display_price());
        orderlines[o].payment_value_inword = words
    }






        var product_id = 0;
        var barcode_val = 0;
        var barcode_image_url = '';
        for (var o in orderlines)
        {
            product_id = orderlines[o].get_product().id;
            orderlines[o].product_image_url = this.get_image_url(product_id);  
            orderlines[o].barcode_image_url = '';
            
            barcode_val = orderlines[o].get_product().barcode;              
            if(barcode_val != ""){
                barcode_image_url = this.get_barcode_url('QR', barcode_val, 100, 100);   
                orderlines[o].barcode_image_url = barcode_image_url;
            }                 
            //alert(orderlines[o].product_image_url+' -- '+orderlines[o].barcode_image_url);
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
                receipt: order.export_for_printing(),
                orderlines: orderlines,
                paymentlines: payment_lines,
            }));
    }           
});

});