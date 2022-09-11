/*  Copyright 2014-2017 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
    Copyright 2016 gaelTorrecillas <https://github.com/gaelTorrecillas>
    Copyright 2016 manawi <https://github.com/manawi>
    Copyright 2017 Ilmir Karamov <https://it-projects.info/team/ilmir-k>
    Copyright 2018,2019 Kolushov Alexandr <https://it-projects.info/team/KolushovAlexandr>
    License MIT (https://opensource.org/licenses/MIT). */
odoo.define("pos_product_available.PosModel", function(require) {
    "use strict";

    var rpc = require("web.rpc");
    var models = require("point_of_sale.models");
    var field_utils = require("web.field_utils");
    var utils = require('web.utils');
    var round_pr = utils.round_precision;

    models.load_fields("product.product", ["qty_available", "type", 'default_code']);

        var Order = models.Order;
    models.Order = models.Order.extend({

        get_total_with_tax: function() {
        return this.get_total_without_tax();
    },

         get_total_without_tax: function() {

            var $elem = $(".table");
            if ($elem.length > 1){
            for(var i = 1, len = $elem.length; i < len; i++){
                $elem[i].children[0].style.display = "none"
                // $elem[i].removeChild($elem[i].children[0])
                
            }
        }

        return round_pr(this.orderlines.reduce((function(sum, orderLine) {
            return sum + orderLine.get_display_price();
        }), 0), this.pos.currency.rounding);
    },
    });


    var PosModelSuper = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        get_product_model: function() {
            return _.find(this.models, function(model) {
                return model.model === "product.product";
            });
        },
        initialize: function(session, attributes) {
            // Compatibility with pos_cache module
            // preserve product.product model data for future request
            this.product_product_model = this.get_product_model(this.models);
            PosModelSuper.initialize.apply(this, arguments);
        },
        load_server_data: function() {
            // Compatibility with pos_cache module
            var self = this;

            var loaded = PosModelSuper.load_server_data.call(this);
            if (this.get_product_model(this.models)) {
                return loaded;
            }
            // If product.product model is not presented in this.models after super was called then pos_cache module installed
            return loaded.then(function() {
                return rpc
                    .query({
                        model: "product.product",
                        method: "search_read",
                        args: [],
                        fields: ["qty_available", "type"],
                        domain: self.product_product_model.domain,
                        context: _.extend(self.product_product_model.context, {
                            location: self.config.default_location_src_id[0],
                        }),
                    })
                    .then(function(products) {
                        self.add_product_qty(products);
                    });
            });
        },
        set_product_qty_available: function(product, qty) {
            product.qty_available = qty;
            this.refresh_qty_available(product);
        },
        update_product_qty_from_order_lines: function(order) {
            var self = this;
            order.orderlines.each(function(line) {
                var product = line.get_product();
                product.qty_available = product.format_float_value(
                    product.qty_available - line.get_quantity(),
                    {digits: [69, 3]}
                );
                self.refresh_qty_available(product);
            });
            // Compatibility with pos_multi_session
            order.trigger("new_updates_to_send");
        },
        add_product_qty: function(products) {
            var self = this;
            _.each(products, function(p) {
                _.extend(self.db.get_product_by_id(p.id), p);
            });
        },
        refresh_qty_available: function(product) {
            var $elem = $("[data-product-id='" + product.id + "'] .qty-tag");
            $elem.html(product.rounded_qty());
            if (product.qty_available <= 0 && !$elem.hasClass("not-available")) {
                $elem.addClass("not-available");
            }
        },
        push_order: function(order, opts) {
            var pushed = PosModelSuper.push_order.call(this, order, opts);
            if (order) {
                this.update_product_qty_from_order_lines(order);
            }
            return pushed;
        },
        push_and_invoice_order: function(order) {
            var invoiced = PosModelSuper.push_and_invoice_order.call(this, order);

            if (order && order.get_client() && order.orderlines) {
                this.update_product_qty_from_order_lines(order);
            }

            return invoiced;
        },
    });


    // exports.Orderline = Backbone.Model.extend({

    // });

    var OrderlineSuper = models.Orderline;
    models.Orderline = models.Orderline.extend({
        export_as_JSON: function() {
            var data = OrderlineSuper.prototype.export_as_JSON.apply(this, arguments);
            data.qty_available = this.product.qty_available;
            return data;
        },
        // Compatibility with pos_multi_session
        apply_ms_data: function(data) {
            if (OrderlineSuper.prototype.apply_ms_data) {
                OrderlineSuper.prototype.apply_ms_data.apply(this, arguments);
            }
            var product = this.pos.db.get_product_by_id(data.product_id);
            if (product.qty_available !== data.qty_available) {
                this.pos.set_product_qty_available(product, data.qty_available);
            }
        },
        get_discount_per: function(){
        var values_total = round_pr(this.get_unit_price() * this.get_quantity(), 2)
        var discountStr = (this.get_lst_price() - this.get_unit_display_price() ) / this.get_lst_price() * 100;
        if (this.discountStr > 0) {
            // this.get_base_price();
            return (this.discountStr / values_total * 100).toFixed(2);;
        }
        return (discountStr).toFixed(2);
    },

        get_discount_str: function(){
        var discountStr = (this.get_lst_price() - this.get_unit_display_price()) * this.get_quantity();
        if (this.discountStr > 0) {
            // this.get_base_price();
            return this.discountStr;
        }
        return (discountStr).toFixed(2);

    },


    set_discount: function(discount){
        var disc = Math.min(Math.max(parseFloat(discount) || 0, 0),100);
        this.discount = disc;
        this.discountStr = '' + disc;
        this.trigger('change',this);
    },


    get_margin : function(){
        // self.margin = (self.net_price - self.product_id.standard_price) /  self.net_price * 100
        var margin = (this.get_unit_display_price() - this.get_product().standard_price) / this.get_unit_display_price() * 100;
        return margin.toFixed(2)
    },

    get_base_price:    function(){
        var rounding = this.pos.currency.rounding;
        // if (this.discountStr < 1) {
        //     // this.get_discount_str();
        // this.get_discount_per();
        // this.get_margin();
        // }

        var unit_pr = round_pr(this.get_lst_price() * this.get_quantity() * (1 - this.get_discount_str()/100), rounding);
        return round_pr(this.get_lst_price() * this.get_quantity() * (1 - this.get_discount_str()/100), rounding);
    },
    });

    models.Product = models.Product.extend({
        format_float_value: function(val) {
            var value = parseFloat(val);
            value = field_utils.format.float(value, {digits: [69, 4]});
            return String(parseFloat(value));
        },
        rounded_qty: function() {
            return this.qty_available;
        },
    });
});
