/*
* @Author: D.Jane
* @Email: jane.odoo.sp@gmail.com
*/
odoo.define('pos_stock_quantity.pos_stock', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var rpc = require("web.rpc");
    // var bus = require('bus.bus').bus;
    // var Model = require('web.Model');
    var task;

    // models.load_fields('product.product', ['type']);
        models.load_fields("product.product", ["qty_available", "type"]);

    var _super_pos = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {

            this.stock_location_modifier();

            _super_pos.initialize.call(this, session, attributes);

            var self = this;
            
            // bus.on('notification', this, function (notifications) {
            //     var stock_quant = notifications.filter(function (item) {
            //         return item[0][1] === 'pos.stock.channel';
            //     }).map(function (item) {
            //         return item[1];
            //     });
            //     var flat_stock_quant = _.reduceRight(stock_quant, function (a, b) {
            //         return a.concat(b)
            //     }, []);

            //     self.on_stock_notification(flat_stock_quant);
            // });
        },
        get_model: function (_name) {
            var _index = this.models.map(function (e) {
                return e.model;
            }).indexOf(_name);
            if (_index > -1) {
                return this.models[_index];
            }
            return false;
        },
        load_qty_after_load_product: function () {
            var wait = this.get_model('account.journal');
            console.log("waitAAAAAAAAAAAAAAAAAAAAa",wait)
            var _wait_super_loaded = wait.loaded;
            console.log("var _wait_super_loaded@@@@@@@@@@@@@@@@@",_wait_super_loaded)
            wait.loaded = function (self, journals) {
                var done = $.Deferred();
                _wait_super_loaded(self, journals);

                var ids = Object.keys(self.db.product_by_id).map(function (item) {
                    return parseInt(item);
                });

                new Model('product.product').call('read', [ids, ['qty_available']]).then(function (res) {
                    self.db.qty_by_product_id = {};
                    res.forEach(function (product) {
                        self.db.qty_by_product_id[product.id] = product.qty_available;
                    });
                    self.refresh_qty();
                    done.resolve();
                });
                return done;
            }
        },
        stock_location_modifier: function () {
            this.stock_location_ids = [];

            var stock_location = this.get_model('stock.location');
            console.log("stock_location@@@@@@@@@@@@@@",stock_location)
            var _super_loaded = stock_location.loaded;
            console.log("_super_loaded@@@@@@@@@@@@@@",_super_loaded)

            // stock_location.loaded = function (self, locations) {
            //     var done = new $.Deferred();
            //     _super_loaded(self, locations);

            //     if (!self.config.show_qty_available) {
            //         return done.resolve();
            //     }

            //     if (self.config.allow_out_of_stock) {
            //         self.config.limit_qty = 0;
            //     }

            //     if (self.config.location_only) {
            //         new Model('stock.quant').call('get_qty_available', [self.shop.id]).then(function (res) {
            //             self.stock_location_ids = _.uniq(res.map(function (item) {
            //                 return item.location_id[0];
            //             }));
            //             self.compute_qty_in_pos_location(res);
            //             done.resolve();
            //         });
            //     } else {
            //         self.load_qty_after_load_product();
            //         done.resolve();
            //     }
            //     return done;
            // };
        },
        on_stock_notification: function (stock_quant) {
            var self = this;
            var product_ids = stock_quant.map(function (item) {
                return item.product_id[0];
            });
            if (this.config && this.config.show_qty_available && product_ids.length > 0) {
                $.when(self.qty_sync(product_ids)).done(function () {
                    self.refresh_qty();
                });
            }
        },
        qty_sync: function (product_ids) {
            var self = this;
            var done = new $.Deferred();
            if (this.config.show_qty_available && this.config.location_only) {
                new Model('stock.quant')
                    .call('get_qty_available', [false, self.stock_location_ids, product_ids])
                    .then(function (res) {
                        self.recompute_qty_in_pos_location(product_ids, res);
                        done.resolve();
                    });

            } else if (this.config.show_qty_available) {
                new Model('product.product')
                    .call('read', [product_ids, ['qty_available']])
                    .then(function (res) {
                        res.forEach(function (product) {
                            self.db.qty_by_product_id[product.id] = product.qty_available;
                        });
                        done.resolve();
                    });
            } else {
                done.resolve();
            }
            return done.promise();
        },
        compute_qty_in_pos_location: function (res) {
            var self = this;
            self.db.qty_by_product_id = {};
            res.forEach(function (item) {
                var product_id = item.product_id[0];

                if (!self.db.qty_by_product_id[product_id]) {
                    self.db.qty_by_product_id[product_id] = item.qty;
                } else {
                    self.db.qty_by_product_id[product_id] += item.qty;
                }
            })
        },
        recompute_qty_in_pos_location: function (product_ids, res) {
            var self = this;
            var res_product_ids = res.map(function (item) {
                return item.product_id[0];
            });

            var out_of_stock_ids = product_ids.filter(function (id) {
                return res_product_ids.indexOf(id) === -1;
            });

            out_of_stock_ids.forEach(function (id) {
               self.db.qty_by_product_id[id] = 0;
            });

            res_product_ids.forEach(function (product_id) {
                self.db.qty_by_product_id[product_id] = false;
            });

            res.forEach(function (item) {
                var product_id = item.product_id[0];

                if (!self.db.qty_by_product_id[product_id]) {
                    self.db.qty_by_product_id[product_id] = item.qty;
                } else {
                    self.db.qty_by_product_id[product_id] += item.qty;
                }
            });
        },
        refresh_qty: function () {
            var self = this;
            var $qty_tag = $('.product-list').find('.qty-tag');
            $qty_tag.each(function () {
                var $product = $(this).parents('.product');
                var id = parseInt($product.attr('data-product-id'));
                console.log("$product@@@@@@@@@@@@@@@",$product);
                // rpc
                // .query({
                //     model: "product.product",
                //     method: "search_read",
                //     args: [],
                //     fields: ["qty_available", "type"],
                // })
                // .then(function(products) {
                //     self.db.qty_by_product_id[id] = products.qty_available;
                //     console.log("self.db.qty_by_product_id[ids]@@@@@@@@@@@@",self.db.qty_by_product_id[id])
                // });

                console.log("this!!!!!!!!!!!!!!!!!!!!!",self.db.product_by_id[id].qty_available);
                var qty = self.db.product_by_id[id].qty_available;

                if (qty === false) {
                    return;
                }

                // if (qty < 1) {
                //     $product.hide();
                // }

                if (qty === undefined) {
                    if (self.config.hide_product){
                        $product.hide();
                        return;
                    } else {
                        qty = 0;
                    }
                }

                $(this).text(qty).show('fast');

                if (qty <= self.config.limit_qty) {
                    $(this).addClass('sold-out');
                    if (!self.config.allow_out_of_stock) {
                        $product.addClass('disable');
                    }
                } else {
                    $(this).removeClass('sold-out');
                    $product.removeClass('disable');
                }
            });
        },
        get_product_image_url: function (product) {
            return window.location.origin + '/web/image?model=product.product&field=image_128&id=' + product.id;
        }
    });


    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        set_quantity: function (quantity) {
            console.log("quantity@@@@@@@@@@@@@@@@",quantity)
            console.log("self.config.limit_qty@@@@@@@@@@@",this.product.qty_available)
            _super_orderline.set_quantity.call(this, quantity);

            if (!this.pos.config.show_qty_available
                || this.pos.config.allow_out_of_stock
                || this.product.type !== 'product') {
                return;
            }

            if (quantity > this.pos.config.limit_qty){
                console.log("trqqqqqqqqqqqqqqqqqqqqqqqqqq")
                this.check_reminder();
            }
            
            if (this.pos.gui.current_screen) {
                this.check_reminder();
            }
        },
        check_reminder: function () {

            var self = this;
                
            var qty_available = this.product.qty_available || 0;
            console.log("qty_available@@@@@@@@@@@@@@@",this.product.qty_available)

            var all_product_line = this.order.orderlines.filter(function (orderline) {
                return self.product.id === orderline.product.id;
            });

            if (all_product_line.indexOf(self) === -1) {
                all_product_line.push(self);
            }

            var sum_qty = 0;
            all_product_line.forEach(function (line) {
                sum_qty += line.quantity;
            });

            if (qty_available - sum_qty < this.pos.config.limit_qty) {
                var max_available = qty_available - sum_qty + self.quantity - this.pos.config.limit_qty;
                if (max_available < 0) {
                    max_available = 0;
                }
                this.pos.gui.show_popup('order_reminder', {
                    max_available: max_available,
                    product_image_url: self.pos.get_product_image_url(self.product),
                    product_name: self.product.display_name,
                    line: self
                });
 
            }
        }
    });


    screens.ProductListWidget.include({
        render_product: function (product) {
            if (this.pos.config.show_qty_available && product.type !== 'product') {
                this.pos.db.qty_by_product_id[product.id] = false;
            }
            return this._super(product);
        },
        renderElement: function () {
            this._super();
            var self = this;
            var done = $.Deferred();
            clearInterval(task);
            task = setTimeout(function () {
                if (self.pos.config.show_qty_available) {
                    self.pos.refresh_qty();
                } else {
                    $(self.el).find('.qty-tag').hide();
                }
                done.resolve();
            }, 100);
            return done;
        }
    });

    screens.PaymentScreenWidget.include({
        finalize_validation: function () {
            if (this.pos.config && this.pos.config.show_qty_available){
                this.sub_qty();
            }
            this._super();
        },
        sub_qty: function () {
            var self = this;
            var order = this.pos.get_order();
            var orderlines = order.get_orderlines();
            var sub_qty_by_product_id = {};
            var ids = [];
            orderlines.forEach(function (line) {
                if (!sub_qty_by_product_id[line.product.id]) {
                    sub_qty_by_product_id[line.product.id] = line.quantity;
                    ids.push(line.product.id);
                } else {
                    sub_qty_by_product_id[line.product.id] += line.quantity;
                }
            });

            ids.forEach(function (id) {
                console.log("self.pos.db1111111111111111",self.pos.db)
                if (self.pos.db.product_by_id[id].qty_available !== false && self.pos.db.product_by_id[id].qty_available !== undefined){
                   self.pos.db.product_by_id[id].qty_available -= sub_qty_by_product_id[id];
                }
            });
        }
    });
});